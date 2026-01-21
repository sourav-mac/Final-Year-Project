"""
Model registry and loading utilities.
"""

import torch
import os
from typing import Optional, Dict, Any
from deepfake_detector.models.detection_models import (
    DeepfakeClassifier,
    GANArtifactDetector,
    FacialForensicsModel,
    FaceDetectionModel
)


class ModelRegistry:
    """Registry for managing detection models."""
    
    _models: Dict[str, torch.nn.Module] = {}
    _device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    @classmethod
    def register_model(cls, name: str, model: torch.nn.Module) -> None:
        """Register a model."""
        cls._models[name] = model.to(cls._device)
        print(f"Model registered: {name}")
    
    @classmethod
    def get_model(cls, name: str) -> Optional[torch.nn.Module]:
        """Get a registered model."""
        return cls._models.get(name)
    
    @classmethod
    def list_models(cls) -> list:
        """List all registered models."""
        return list(cls._models.keys())
    
    @classmethod
    def load_all_models(cls, model_dir: str = 'models') -> None:
        """
        Load all available models.
        
        Args:
            model_dir: Directory containing model checkpoints
        """
        models_config = {
            'deepfake_classifier': DeepfakeClassifier,
            'gan_detector': GANArtifactDetector,
            'facial_forensics': FacialForensicsModel,
            'face_detection': FaceDetectionModel,
        }
        
        for model_name, model_class in models_config.items():
            try:
                model = model_class()
                
                # Try to load checkpoint if it exists
                checkpoint_path = os.path.join(model_dir, f'{model_name}.pth')
                if os.path.exists(checkpoint_path):
                    checkpoint = torch.load(checkpoint_path, map_location=cls._device)
                    if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
                        model.load_state_dict(checkpoint['state_dict'])
                    else:
                        model.load_state_dict(checkpoint)
                    print(f"Loaded checkpoint for {model_name}")
                
                cls.register_model(model_name, model)
                model.eval()
            except Exception as e:
                print(f"Warning: Failed to load model {model_name}: {e}")
    
    @classmethod
    def set_device(cls, device: str) -> None:
        """Set device for all models."""
        cls._device = torch.device(device)
        for model in cls._models.values():
            model.to(cls._device)
    
    @classmethod
    def get_device(cls) -> torch.device:
        """Get current device."""
        return cls._device


def create_model(model_type: str, pretrained: bool = False) -> Optional[torch.nn.Module]:
    """
    Create a model instance.
    
    Args:
        model_type: Type of model to create
        pretrained: Whether to load pretrained weights
        
    Returns:
        Model instance or None if type not found
    """
    models = {
        'deepfake_classifier': DeepfakeClassifier,
        'gan_detector': GANArtifactDetector,
        'facial_forensics': FacialForensicsModel,
        'face_detection': FaceDetectionModel,
    }
    
    if model_type not in models:
        print(f"Unknown model type: {model_type}")
        return None
    
    model = models[model_type]()
    
    if pretrained:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        checkpoint_path = f'models/{model_type}.pth'
        
        if os.path.exists(checkpoint_path):
            checkpoint = torch.load(checkpoint_path, map_location=device)
            if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
                model.load_state_dict(checkpoint['state_dict'])
            else:
                model.load_state_dict(checkpoint)
    
    return model
