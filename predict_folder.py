"""
Placeholder predict_folder.py
- Replace with the project's real prediction pipeline.
- Exposes predict_on_video(video_path, model) -> float
"""
import os
import random


def predict_on_video(video_path, model=None):
    """Simple placeholder that pretends to analyze the video and returns a score.
    0.0 -> real, 1.0 -> fake
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(video_path)

    # If model provided and has predict, call it (best-effort)
    try:
        if model is not None and hasattr(model, 'predict'):
            return float(model.predict(video_path))
    except Exception:
        pass

    # Fallback: deterministic pseudo-random score based on filename
    return float((sum(bytearray(os.path.basename(video_path), 'utf8')) % 100) / 100.0)
