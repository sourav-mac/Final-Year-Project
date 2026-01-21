"""
Configuration settings for the Deepfake Detection System.
"""

import os
from datetime import timedelta

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Upload Configuration
UPLOAD_FOLDER = 'deepfake_detector/uploads'
REPORTS_FOLDER = 'deepfake_detector/reports'
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'wav', 'mp3', 'm4a'}

# Model Configuration
MODEL_PATHS = {
    'face_detection': 'models/face_detection_model.pth',
    'deepfake_classifier': 'models/deepfake_classifier.pth',
    'gan_detector': 'models/gan_detector.pth',
    'facial_forensics': 'models/facial_forensics.pth',
}

# Detection Parameters
CONFIDENCE_THRESHOLD = 0.5
MIN_FACE_SIZE = 10  # pixels
FRAME_SAMPLE_RATE = 5  # Process every nth frame for videos
AUDIO_SAMPLE_RATE = 16000  # Hz

# Processing Configuration
NUM_WORKERS = 4
BATCH_SIZE = 8
DEVICE = 'cuda'  # 'cuda' or 'cpu'

# Report Configuration
GENERATE_HEATMAPS = True
INCLUDE_METADATA = True
REPORT_FORMAT = 'pdf'  # pdf, json, html

# Security
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
