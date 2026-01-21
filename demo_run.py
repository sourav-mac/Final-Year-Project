"""
Simplified Demo Version - Deepfake Detection System
This is a demo version that works without heavy dependencies
"""

import sys
import os

# Add package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)

# Set absolute paths for templates and static
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deepfake_detector', 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deepfake_detector', 'static')

app.template_folder = template_dir
app.static_folder = static_dir
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['SECRET_KEY'] = 'dev-key-change-in-production'

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and demo detection."""
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No filename'}), 400
    
    filename = file.filename
    
    try:
        # DEMO RESPONSE - This is for demonstration
        # In production, this would use the actual detection models
        
        import random
        
        # Simulate analysis
        is_deepfake = random.choice([True, False])
        confidence = random.uniform(0.65, 0.95)
        
        response = {
            'status': 'success',
            'filename': filename,
            'media_type': 'image',  # Demo assumes image
            'is_deepfake': is_deepfake,
            'confidence': float(confidence),
            'model_predictions': {
                'deepfake_classifier': is_deepfake,
                'gan_detector': random.choice([True, False]),
                'facial_forensics': random.choice([True, False]),
            },
            'model_confidences': {
                'deepfake_classifier': float(confidence),
                'gan_detector': float(random.uniform(0.5, 0.9)),
                'facial_forensics': float(random.uniform(0.5, 0.9)),
            },
            'metadata': {
                'note': 'DEMO MODE - Install dependencies for real detection',
                'filename': filename,
                'analysis_time': datetime.now().isoformat(),
            },
            'json_report': f'demo_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            'html_report': f'demo_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html',
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/report/<report_name>')
def get_report(report_name):
    """Download generated report."""
    return jsonify({'status': 'Demo mode - Report generation disabled'}), 200

@app.route('/api/info')
def get_info():
    """Get system information."""
    return jsonify({
        'version': '1.0.0 (DEMO MODE)',
        'mode': 'DEMO - Install full dependencies for production use',
        'status': 'running',
        'note': 'Run: pip install -r requirements.txt for full functionality',
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy (demo mode)'}), 200

if __name__ == '__main__':
    print("""
    ╔═════════════════════════════════════════════════════════╗
    ║                 DEEPFAKE DETECTION SYSTEM                ║
    ║                      DEMO MODE v1.0                      ║
    ╠═════════════════════════════════════════════════════════╣
    ║ Running on: http://127.0.0.1:5000                       ║
    ║ Note: This is DEMO MODE with random predictions         ║
    ║                                                          ║
    ║ To use real detection models:                           ║
    ║ 1. Install dependencies: pip install -r requirements.txt ║
    ║ 2. Reinstall opencv-python and torch properly           ║
    ║ 3. Run: python run.py                                   ║
    ╠═════════════════════════════════════════════════════════╣
    ║ Press CTRL+C to quit                                    ║
    ╚═════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
