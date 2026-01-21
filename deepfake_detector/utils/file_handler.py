"""
File handling utilities for media upload and processing.
"""

import os
from werkzeug.utils import secure_filename
from deepfake_detector.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_upload(filename: str, file_size: int) -> tuple[bool, str]:
    """
    Validate uploaded file.
    
    Args:
        filename: Original filename
        file_size: File size in bytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not filename:
        return False, "No filename provided"
    
    if not allowed_file(filename):
        return False, f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
    
    if file_size > MAX_FILE_SIZE:
        return False, f"File too large. Maximum size: {MAX_FILE_SIZE / (1024**2):.0f} MB"
    
    if file_size == 0:
        return False, "File is empty"
    
    return True, ""


def get_secure_filename(filename: str) -> str:
    """Get secure filename."""
    return secure_filename(filename)


def get_file_type(filepath: str) -> str:
    """
    Determine file type (image, video, audio).
    
    Args:
        filepath: Path to file
        
    Returns:
        File type string: 'image', 'video', 'audio', or 'unknown'
    """
    if not os.path.exists(filepath):
        return 'unknown'
    
    # Extension-based detection (simple and reliable)
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext in {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}:
        return 'image'
    elif ext in {'.mp4', '.avi', '.mov', '.mkv'}:
        return 'video'
    elif ext in {'.wav', '.mp3', '.m4a'}:
        return 'audio'
    
    return 'unknown'


def ensure_upload_dir(upload_dir: str) -> None:
    """Ensure upload directory exists."""
    os.makedirs(upload_dir, exist_ok=True)
