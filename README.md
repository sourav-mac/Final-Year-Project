# Deepfake Detection System

A modern web application for detecting deepfake videos using deep learning techniques. This project combines state-of-the-art machine learning models with an intuitive user interface to help identify manipulated video content.

## Features

- 🎥 Real-time deepfake video analysis
- 🚀 Modern, responsive web interface
- 💫 Smooth animations and transitions
- 📊 Clear visualization of detection results
- 🔒 Privacy-focused local processing

## Tech Stack

### Backend
- FastAPI for high-performance API endpoints
- PyTorch for deep learning inference
- FaceNet for face detection and analysis
- OpenCV for video processing
- Albumentations for image augmentation

### Frontend
- React with TypeScript for robust UI development
- TailwindCSS for modern styling
- Axios for API communication
- React Icons for beautiful iconography
- React Dropzone for intuitive file uploads

## Quick Start

1. Clone the repository
2. Set up the backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

3. Set up the frontend:
```bash
cd frontend
npm install
npm run dev
```

4. Open http://localhost:5173 in your browser

## Usage

1. Upload a video file (supports MP4, AVI, or MOV format)
2. Wait for the analysis to complete
3. View the detailed results showing:
   - Prediction score (0 to 1)
   - Clear indication of whether the video is real or fake
   - Confidence metrics

## Contributing

Feel free to submit issues and pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License - see LICENSE file for details