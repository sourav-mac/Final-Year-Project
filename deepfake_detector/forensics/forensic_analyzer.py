"""
Forensic analysis tools for detailed media examination.
"""

import numpy as np
import cv2
from PIL import Image
from PIL.ExifTags import TAGS
from typing import Dict, Any, Optional, Tuple
from pathlib import Path


class MetadataAnalyzer:
    """Extract and analyze file metadata."""
    
    @staticmethod
    def extract_image_exif(image_path: str) -> Dict[str, Any]:
        """Extract EXIF data from image."""
        exif_data = {}
        try:
            image = Image.open(image_path)
            exif = image._getexif()
            
            if exif:
                for tag_id, value in exif.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    exif_data[tag_name] = str(value)[:100]  # Limit value length
        except Exception as e:
            exif_data['error'] = str(e)
        
        return exif_data
    
    @staticmethod
    def get_file_properties(file_path: str) -> Dict[str, Any]:
        """Get basic file properties."""
        try:
            path = Path(file_path)
            stat = path.stat()
            
            return {
                'filename': path.name,
                'file_size': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime,
                'accessed': stat.st_atime,
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def analyze_file_headers(file_path: str) -> Dict[str, Any]:
        """Analyze file headers and magic numbers."""
        headers = {}
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)
                headers['magic_bytes'] = header.hex()
                headers['magic_ascii'] = ''.join(chr(b) if 32 <= b < 127 else '.' for b in header)
        except Exception as e:
            headers['error'] = str(e)
        
        return headers


class ArtifactAnalyzer:
    """Detect visual artifacts in images."""
    
    @staticmethod
    def detect_compression_artifacts(image: np.ndarray) -> Dict[str, Any]:
        """Detect JPEG compression artifacts."""
        if len(image.shape) == 3:
            image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            image_gray = image
        
        # Detect 8x8 block patterns (JPEG compression)
        block_size = 8
        artifact_score = 0
        
        for y in range(0, image_gray.shape[0] - block_size, block_size):
            for x in range(0, image_gray.shape[1] - block_size, block_size):
                block = image_gray[y:y+block_size, x:x+block_size].astype(float)
                
                # Compute variance at block boundaries
                top_edge = np.var(block[0, :])
                left_edge = np.var(block[:, 0])
                
                if top_edge > 100 or left_edge > 100:
                    artifact_score += 1
        
        artifact_score = artifact_score / ((image_gray.shape[0] // block_size) * (image_gray.shape[1] // block_size))
        
        return {
            'compression_artifact_score': float(artifact_score),
            'likely_compressed': artifact_score > 0.3,
        }
    
    @staticmethod
    def detect_noise_inconsistencies(image: np.ndarray) -> Dict[str, Any]:
        """Detect unnatural noise patterns."""
        if len(image.shape) == 3:
            image_float = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype(float)
        else:
            image_float = image.astype(float)
        
        # Apply Laplacian to detect edges
        laplacian = cv2.Laplacian(image_float, cv2.CV_64F)
        
        # Analyze noise distribution
        noise_std = np.std(laplacian)
        noise_entropy = -np.sum(np.histogram(laplacian, bins=256)[0] / laplacian.size * 
                               np.log2(np.histogram(laplacian, bins=256)[0] / laplacian.size + 1e-10))
        
        return {
            'noise_std': float(noise_std),
            'noise_entropy': float(noise_entropy),
            'unnatural_noise': noise_std < 5 or noise_std > 100,
        }
    
    @staticmethod
    def detect_color_inconsistencies(image: np.ndarray) -> Dict[str, Any]:
        """Detect color relationship inconsistencies."""
        if len(image.shape) != 3 or image.shape[2] != 3:
            return {'error': 'Expected RGB image'}
        
        r, g, b = image[:,:,0], image[:,:,1], image[:,:,2]
        
        # Compute color channel statistics
        r_mean, r_std = np.mean(r), np.std(r)
        g_mean, g_std = np.mean(g), np.std(g)
        b_mean, b_std = np.mean(b), np.std(b)
        
        # Check for channel correlation
        rg_corr = np.corrcoef(r.flatten(), g.flatten())[0, 1]
        rb_corr = np.corrcoef(r.flatten(), b.flatten())[0, 1]
        gb_corr = np.corrcoef(g.flatten(), b.flatten())[0, 1]
        
        # Natural images usually have positive correlation between channels
        unnatural = (rg_corr < 0 or rb_corr < 0 or gb_corr < 0)
        
        return {
            'r_mean': float(r_mean),
            'g_mean': float(g_mean),
            'b_mean': float(b_mean),
            'rg_correlation': float(rg_corr),
            'rb_correlation': float(rb_corr),
            'gb_correlation': float(gb_corr),
            'unnatural_colors': unnatural,
        }
    
    @staticmethod
    def detect_edge_inconsistencies(image: np.ndarray) -> Dict[str, Any]:
        """Detect unnatural edge formations."""
        if len(image.shape) == 3:
            image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            image_gray = image
        
        # Edge detection
        edges = cv2.Canny(image_gray, 50, 150)
        
        # Analyze edge distribution
        edge_count = np.count_nonzero(edges)
        edge_ratio = edge_count / edges.size
        
        # Check for too sharp or too smooth edges
        suspicious = edge_ratio < 0.01 or edge_ratio > 0.3
        
        return {
            'edge_ratio': float(edge_ratio),
            'edge_count': int(edge_count),
            'suspicious_edges': suspicious,
        }


class LuminanceAnalyzer:
    """Analyze lighting and luminance patterns."""
    
    @staticmethod
    def analyze_lighting_consistency(image: np.ndarray) -> Dict[str, Any]:
        """Analyze lighting consistency across image."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Divide image into quadrants
        h, w = gray.shape
        q1 = gray[:h//2, :w//2].mean()
        q2 = gray[:h//2, w//2:].mean()
        q3 = gray[h//2:, :w//2].mean()
        q4 = gray[h//2:, w//2:].mean()
        
        quadrants = [q1, q2, q3, q4]
        quadrant_std = np.std(quadrants)
        
        return {
            'quadrant_means': [float(q) for q in quadrants],
            'luminance_variance': float(quadrant_std),
            'inconsistent_lighting': quadrant_std > 50,
        }
    
    @staticmethod
    def detect_shadow_inconsistencies(image: np.ndarray) -> Dict[str, Any]:
        """Detect shadow and highlight inconsistencies."""
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Analyze shadow regions
        shadows = gray < 85
        highlights = gray > 170
        
        shadow_ratio = np.count_nonzero(shadows) / shadows.size
        highlight_ratio = np.count_nonzero(highlights) / highlights.size
        
        return {
            'shadow_ratio': float(shadow_ratio),
            'highlight_ratio': float(highlight_ratio),
            'extreme_shadow_highlight': shadow_ratio > 0.4 or highlight_ratio > 0.4,
        }


class ForensicAnalyzer:
    """High-level forensic analysis coordinator."""
    
    def __init__(self):
        self.metadata_analyzer = MetadataAnalyzer()
        self.artifact_analyzer = ArtifactAnalyzer()
        self.luminance_analyzer = LuminanceAnalyzer()
    
    def analyze_image(self, image_path: str, image_array: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Perform comprehensive forensic analysis on image.
        
        Args:
            image_path: Path to image file
            image_array: Optional pre-loaded image array
            
        Returns:
            Dictionary with forensic analysis results
        """
        forensic_report = {}
        
        # File-level analysis
        forensic_report['metadata'] = self.metadata_analyzer.extract_image_exif(image_path)
        forensic_report['file_properties'] = self.metadata_analyzer.get_file_properties(image_path)
        forensic_report['file_headers'] = self.metadata_analyzer.analyze_file_headers(image_path)
        
        # Load image if not provided
        if image_array is None:
            from deepfake_detector.utils.media_processor import ImageProcessor
            image_array = ImageProcessor.read_image(image_path)
            if image_array is None:
                forensic_report['error'] = 'Failed to load image'
                return forensic_report
        
        # Image-level analysis
        forensic_report['compression_analysis'] = self.artifact_analyzer.detect_compression_artifacts(image_array)
        forensic_report['noise_analysis'] = self.artifact_analyzer.detect_noise_inconsistencies(image_array)
        forensic_report['color_analysis'] = self.artifact_analyzer.detect_color_inconsistencies(image_array)
        forensic_report['edge_analysis'] = self.artifact_analyzer.detect_edge_inconsistencies(image_array)
        forensic_report['lighting_analysis'] = self.luminance_analyzer.analyze_lighting_consistency(image_array)
        forensic_report['shadow_analysis'] = self.luminance_analyzer.detect_shadow_inconsistencies(image_array)
        
        return forensic_report
