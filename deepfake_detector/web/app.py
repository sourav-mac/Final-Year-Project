"""
Flask web application for deepfake detection.
"""

import os
import torch
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from deepfake_detector.config import (
    FLASK_ENV, DEBUG, SECRET_KEY, UPLOAD_FOLDER, 
    REPORTS_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
)
from deepfake_detector.utils.file_handler import (
    allowed_file, validate_upload, ensure_upload_dir, get_file_type
)
from deepfake_detector.core.detection_engine import DetectionEngine
from deepfake_detector.forensics.report_generator import ReportGenerator


def create_app():
    """Create and configure Flask application."""
    
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configuration
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['ENV'] = FLASK_ENV
    app.config['DEBUG'] = DEBUG
    
    # Create necessary directories
    ensure_upload_dir(UPLOAD_FOLDER)
    ensure_upload_dir(REPORTS_FOLDER)
    
    # Initialize detection engine
    try:
        detection_engine = DetectionEngine()
        app.detection_engine = detection_engine
    except Exception as e:
        app.logger.warning(f"Failed to load some models: {e}")
    
    # Initialize report generator
    report_generator = ReportGenerator(REPORTS_FOLDER)
    app.report_generator = report_generator
    
    # Routes
    @app.route('/')
    def index():
        """Home page."""
        return render_template('index.html')
    
    @app.route('/api/upload', methods=['POST'])
    def upload_file():
        """Handle file upload and detection."""
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No filename'}), 400
        
        # Validate upload
        is_valid, error_msg = validate_upload(file.filename, 0)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        try:
            # Save file
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Detect media type
            media_type = get_file_type(file_path)
            
            # Run detection
            app.logger.info(f"Running detection on {filename}")
            detection_result = app.detection_engine.detect(file_path, media_type)
            
            # Generate reports
            json_report = app.report_generator.generate_json_report(detection_result)
            html_report = app.report_generator.generate_html_report(detection_result)
            
            # Prepare response
            consensus, avg_conf = detection_result.get_consensus()
            
            response = {
                'status': 'success',
                'filename': filename,
                'media_type': media_type,
                'is_deepfake': consensus,
                'confidence': float(avg_conf),
                'model_predictions': {k: bool(v) for k, v in detection_result.predictions.items()},
                'model_confidences': {k: float(v) for k, v in detection_result.confidence_scores.items()},
                'metadata': detection_result.metadata,
                'json_report': os.path.basename(json_report),
                'html_report': os.path.basename(html_report),
            }
            
            return jsonify(response), 200
        
        except Exception as e:
            app.logger.error(f"Detection error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/report/<report_name>')
    def get_report(report_name):
        """Download generated report."""
        try:
            report_path = os.path.join(REPORTS_FOLDER, secure_filename(report_name))
            
            if not os.path.exists(report_path):
                return jsonify({'error': 'Report not found'}), 404
            
            return send_file(report_path, as_attachment=True)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/info')
    def get_info():
        """Get system information."""
        return jsonify({
            'version': '1.0.0',
            'cuda_available': torch.cuda.is_available(),
            'device': str(app.detection_engine.model_registry.get_device()),
            'models_loaded': app.detection_engine.model_registry.list_models(),
        })
    
    @app.route('/api/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({'status': 'healthy'}), 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
