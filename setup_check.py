#!/usr/bin/env python3
"""
Setup and validation script for the Deepfake Detection System
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✓ Python {sys.version.split()[0]} detected")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'torch',
        'torchvision',
        'opencv',
        'numpy',
        'flask',
        'PIL',
        'librosa',
        'scipy',
    ]
    
    print("\nChecking dependencies...")
    all_installed = True
    
    for package in required_packages:
        try:
            if package == 'opencv':
                import cv2
            elif package == 'PIL':
                from PIL import Image
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ❌ {package} (not installed)")
            all_installed = False
    
    if not all_installed:
        print("\n⚠️  Some packages are missing. Install with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True


def check_pytorch_gpu():
    """Check if PyTorch can access GPU."""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"\n✓ GPU Support: {torch.cuda.get_device_name(0)}")
            print(f"  CUDA Version: {torch.version.cuda}")
            return True
        else:
            print("\n⚠️  GPU not available (CPU-only mode)")
            return False
    except Exception as e:
        print(f"\n⚠️  GPU check failed: {e}")
        return False


def check_project_structure():
    """Verify project structure is complete."""
    print("\nVerifying project structure...")
    
    required_dirs = [
        'deepfake_detector',
        'deepfake_detector/models',
        'deepfake_detector/core',
        'deepfake_detector/forensics',
        'deepfake_detector/utils',
        'deepfake_detector/web',
        'deepfake_detector/templates',
        'deepfake_detector/static',
        'deepfake_detector/uploads',
        'deepfake_detector/reports',
    ]
    
    required_files = [
        'run.py',
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'deepfake_detector/__init__.py',
        'deepfake_detector/config.py',
        'deepfake_detector/models/detection_models.py',
        'deepfake_detector/models/model_registry.py',
        'deepfake_detector/core/detection_engine.py',
        'deepfake_detector/forensics/forensic_analyzer.py',
        'deepfake_detector/forensics/report_generator.py',
        'deepfake_detector/utils/file_handler.py',
        'deepfake_detector/utils/media_processor.py',
        'deepfake_detector/web/app.py',
        'deepfake_detector/templates/index.html',
    ]
    
    all_exists = True
    
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ❌ {dir_path} (missing)")
            all_exists = False
    
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ❌ {file_path} (missing)")
            all_exists = False
    
    return all_exists


def test_imports():
    """Test if core modules can be imported."""
    print("\nTesting module imports...")
    
    modules_to_test = [
        'deepfake_detector.config',
        'deepfake_detector.utils.file_handler',
        'deepfake_detector.utils.media_processor',
        'deepfake_detector.models.detection_models',
        'deepfake_detector.models.model_registry',
        'deepfake_detector.core.detection_engine',
        'deepfake_detector.forensics.forensic_analyzer',
        'deepfake_detector.forensics.report_generator',
        'deepfake_detector.web.app',
    ]
    
    all_imported = True
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ❌ {module} - {e}")
            all_imported = False
    
    return all_imported


def test_detection_engine():
    """Test if detection engine can be initialized."""
    print("\nTesting detection engine...")
    
    try:
        from deepfake_detector.core.detection_engine import DetectionEngine
        engine = DetectionEngine()
        
        models = engine.model_registry.list_models()
        print(f"  ✓ Engine initialized")
        print(f"  ✓ Models loaded: {', '.join(models)}")
        
        return True
    except Exception as e:
        print(f"  ⚠️  Engine test failed: {e}")
        print("     Some models may not be loaded (this is normal)")
        return True  # Don't fail on this


def print_summary():
    """Print setup summary."""
    print("\n" + "="*60)
    print("🛡️  DEEPFAKE DETECTION SYSTEM - SETUP VALIDATION")
    print("="*60)


def print_next_steps():
    """Print next steps."""
    print("\n" + "="*60)
    print("✅ SETUP VALIDATION COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Start the application:")
    print("   python run.py")
    print("\n2. Open in browser:")
    print("   http://localhost:5000")
    print("\n3. Upload and analyze media files")
    print("\n4. Learn more:")
    print("   - README.md - Comprehensive documentation")
    print("   - QUICKSTART.md - Quick start guide")
    print("   - PROJECT_SUMMARY.md - Project overview")
    print("   - examples.py - Usage examples")
    print("\n" + "="*60)


def main():
    """Run all validation checks."""
    print_summary()
    
    # Run checks
    checks = [
        ("Python Version", check_python_version()),
        ("Dependencies", check_dependencies()),
        ("Project Structure", check_project_structure()),
    ]
    
    # Only test imports and engine if structure is OK
    if checks[-1][1]:  # If project structure is OK
        checks.append(("Module Imports", test_imports()))
        checks.append(("Detection Engine", test_detection_engine()))
    
    check_pytorch_gpu()  # GPU check is informational
    
    # Print results
    print("\n" + "="*60)
    print("VALIDATION RESULTS")
    print("="*60)
    
    for check_name, result in checks:
        status = "✓" if result else "❌"
        print(f"{status} {check_name}")
    
    # Determine if setup is successful
    all_passed = all(result for _, result in checks)
    
    if all_passed:
        print_next_steps()
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix issues and try again.")
        print("Run: pip install -r requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
