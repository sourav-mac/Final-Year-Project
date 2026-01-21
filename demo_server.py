#!/usr/bin/env python3
"""
🛡️ Deepfake Detection System - DEMO SERVER
Educational AI-based deepfake detection system
Running in DEMO MODE with simulated predictions
"""

import http.server
import json
import os
import random
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import sys

PORT = 5000
HOST = '0.0.0.0'

class DeepfakeDemoHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for demo server."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self.serve_index()
        elif self.path == '/api/info':
            self.json_response({
                'status': 'running',
                'mode': 'DEMO MODE',
                'version': '1.0.0',
                'message': 'Deepfake Detection System (Demo)',
                'note': 'This is demo mode. Install dependencies for real detection.',
            })
        elif self.path == '/api/health':
            self.json_response({'status': 'healthy', 'mode': 'demo'})
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/api/upload':
            self.handle_upload()
        else:
            self.send_error(404)
    
    def handle_upload(self):
        """Handle file upload and return demo results."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            
            if content_length > 500 * 1024 * 1024:
                self.json_response({'error': 'File too large'}, 400)
                return
            
            # Simulate detection with random results
            is_deepfake = random.choice([True, False])
            confidence = random.uniform(0.65, 0.95)
            
            response_data = {
                'status': 'success',
                'filename': 'sample_upload.jpg',
                'media_type': 'image',
                'is_deepfake': is_deepfake,
                'confidence': round(confidence, 3),
                'model_predictions': {
                    'deepfake_classifier': is_deepfake,
                    'gan_detector': random.choice([True, False]),
                    'facial_forensics': random.choice([True, False]),
                },
                'model_confidences': {
                    'deepfake_classifier': round(confidence, 3),
                    'gan_detector': round(random.uniform(0.5, 0.9), 3),
                    'facial_forensics': round(random.uniform(0.5, 0.9), 3),
                },
                'metadata': {
                    'analysis_time': datetime.now().isoformat(),
                    'mode': 'DEMO - Random predictions for demonstration',
                    'note': 'Install full dependencies for real deepfake detection',
                },
                'json_report': 'demo_report.json',
                'html_report': 'demo_report.html',
            }
            
            self.json_response(response_data)
        
        except Exception as e:
            self.json_response({'error': str(e)}, 500)
    
    def serve_index(self):
        """Serve the index.html file."""
        # Try multiple possible paths
        base_dir = Path(__file__).parent.absolute()
        possible_paths = [
            base_dir / 'deepfake_detector' / 'templates' / 'index.html',
            Path(os.getcwd()) / 'deepfake_detector' / 'templates' / 'index.html',
            Path('deepfake_detector') / 'templates' / 'index.html',
        ]
        
        html_path = None
        for path in possible_paths:
            if path.exists():
                html_path = path
                break
        
        if html_path is None:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            # Serve fallback HTML
            fallback_html = self.get_fallback_html()
            self.wfile.write(fallback_html.encode('utf-8'))
            return
        
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(content.encode('utf-8')))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            fallback_html = self.get_fallback_html()
            self.wfile.write(fallback_html.encode('utf-8'))
    
    def get_fallback_html(self):
        """Return fallback HTML if index.html not found."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deepfake Detection System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
            padding: 40px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            color: #333;
            font-size: 32px;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 14px;
        }
        
        .upload-area {
            border: 2px dashed #667eea;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
            background-color: #f8f9ff;
        }
        
        .upload-area:hover {
            border-color: #764ba2;
            background-color: #f0f2ff;
        }
        
        .upload-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        
        .upload-text {
            color: #333;
            font-size: 16px;
            margin-bottom: 10px;
        }
        
        .upload-subtext {
            color: #999;
            font-size: 14px;
        }
        
        #fileInput {
            display: none;
        }
        
        .file-info {
            background: #f0f2ff;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .file-info.show {
            display: block;
        }
        
        .file-name {
            color: #333;
            font-weight: 500;
            margin-bottom: 5px;
        }
        
        .file-size {
            color: #999;
            font-size: 12px;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        button {
            flex: 1;
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-analyze {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-analyze:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn-analyze:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .btn-clear {
            background: #f0f2ff;
            color: #667eea;
            border: 1px solid #667eea;
        }
        
        .btn-clear:hover:not(:disabled) {
            background: #e8ebff;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 30px;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f0f2ff;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            color: #667eea;
            font-size: 14px;
        }
        
        .results {
            display: none;
        }
        
        .results.show {
            display: block;
        }
        
        .result-box {
            background: #f0f2ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .result-status {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .result-status.authentic {
            color: #28a745;
        }
        
        .result-status.deepfake {
            color: #dc3545;
        }
        
        .confidence-bar {
            background: #e0e0e0;
            height: 10px;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 10px;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
        }
        
        .predictions-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        
        .predictions-table th,
        .predictions-table td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        .predictions-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        
        .predictions-table td {
            color: #666;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }
        
        .badge.authentic {
            background: #d4edda;
            color: #155724;
        }
        
        .badge.deepfake {
            background: #f8d7da;
            color: #721c24;
        }
        
        .demo-notice {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .demo-notice strong {
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Deepfake Detection System</h1>
            <p>Educational AI-based platform for detecting manipulated media</p>
        </div>
        
        <div class="demo-notice">
            <strong>📊 DEMO MODE:</strong> This is running in demo mode with simulated predictions. Install full dependencies for real deepfake detection.
        </div>
        
        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📁</div>
            <div class="upload-text">Click to upload or drag and drop</div>
            <div class="upload-subtext">Supported: Images (JPG, PNG), Videos (MP4, AVI), Audio (WAV, MP3)</div>
            <input type="file" id="fileInput">
        </div>
        
        <div class="file-info" id="fileInfo">
            <div class="file-name" id="fileName"></div>
            <div class="file-size" id="fileSize"></div>
        </div>
        
        <div class="button-group">
            <button class="btn-analyze" id="analyzeBtn" disabled>🚀 Analyze</button>
            <button class="btn-clear" id="clearBtn">🔄 Clear</button>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div class="loading-text">Analyzing media...</div>
        </div>
        
        <div class="results" id="results">
            <div class="result-box">
                <div class="result-status" id="resultStatus"></div>
                <div id="confidenceContainer">
                    <div>Confidence Score</div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" id="confidenceFill"></div>
                    </div>
                    <div id="confidenceText" style="margin-top: 5px; color: #666; font-size: 12px;"></div>
                </div>
            </div>
            
            <div class="result-box">
                <div style="font-weight: 600; margin-bottom: 15px;">Model Predictions</div>
                <table class="predictions-table">
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Prediction</th>
                            <th>Confidence</th>
                        </tr>
                    </thead>
                    <tbody id="predictionsBody">
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const clearBtn = document.getElementById('clearBtn');
        const loading = document.getElementById('loading');
        const results = document.getElementById('results');
        
        let selectedFile = null;
        
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelect(files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });
        
        function handleFileSelect(file) {
            selectedFile = file;
            fileName.textContent = file.name;
            fileSize.textContent = `Size: ${(file.size / 1024 / 1024).toFixed(2)} MB`;
            fileInfo.classList.add('show');
            analyzeBtn.disabled = false;
        }
        
        analyzeBtn.addEventListener('click', async () => {
            if (!selectedFile) return;
            
            loading.classList.add('show');
            results.classList.remove('show');
            analyzeBtn.disabled = true;
            
            const formData = new FormData();
            formData.append('file', selectedFile);
            
            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    alert('Error: ' + (data.error || 'Detection failed'));
                    return;
                }
                
                displayResults(data);
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                loading.classList.remove('show');
                analyzeBtn.disabled = false;
            }
        });
        
        clearBtn.addEventListener('click', () => {
            selectedFile = null;
            fileInput.value = '';
            fileInfo.classList.remove('show');
            results.classList.remove('show');
            analyzeBtn.disabled = true;
        });
        
        function displayResults(data) {
            const resultStatus = document.getElementById('resultStatus');
            if (data.is_deepfake) {
                resultStatus.textContent = '⚠️ Likely Deepfake Detected';
                resultStatus.className = 'result-status deepfake';
            } else {
                resultStatus.textContent = '✓ Authentic Media';
                resultStatus.className = 'result-status authentic';
            }
            
            const confidence = data.confidence * 100;
            document.getElementById('confidenceFill').style.width = confidence + '%';
            document.getElementById('confidenceText').textContent = `${confidence.toFixed(1)}%`;
            
            const predictionsBody = document.getElementById('predictionsBody');
            predictionsBody.innerHTML = '';
            
            for (const [model, prediction] of Object.entries(data.model_predictions)) {
                const confidenceScore = data.model_confidences[model] || 0;
                const badgeClass = prediction ? 'deepfake' : 'authentic';
                const predictionText = prediction ? 'Deepfake' : 'Authentic';
                
                const row = `
                    <tr>
                        <td>${model}</td>
                        <td><span class="badge ${badgeClass}">${predictionText}</span></td>
                        <td>${(confidenceScore * 100).toFixed(1)}%</td>
                    </tr>
                `;
                predictionsBody.innerHTML += row;
            }
            
            results.classList.add('show');
        }
    </script>
</body>
</html>"""
    
    def json_response(self, data, status_code=200):
        """Send JSON response."""
        json_data = json.dumps(data, indent=2)
        json_bytes = json_data.encode('utf-8')
        
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(json_bytes))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json_bytes)
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

if __name__ == '__main__':
    server_address = (HOST, PORT)
    httpd = http.server.HTTPServer(server_address, DeepfakeDemoHandler)
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   🛡️  DEEPFAKE DETECTION SYSTEM - DEMO MODE                   ║
║                                                                ║
║   Educational AI-based Media Analysis Platform                ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                ║
║   ✨ Features:                                                ║
║   • Deepfake Detection (Images, Videos, Audio)               ║
║   • Multi-Model Ensemble Analysis                            ║
║   • Forensic Report Generation                               ║
║   • Beautiful Web Interface                                  ║
║                                                                ║
║   📊 Current Mode: DEMO with Random Predictions              ║
║   (Install dependencies for real detection)                  ║
║                                                                ║
║   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                ║
║   🚀 Server Running:                                          ║
║   → http://127.0.0.1:5000                                     ║
║   → http://localhost:5000                                     ║
║                                                                ║
║   📚 Documentation:                                           ║
║   • README.md - Full documentation                           ║
║   • QUICKSTART.md - Quick start guide                        ║
║   • examples.py - 14 code examples                           ║
║                                                                ║
║   🔧 To Use Real Detection:                                   ║
║   1. Install: pip install -r requirements.txt                ║
║   2. Run: python run.py                                       ║
║                                                                ║
║   ⏹️  Press CTRL+C to Stop Server                             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped.")
