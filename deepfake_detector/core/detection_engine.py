"""
Core detection pipeline and analysis engine.
"""

import torch
import numpy as np
import cv2
from typing import Dict, List, Tuple, Optional, Any
from deepfake_detector.models.model_registry import ModelRegistry
from deepfake_detector.utils.media_processor import ImageProcessor, VideoProcessor, AudioProcessor
from deepfake_detector.config import CONFIDENCE_THRESHOLD, FRAME_SAMPLE_RATE


class DetectionResult:
    """Container for detection results."""
    
    def __init__(self, media_type: str, filename: str):
        self.media_type = media_type  # 'image' or 'video'
        self.filename = filename
        self.predictions: Dict[str, Any] = {}
        self.confidence_scores: Dict[str, float] = {}
        self.metadata: Dict[str, Any] = {}
        self.heatmaps: Dict[str, np.ndarray] = {}
        self.analysis_details: Dict[str, Any] = {}
    
    def add_prediction(self, model_name: str, prediction: bool, confidence: float, details: Dict = None):
        """Add prediction from a model."""
        self.predictions[model_name] = prediction
        self.confidence_scores[model_name] = confidence
        if details:
            self.analysis_details[model_name] = details
    
    def get_consensus(self) -> Tuple[bool, float]:
        """Get consensus prediction from all models."""
        if not self.predictions:
            return False, 0.0
        
        # Weighted voting
        is_deepfake_votes = [1 if v else 0 for v in self.predictions.values()]
        confidence_scores = list(self.confidence_scores.values())
        
        consensus_vote = np.mean(is_deepfake_votes) > 0.5
        avg_confidence = np.mean(confidence_scores)
        
        return consensus_vote, avg_confidence
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        consensus, avg_conf = self.get_consensus()
        
        return {
            'filename': self.filename,
            'media_type': self.media_type,
            'is_deepfake': consensus,
            'average_confidence': float(avg_conf),
            'model_predictions': {k: bool(v) for k, v in self.predictions.items()},
            'model_confidences': {k: float(v) for k, v in self.confidence_scores.items()},
            'metadata': self.metadata,
            'analysis_details': self.analysis_details,
        }


class ImageAnalyzer:
    """Analyzer for static images."""
    
    def __init__(self, model_registry: ModelRegistry):
        self.model_registry = model_registry
        self.device = model_registry.get_device()
    
    def preprocess_image(self, image: np.ndarray, target_size: Tuple[int, int] = (224, 224)) -> torch.Tensor:
        """Preprocess image for model input."""
        # Resize
        image_resized = ImageProcessor.resize_image(image, target_size)
        
        # Normalize
        image_normalized = ImageProcessor.normalize_image(image_resized)
        
        # Convert to tensor and add batch dimension
        tensor = torch.from_numpy(image_normalized).permute(2, 0, 1).unsqueeze(0)
        
        return tensor.to(self.device)
    
    def analyze(self, image_path: str) -> DetectionResult:
        """
        Analyze image for deepfakes.
        
        Args:
            image_path: Path to image file
            
        Returns:
            DetectionResult object
        """
        result = DetectionResult('image', image_path)
        
        # Read image
        image = ImageProcessor.read_image(image_path)
        if image is None:
            result.metadata['error'] = 'Failed to read image'
            return result
        
        # Store metadata
        result.metadata = ImageProcessor.get_image_metadata(image_path)
        
        # Preprocess
        tensor = self.preprocess_image(image)
        
        # Run detection models
        with torch.no_grad():
            # Deepfake classifier
            classifier = self.model_registry.get_model('deepfake_classifier')
            if classifier:
                logits = classifier(tensor)
                probs = torch.nn.functional.softmax(logits, dim=1)
                confidence = float(probs[0, 1].cpu().numpy())
                is_fake = confidence > CONFIDENCE_THRESHOLD
                result.add_prediction('deepfake_classifier', is_fake, confidence)
            
            # GAN artifact detector
            gan_detector = self.model_registry.get_model('gan_detector')
            if gan_detector:
                logits = gan_detector(tensor)
                probs = torch.nn.functional.softmax(logits, dim=1)
                confidence = float(probs[0, 1].cpu().numpy())
                is_fake = confidence > CONFIDENCE_THRESHOLD
                result.add_prediction('gan_detector', is_fake, confidence)
            
            # Facial forensics
            facial = self.model_registry.get_model('facial_forensics')
            if facial:
                logits = facial(tensor)
                probs = torch.nn.functional.softmax(logits, dim=1)
                confidence = float(probs[0, 1].cpu().numpy())
                is_fake = confidence > CONFIDENCE_THRESHOLD
                result.add_prediction('facial_forensics', is_fake, confidence)
        
        return result


class VideoAnalyzer:
    """Analyzer for videos."""
    
    def __init__(self, model_registry: ModelRegistry):
        self.model_registry = model_registry
        self.device = model_registry.get_device()
        self.image_analyzer = ImageAnalyzer(model_registry)
    
    def analyze(self, video_path: str, sample_rate: int = FRAME_SAMPLE_RATE) -> DetectionResult:
        """
        Analyze video for deepfakes.
        
        Args:
            video_path: Path to video file
            sample_rate: Extract every nth frame
            
        Returns:
            DetectionResult object
        """
        result = DetectionResult('video', video_path)
        
        # Get video properties
        result.metadata = VideoProcessor.get_video_properties(video_path)
        
        # Extract frames
        frames = VideoProcessor.extract_frames(video_path, sample_rate=sample_rate)
        
        if not frames:
            result.metadata['error'] = 'Failed to extract frames'
            return result
        
        # Analyze frames
        frame_predictions = []
        frame_confidences = []
        
        for frame in frames:
            # Analyze single frame
            frame_tensor = self.image_analyzer.preprocess_image(frame)
            
            with torch.no_grad():
                classifier = self.model_registry.get_model('deepfake_classifier')
                if classifier:
                    logits = classifier(frame_tensor)
                    probs = torch.nn.functional.softmax(logits, dim=1)
                    confidence = float(probs[0, 1].cpu().numpy())
                    is_fake = confidence > CONFIDENCE_THRESHOLD
                    frame_predictions.append(is_fake)
                    frame_confidences.append(confidence)
        
        if frame_predictions:
            # Aggregate results across frames
            num_fake_frames = sum(frame_predictions)
            fake_frame_ratio = num_fake_frames / len(frame_predictions)
            avg_confidence = np.mean(frame_confidences)
            
            # Determine if video is deepfake based on frame analysis
            is_deepfake = fake_frame_ratio > 0.3  # More than 30% fake frames
            
            result.add_prediction('frame_analysis', is_deepfake, float(avg_confidence), {
                'num_frames_analyzed': len(frame_predictions),
                'num_fake_frames': num_fake_frames,
                'fake_frame_ratio': float(fake_frame_ratio),
            })
            
            result.analysis_details['temporal_consistency'] = {
                'frame_predictions': [bool(p) for p in frame_predictions],
                'frame_confidences': [float(c) for c in frame_confidences],
            }
        
        return result


class AudioAnalyzer:
    """Analyzer for audio content."""
    
    def __init__(self, model_registry: ModelRegistry):
        self.model_registry = model_registry
        self.device = model_registry.get_device()
    
    def analyze(self, audio_path: str) -> DetectionResult:
        """
        Analyze audio for synthesis/deepfake detection.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            DetectionResult object
        """
        result = DetectionResult('audio', audio_path)
        
        # Load audio
        audio, sr = AudioProcessor.load_audio(audio_path)
        if len(audio) == 0:
            result.metadata['error'] = 'Failed to load audio'
            return result
        
        # Get audio properties
        result.metadata = AudioProcessor.get_audio_properties(audio_path)
        
        # Extract features
        mfcc = AudioProcessor.extract_mfcc(audio, sr)
        mel_spec = AudioProcessor.extract_spectrogram(audio, sr)
        
        # Store feature statistics
        result.analysis_details['mfcc_stats'] = {
            'mean': float(np.mean(mfcc)),
            'std': float(np.std(mfcc)),
            'min': float(np.min(mfcc)),
            'max': float(np.max(mfcc)),
        }
        
        result.analysis_details['spectrogram_stats'] = {
            'mean': float(np.mean(mel_spec)),
            'std': float(np.std(mel_spec)),
            'min': float(np.min(mel_spec)),
            'max': float(np.max(mel_spec)),
        }
        
        # Simple heuristic: check for unnatural spectral characteristics
        # This is a placeholder for a proper audio deepfake detector
        spectral_entropy = -np.sum((mel_spec / mel_spec.sum()) * np.log2(mel_spec / mel_spec.sum() + 1e-10))
        is_suspicious = spectral_entropy < 5.0  # Low entropy might indicate synthesis
        
        result.add_prediction('audio_analysis', is_suspicious, 0.5, {
            'spectral_entropy': float(spectral_entropy),
            'suspicious_patterns': is_suspicious,
        })
        
        return result


class DetectionEngine:
    """Main detection engine coordinating all analyses."""
    
    def __init__(self):
        self.model_registry = ModelRegistry()
        self.model_registry.load_all_models()
        
        self.image_analyzer = ImageAnalyzer(self.model_registry)
        self.video_analyzer = VideoAnalyzer(self.model_registry)
        self.audio_analyzer = AudioAnalyzer(self.model_registry)
    
    def detect(self, file_path: str, media_type: Optional[str] = None) -> DetectionResult:
        """
        Main detection method for any media file.
        
        Args:
            file_path: Path to media file
            media_type: Type of media ('image', 'video', 'audio') - auto-detected if None
            
        Returns:
            DetectionResult object
        """
        if media_type == 'image':
            return self.image_analyzer.analyze(file_path)
        elif media_type == 'video':
            return self.video_analyzer.analyze(file_path)
        elif media_type == 'audio':
            return self.audio_analyzer.analyze(file_path)
        else:
            # Auto-detect
            from deepfake_detector.utils.file_handler import get_file_type
            detected_type = get_file_type(file_path)
            return self.detect(file_path, detected_type)
    
    def batch_detect(self, file_paths: List[str]) -> List[DetectionResult]:
        """
        Analyze multiple files.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            List of DetectionResult objects
        """
        results = []
        for file_path in file_paths:
            try:
                result = self.detect(file_path)
                results.append(result)
            except Exception as e:
                result = DetectionResult('unknown', file_path)
                result.metadata['error'] = str(e)
                results.append(result)
        
        return results
