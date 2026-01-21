"""
Media processing utilities for images, videos, and audio.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
import librosa
import soundfile as sf


class ImageProcessor:
    """Handle image processing operations."""
    
    @staticmethod
    def read_image(image_path: str) -> Optional[np.ndarray]:
        """Read image from file."""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"Error reading image: {e}")
            return None
    
    @staticmethod
    def resize_image(image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray:
        """Resize image to target size."""
        return cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)
    
    @staticmethod
    def normalize_image(image: np.ndarray) -> np.ndarray:
        """Normalize image to [0, 1] range."""
        return image.astype(np.float32) / 255.0
    
    @staticmethod
    def get_image_metadata(image_path: str) -> dict:
        """Extract image metadata using OpenCV."""
        try:
            img = cv2.imread(image_path)
            if img is None:
                return {}
            
            h, w = img.shape[:2]
            channels = img.shape[2] if len(img.shape) > 2 else 1
            
            return {
                'width': w,
                'height': h,
                'channels': channels,
                'file_size': Path(image_path).stat().st_size,
            }
        except Exception as e:
            print(f"Error extracting image metadata: {e}")
            return {}


class VideoProcessor:
    """Handle video processing operations."""
    
    @staticmethod
    def get_video_properties(video_path: str) -> dict:
        """Get video properties."""
        try:
            cap = cv2.VideoCapture(video_path)
            
            properties = {
                'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'fps': cap.get(cv2.CAP_PROP_FPS),
                'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS),
                'codec': int(cap.get(cv2.CAP_PROP_FOURCC)),
                'file_size': Path(video_path).stat().st_size,
            }
            
            cap.release()
            return properties
        except Exception as e:
            print(f"Error getting video properties: {e}")
            return {}
    
    @staticmethod
    def extract_frames(video_path: str, sample_rate: int = 5) -> List[np.ndarray]:
        """
        Extract frames from video at specified sample rate.
        
        Args:
            video_path: Path to video file
            sample_rate: Extract every nth frame
            
        Returns:
            List of frames as numpy arrays
        """
        frames = []
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % sample_rate == 0:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append(frame_rgb)
                
                frame_count += 1
            
            cap.release()
        except Exception as e:
            print(f"Error extracting frames: {e}")
        
        return frames
    
    @staticmethod
    def get_frame_at_time(video_path: str, time_seconds: float) -> Optional[np.ndarray]:
        """Get specific frame at given time."""
        try:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_number = int(time_seconds * fps)
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return None
        except Exception as e:
            print(f"Error extracting frame: {e}")
            return None


class AudioProcessor:
    """Handle audio processing operations."""
    
    @staticmethod
    def load_audio(audio_path: str, sr: int = 16000) -> Tuple[np.ndarray, int]:
        """
        Load audio file.
        
        Args:
            audio_path: Path to audio file
            sr: Sample rate
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            y, sr_loaded = librosa.load(audio_path, sr=sr)
            return y, sr_loaded
        except Exception as e:
            print(f"Error loading audio: {e}")
            return np.array([]), 0
    
    @staticmethod
    def extract_mfcc(audio: np.ndarray, sr: int, n_mfcc: int = 13) -> np.ndarray:
        """Extract MFCC features from audio."""
        try:
            mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
            return mfcc
        except Exception as e:
            print(f"Error extracting MFCC: {e}")
            return np.array([])
    
    @staticmethod
    def extract_spectrogram(audio: np.ndarray, sr: int) -> np.ndarray:
        """Extract mel-spectrogram from audio."""
        try:
            mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr)
            return librosa.power_to_db(mel_spec, ref=np.max)
        except Exception as e:
            print(f"Error extracting spectrogram: {e}")
            return np.array([])
    
    @staticmethod
    def get_audio_properties(audio_path: str) -> dict:
        """Get audio file properties."""
        try:
            y, sr = librosa.load(audio_path, sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
            
            return {
                'sample_rate': sr,
                'duration': duration,
                'frame_count': len(y),
                'file_size': Path(audio_path).stat().st_size,
            }
        except Exception as e:
            print(f"Error getting audio properties: {e}")
            return {}
