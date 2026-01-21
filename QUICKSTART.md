# 🚀 Quick Start Guide

## Installation & Setup (5 minutes)

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python run.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### Step 3: Open in Browser
Navigate to: `http://localhost:5000`

## Using the Web Interface

### 1. Upload Media
- Click the upload area or drag and drop
- Supported formats:
  - **Images**: JPG, JPEG, PNG, GIF, BMP
  - **Videos**: MP4, AVI, MOV, MKV
  - **Audio**: WAV, MP3, M4A

### 2. Analyze
- Click "🚀 Analyze" button
- Wait for processing to complete (30 seconds - 2 minutes depending on file size)

### 3. Review Results
- See verdict: "Authentic" or "Deepfake Detected"
- View confidence score (0-100%)
- Check individual model predictions
- Review metadata analysis

### 4. Download Report
- **JSON Report**: Machine-readable detailed analysis
- **HTML Report**: Human-readable formatted report

## Command Line Usage

### Analyze Single File
```python
from deepfake_detector.core.detection_engine import DetectionEngine

engine = DetectionEngine()
result = engine.detect('image.jpg')
print(result.to_dict())
```

### Batch Analysis
```python
from deepfake_detector.core.detection_engine import DetectionEngine

engine = DetectionEngine()
files = ['image1.jpg', 'image2.jpg', 'video.mp4']
results = engine.batch_detect(files)

for result in results:
    print(f"{result.filename}: {result.get_consensus()}")
```

### Generate Reports Programmatically
```python
from deepfake_detector.core.detection_engine import DetectionEngine
from deepfake_detector.forensics.report_generator import ReportGenerator

engine = DetectionEngine()
result = engine.detect('image.jpg')

generator = ReportGenerator()
json_report = generator.generate_json_report(result)
html_report = generator.generate_html_report(result)

print(f"Reports saved: {json_report}, {html_report}")
```

## Understanding Results

### Consensus Score
- **0-50%**: Likely Authentic
- **50-70%**: Uncertain (recommend manual review)
- **70-100%**: Likely Deepfake

### Model Predictions
Each model votes independently:
- **Deepfake Classifier**: Detects common deepfake patterns
- **GAN Detector**: Identifies GAN-generated artifacts
- **Facial Forensics**: Analyzes facial inconsistencies

Final decision uses majority voting.

### Metadata Analysis
- **Compression Artifacts**: JPEG compression signatures
- **Color Coherence**: Channel correlation analysis
- **Edge Formation**: Natural vs synthetic edge patterns
- **Lighting**: Consistency of light sources
- **Shadow Patterns**: Realistic shadow distribution

## Troubleshooting

### Issue: Model Loading Fails
```
Warning: Failed to load model deepfake_classifier: ...
```
**Solution**: Models are optional. The system will work with available models. If you have pre-trained weights, place `.pth` files in `deepfake_detector/models/`

### Issue: GPU Not Used
**Check**: CUDA is properly installed
```python
import torch
print(torch.cuda.is_available())  # Should print True
```

**Fix**: Install PyTorch with CUDA support:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Issue: Out of Memory
**Solution**: Reduce batch size or video frame sampling rate in `config.py`

### Issue: Files Not Processing
**Check**: File format is supported and file size < 500MB

## Performance Tips

### For Better Accuracy
1. Use high-resolution images (1000x1000+ pixels)
2. For videos, ensure multiple faces are visible
3. Audio should be at least 5 seconds long

### For Faster Processing
1. Set `FRAME_SAMPLE_RATE = 10` for videos (sample every 10th frame)
2. Use GPU acceleration (ensure CUDA is available)
3. Reduce `BATCH_SIZE` if memory-constrained

## API Endpoints

### POST `/api/upload`
Upload and analyze media file.

**Request:**
```
Form Data: file (multipart/form-data)
```

**Response:**
```json
{
  "status": "success",
  "filename": "image.jpg",
  "media_type": "image",
  "is_deepfake": false,
  "confidence": 0.85,
  "model_predictions": { ... },
  "model_confidences": { ... }
}
```

### GET `/api/report/<report_name>`
Download generated report.

### GET `/api/info`
Get system information (CUDA, loaded models, etc.)

### GET `/api/health`
Health check endpoint.

## Example Workflows

### Workflow 1: Verify Incoming Video
```python
from deepfake_detector.core.detection_engine import DetectionEngine
from deepfake_detector.forensics.report_generator import ReportGenerator

engine = DetectionEngine()
generator = ReportGenerator()

result = engine.detect('incoming_video.mp4')
is_deepfake, confidence = result.get_consensus()

if confidence > 0.7:
    print(f"Alert: Likely deepfake detected (confidence: {confidence:.1%})")
    html_report = generator.generate_html_report(result)
    print(f"Report saved: {html_report}")
else:
    print("Video appears authentic")
```

### Workflow 2: Batch Verification
```python
from pathlib import Path
from deepfake_detector.core.detection_engine import DetectionEngine

engine = DetectionEngine()
image_files = list(Path('images_to_verify').glob('*.jpg'))

results = engine.batch_detect(image_files)

suspicious = [r for r in results if r.get_consensus()[0]]
print(f"Suspicious files: {len(suspicious)}/{len(results)}")

for result in suspicious:
    print(f"  - {result.filename}: {result.get_consensus()[1]:.1%} confidence")
```

## Next Steps

1. **Fine-tune Models**: Train on custom dataset for your use case
2. **Integrate with Pipeline**: Use the Python API in your existing systems
3. **Deploy to Production**: Use Docker/cloud services
4. **Add Custom Rules**: Extend forensic analysis with domain-specific checks

## Learning Resources

This project demonstrates:
- ✅ Deep Learning with PyTorch
- ✅ Computer Vision (OpenCV, CNNs)
- ✅ Web Development (Flask)
- ✅ Ensemble Learning
- ✅ Signal Processing (Audio)
- ✅ Forensic Analysis

## Support & Issues

For issues, errors, or questions:
1. Check the troubleshooting section above
2. Review error logs in console
3. Check README.md for more details
4. Create an issue in the repository

---

Happy detecting! 🛡️
