"""
Example usage scenarios for the Deepfake Detection System
"""

# Example 1: Basic Image Analysis
# ===============================
from deepfake_detector.core.detection_engine import DetectionEngine

engine = DetectionEngine()

# Analyze single image
result = engine.detect('sample_image.jpg', 'image')
is_deepfake, confidence = result.get_consensus()

print(f"Verdict: {'Deepfake' if is_deepfake else 'Authentic'}")
print(f"Confidence: {confidence:.1%}")


# Example 2: Video Analysis with Temporal Tracking
# ================================================
result = engine.detect('sample_video.mp4', 'video')

temporal_data = result.analysis_details.get('temporal_consistency', {})
frame_predictions = temporal_data.get('frame_predictions', [])
fake_count = sum(frame_predictions)
total_frames = len(frame_predictions)

print(f"\nVideo Analysis:")
print(f"Analyzed {total_frames} frames")
print(f"Suspicious frames: {fake_count}/{total_frames}")
print(f"Confidence: {result.get_consensus()[1]:.1%}")


# Example 3: Batch Processing Multiple Files
# ===========================================
import os
from pathlib import Path

image_dir = 'images_to_analyze'
files = [str(f) for f in Path(image_dir).glob('*.jpg')]

results = engine.batch_detect(files)

for result in results:
    is_fake, conf = result.get_consensus()
    status = "⚠️ Deepfake" if is_fake else "✓ Authentic"
    print(f"{result.filename}: {status} ({conf:.1%})")


# Example 4: Detailed Forensic Analysis
# ======================================
from deepfake_detector.forensics.forensic_analyzer import ForensicAnalyzer
from deepfake_detector.utils.media_processor import ImageProcessor

analyzer = ForensicAnalyzer()

# Get forensic report
forensic_report = analyzer.analyze_image('test_image.jpg')

print("\nForensic Analysis Results:")
print(f"- Compression artifacts: {forensic_report['compression_analysis']['compression_artifact_score']:.2f}")
print(f"- Color inconsistencies: {forensic_report['color_analysis']['unnatural_colors']}")
print(f"- Edge formation issues: {forensic_report['edge_analysis']['suspicious_edges']}")
print(f"- Lighting inconsistencies: {forensic_report['lighting_analysis']['inconsistent_lighting']}")


# Example 5: Generate Reports Programmatically
# =============================================
from deepfake_detector.forensics.report_generator import ReportGenerator

generator = ReportGenerator()

result = engine.detect('image.jpg')

# Generate both JSON and HTML reports
json_report_path = generator.generate_json_report(result)
html_report_path = generator.generate_html_report(result)

print(f"\nReports generated:")
print(f"- JSON: {json_report_path}")
print(f"- HTML: {html_report_path}")

# Access the report data
report_data = result.to_dict()
print(f"Report data: {report_data}")


# Example 6: Custom Model Predictions
# ===================================
import torch
import numpy as np
from deepfake_detector.models.model_registry import ModelRegistry
from deepfake_detector.utils.media_processor import ImageProcessor

registry = ModelRegistry()
registry.load_all_models()

# Load and preprocess image
image = ImageProcessor.read_image('test.jpg')
image_resized = ImageProcessor.resize_image(image, (224, 224))
image_normalized = ImageProcessor.normalize_image(image_resized)
image_tensor = torch.from_numpy(image_normalized).permute(2, 0, 1).unsqueeze(0)

device = registry.get_device()
image_tensor = image_tensor.to(device)

# Run each model individually
with torch.no_grad():
    classifier = registry.get_model('deepfake_classifier')
    if classifier:
        logits = classifier(image_tensor)
        probs = torch.nn.functional.softmax(logits, dim=1)
        confidence = float(probs[0, 1].cpu().numpy())
        print(f"\nDeepfake Classifier Confidence: {confidence:.1%}")


# Example 7: Audio Analysis
# =========================
audio_result = engine.detect('audio_file.wav', 'audio')

mfcc_stats = audio_result.analysis_details.get('mfcc_stats', {})
spec_stats = audio_result.analysis_details.get('spectrogram_stats', {})

print(f"\nAudio Analysis:")
print(f"- MFCC Mean: {mfcc_stats.get('mean', 'N/A')}")
print(f"- Spectral Entropy: {audio_result.analysis_details.get('audio_analysis', {}).get('spectral_entropy', 'N/A')}")


# Example 8: Confidence Threshold Customization
# ============================================
from deepfake_detector import config

# Adjust sensitivity
original_threshold = config.CONFIDENCE_THRESHOLD
config.CONFIDENCE_THRESHOLD = 0.7  # More strict (fewer false positives)

result_strict = engine.detect('image.jpg')
print(f"\nWith strict threshold (0.7): {result_strict.get_consensus()}")

# Restore original
config.CONFIDENCE_THRESHOLD = original_threshold


# Example 9: Metadata Extraction
# ==============================
from deepfake_detector.forensics.forensic_analyzer import MetadataAnalyzer

metadata_analyzer = MetadataAnalyzer()

# Extract EXIF data
exif_data = metadata_analyzer.extract_image_exif('image_with_exif.jpg')
print(f"\nEXIF Data:")
for key, value in exif_data.items():
    print(f"  {key}: {value}")

# Get file properties
file_props = metadata_analyzer.get_file_properties('image.jpg')
print(f"\nFile Properties:")
for key, value in file_props.items():
    print(f"  {key}: {value}")


# Example 10: Web Server Integration
# ==================================
# This is handled in deepfake_detector/web/app.py
# But you can also use it programmatically:

from deepfake_detector.web.app import create_app
import os

# Create Flask app
app = create_app()

# Access the detection engine from the app
with app.app_context():
    result = app.detection_engine.detect('image.jpg')
    print(f"Analysis result: {result.to_dict()}")


# Example 11: Stream Processing (Large File)
# ==========================================
def analyze_large_video_in_chunks(video_path):
    """Process large video file in chunks."""
    from deepfake_detector.utils.media_processor import VideoProcessor
    from deepfake_detector.core.detection_engine import ImageAnalyzer
    from deepfake_detector.models.model_registry import ModelRegistry
    
    registry = ModelRegistry()
    registry.load_all_models()
    analyzer = ImageAnalyzer(registry)
    
    # Extract frames with larger sample rate to reduce memory
    frames = VideoProcessor.extract_frames(video_path, sample_rate=10)
    
    predictions = []
    for i, frame in enumerate(frames):
        # Analyze each frame
        tensor = analyzer.preprocess_image(frame)
        # Process and store results
        print(f"Processed frame {i}")
    
    return predictions

# analyze_large_video_in_chunks('large_video.mp4')


# Example 12: Integration with External Systems
# =============================================
def process_incoming_media(file_path, alert_callback=None):
    """
    Process incoming media and trigger alerts if deepfake detected.
    
    This shows how to integrate the detection system with external workflows.
    """
    
    engine = DetectionEngine()
    result = engine.detect(file_path)
    is_deepfake, confidence = result.get_consensus()
    
    if confidence > 0.7:  # High confidence deepfake
        if alert_callback:
            alert_callback({
                'status': 'ALERT',
                'file': file_path,
                'confidence': confidence,
                'details': result.to_dict()
            })
        return False  # Block the file
    
    elif confidence > 0.5:  # Uncertain
        if alert_callback:
            alert_callback({
                'status': 'REVIEW',
                'file': file_path,
                'confidence': confidence,
                'details': result.to_dict()
            })
        return None  # Mark for manual review
    
    else:  # Likely authentic
        return True  # Allow the file

# Usage:
# def my_alert_handler(alert_data):
#     print(f"Alert: {alert_data}")
#     # Send email, log to database, etc.
#
# result = process_incoming_media('file.jpg', alert_callback=my_alert_handler)


# Example 13: Model Performance Analysis
# ======================================
def analyze_model_agreement(image_path):
    """
    Analyze how well different models agree with each other.
    High disagreement might indicate uncertain cases.
    """
    
    result = engine.detect(image_path)
    
    predictions = result.predictions.values()
    agreement = (sum(predictions) / len(predictions)) if predictions else 0.5
    
    print(f"\nModel Agreement Analysis:")
    print(f"- Consensus prediction: {result.get_consensus()[0]}")
    print(f"- Agreement ratio: {agreement:.1%}")
    print(f"- Individual predictions: {result.predictions}")
    
    if 0.3 < agreement < 0.7:
        print("⚠️ Models disagree - manual review recommended")
    else:
        print("✓ Models agree - confident prediction")

# analyze_model_agreement('test_image.jpg')


# Example 14: Performance Metrics
# ===============================
import time
from pathlib import Path

def benchmark_detection_speed(image_dir, num_samples=10):
    """Benchmark detection speed on multiple images."""
    
    images = list(Path(image_dir).glob('*.jpg'))[:num_samples]
    
    start_time = time.time()
    
    results = engine.batch_detect([str(img) for img in images])
    
    elapsed = time.time() - start_time
    
    print(f"\nPerformance Metrics:")
    print(f"- Processed {len(results)} images")
    print(f"- Total time: {elapsed:.2f}s")
    print(f"- Average per image: {elapsed/len(results):.2f}s")
    print(f"- Images per second: {len(results)/elapsed:.2f}")

# benchmark_detection_speed('images_folder')


print("\n" + "="*50)
print("Examples completed! Explore each to learn the system.")
print("="*50)
