"""
Placeholder kernel_utils.py
- Replace or extend with your real model-loading code.
- This file provides a CPU-safe get_model() that can be replaced with the project's real loader.
"""
import torch
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "weights" / "efficientnet_b7.pth"


def get_model(device=None):
    """Return a model object or None.

    This placeholder returns a minimal object with a `predict` method that accepts
    a numpy array or path and returns a float score. Replace with your real model loader.
    """
    if device is None:
        device = torch.device("cpu")

    class DummyModel:
        def predict(self, x):
            return 0.5

    return DummyModel()
