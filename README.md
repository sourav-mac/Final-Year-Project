# 🛡️ Deepfake Detection System

An educational AI-based platform for detecting manipulated media (images, videos, and audio).

## 📋 Overview

This is an original deepfake detection system built from scratch for educational purposes. It uses multiple AI models to analyze media files and identify potential deepfakes with detailed forensic reports.

**Features:**
- 🎬 **Image Analysis** - Detect face manipulations and synthetic images
- 📹 **Video Analysis** - Frame-by-frame deepfake detection with temporal consistency checks
- 🎙️ **Audio Analysis** - Detect synthetic voices and audio artifacts
- 🧠 **Multi-Model Ensemble** - Combines multiple detection models for robust predictions
- 📊 **Forensic Reports** - Generate detailed JSON and HTML reports with metadata analysis
- 🔬 **Artifact Detection** - JPEG compression, color inconsistencies, edge analysis
- ⚡ **Real-time Processing** - Fast analysis with GPU acceleration support

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip
- CUDA (optional, for GPU acceleration)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd Final-Year-Project
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# source venv/bin/activate  # On Linux/Mac
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Application

**Start the web server:**
```bash
python run.py --host 0.0.0.0 --port 5000
```

Then open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
deepfake_detector/
├── config.py                 # Configuration settings
├── models/
│   ├── detection_models.py   # Neural network architectures
│   └── model_registry.py     # Model management
├── core/
│   └── detection_engine.py   # Main detection pipeline
├── forensics/
│   ├── forensic_analyzer.py  # Forensic analysis tools
│   └── report_generator.py   # Report generation
├── utils/
│   ├── file_handler.py       # File handling and validation
│   └── media_processor.py    # Image/video/audio processing
├── web/
│   └── app.py               # Flask web application
├── templates/
│   └── index.html           # Web interface
├── static/                  # Static assets
├── uploads/                 # Uploaded files
└── reports/                 # Generated reports
```

## 🔧 Core Components

### Detection Models

1. **DeepfakeClassifier** - Binary classifier for deepfake vs authentic images
2. **GANArtifactDetector** - Detects traces of GAN-generated images
3. **FacialForensicsModel** - Analyzes facial morphing and inconsistencies
4. **FaceDetectionModel** - Detects and localizes faces in images

### Analysis Engines

- **ImageAnalyzer** - Analyzes static images
- **VideoAnalyzer** - Analyzes video frames and temporal consistency
- **AudioAnalyzer** - Analyzes audio for synthesis artifacts
- **ForensicAnalyzer** - Detailed forensic analysis

### Forensic Capabilities

- **EXIF/Metadata Extraction**
- **JPEG Compression Artifact Analysis**
- **Color Relationship Analysis**
- **Lighting and Shadow Consistency**
- **Edge Formation Analysis**
- **Noise Pattern Detection**

## 📊 Detection Results

Each analysis produces:

```json
{
  "filename": "image.jpg",
  "media_type": "image",
  "is_deepfake": false,
  "average_confidence": 0.85,
  "model_predictions": {
    "deepfake_classifier": false,
    "gan_detector": false,
    "facial_forensics": false
  },
  "model_confidences": {
    "deepfake_classifier": 0.92,
    "gan_detector": 0.78,
    "facial_forensics": 0.85
  },
  "metadata": { ... }
}
```

## 🎓 Educational Focus

This project demonstrates:

1. **Deep Learning** - CNN architectures for image classification
2. **Computer Vision** - Face detection, artifact detection, forensic analysis
3. **Signal Processing** - Audio feature extraction (MFCC, Spectrograms)
4. **Web Development** - Flask backend, interactive web interface
5. **Ensemble Learning** - Multi-model voting for robust predictions

## 📈 How It Works

### 1. Image Analysis Pipeline

```
Input Image
    ↓
Preprocessing & Resizing
    ↓
[Deepfake Classifier] → Prediction + Confidence
[GAN Artifact Detector] → Prediction + Confidence
[Facial Forensics] → Prediction + Confidence
    ↓
Ensemble Voting → Final Decision
    ↓
Forensic Analysis (Metadata, Artifacts, Lighting)
    ↓
Detailed Report
```

### 2. Video Analysis Pipeline

```
Input Video
    ↓
Extract Frames (every nth frame)
    ↓
Process Each Frame Through Image Pipeline
    ↓
Temporal Consistency Analysis
    ↓
Calculate Fake Frame Ratio
    ↓
Final Verdict + Report
```

### 3. Audio Analysis Pipeline

```
Input Audio
    ↓
Load and Resample
    ↓
Extract MFCC Features
    ↓
Extract Mel-Spectrogram
    ↓
Analyze Spectral Characteristics
    ↓
Detect Synthesis Indicators
    ↓
Report
```

## 🔐 Security & Privacy

- Files are temporarily stored in the `uploads` directory
- Reports are generated and can be downloaded
- No data is permanently stored or transmitted to external servers
- For production use, implement file encryption and cleanup policies

## 💡 Customization

### Adjust Detection Sensitivity

Edit `deepfake_detector/config.py`:
```python
CONFIDENCE_THRESHOLD = 0.5  # Lower = more sensitive
FRAME_SAMPLE_RATE = 5       # Process every nth frame
```

### Add Custom Models

Extend `models/detection_models.py` with new architectures and register in `model_registry.py`.

### Integrate with Your Pipeline

```python
from deepfake_detector.core.detection_engine import DetectionEngine

engine = DetectionEngine()
result = engine.detect('path/to/file.jpg')
print(result.to_dict())
```

## 🧪 Testing

```bash
# Test image analysis
python -c "
from deepfake_detector.core.detection_engine import DetectionEngine
engine = DetectionEngine()
result = engine.detect('test_image.jpg', 'image')
print(result.to_dict())
"
```

## 📚 Dependencies

- **PyTorch** - Deep learning framework
- **OpenCV** - Computer vision
- **NumPy/SciPy** - Numerical computing
- **Pillow** - Image processing
- **Librosa** - Audio processing
- **Flask** - Web framework
- **scikit-learn** - Machine learning utilities

## 🤝 Contributing

This is an educational project. Feel free to:
- Improve model architectures
- Add new detection methods
- Enhance forensic analysis
- Optimize performance
- Add new features

## 📝 License

This project is for educational purposes only.

## ⚠️ Disclaimer

This system is for educational and research purposes. While it aims to detect deepfakes, no system is 100% accurate. Always verify important media through multiple sources and expert analysis.

## 📧 Support

For issues and questions, please create an issue in the repository.

---

**Built for learning. Designed for accuracy. Created for a safer digital world.** 🌍
