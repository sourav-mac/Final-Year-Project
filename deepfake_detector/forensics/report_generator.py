"""
Report generation for detection results.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class ReportGenerator:
    """Generate detailed forensic reports."""
    
    def __init__(self, reports_dir: str = 'deepfake_detector/reports'):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=1,  # Center
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=12,
            spaceBefore=12,
        )
    
    def generate_json_report(self, detection_result: Any, output_path: Optional[str] = None) -> str:
        """
        Generate JSON report.
        
        Args:
            detection_result: DetectionResult object
            output_path: Optional custom output path
            
        Returns:
            Path to generated report
        """
        if output_path is None:
            filename = f"{detection_result.filename.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            output_path = os.path.join(self.reports_dir, filename)
        
        report_data = {
            'generation_timestamp': datetime.now().isoformat(),
            'case_id': self._generate_case_id(),
            'analysis': detection_result.to_dict(),
        }
        
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        return output_path
    
    def generate_html_report(self, detection_result: Any, output_path: Optional[str] = None) -> str:
        """
        Generate HTML report.
        
        Args:
            detection_result: DetectionResult object
            output_path: Optional custom output path
            
        Returns:
            Path to generated report
        """
        if output_path is None:
            filename = f"{detection_result.filename.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            output_path = os.path.join(self.reports_dir, filename)
        
        consensus, avg_conf = detection_result.get_consensus()
        result_text = "⚠️ LIKELY DEEPFAKE" if consensus else "✓ AUTHENTIC"
        result_color = "#dc3545" if consensus else "#28a745"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Deepfake Detection Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    color: #333;
                    background-color: #f8f9fa;
                }}
                .container {{
                    max-width: 900px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px solid #1f77b4;
                    padding-bottom: 20px;
                    margin-bottom: 20px;
                }}
                .case-id {{
                    font-size: 12px;
                    color: #666;
                    margin-top: 10px;
                }}
                .result-box {{
                    background-color: {result_color};
                    color: white;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                    font-size: 18px;
                    text-align: center;
                    font-weight: bold;
                }}
                .confidence {{
                    font-size: 16px;
                    margin-top: 10px;
                }}
                .section {{
                    margin: 25px 0;
                    padding: 15px;
                    background-color: #f0f5f9;
                    border-left: 4px solid #1f77b4;
                }}
                .section-title {{
                    font-size: 16px;
                    font-weight: bold;
                    color: #1f77b4;
                    margin-bottom: 10px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #1f77b4;
                    color: white;
                }}
                .timestamp {{
                    text-align: right;
                    color: #999;
                    font-size: 12px;
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Deepfake Detection Report</h1>
                    <div class="case-id">Case ID: {self._generate_case_id()}</div>
                </div>
                
                <div class="result-box">
                    {result_text}
                    <div class="confidence">Confidence: {avg_conf:.1%}</div>
                </div>
                
                <div class="section">
                    <div class="section-title">File Information</div>
                    <table>
                        <tr><th>Property</th><th>Value</th></tr>
                        <tr><td>Filename</td><td>{detection_result.filename}</td></tr>
                        <tr><td>Media Type</td><td>{detection_result.media_type}</td></tr>
                        <tr><td>Analysis Time</td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
                    </table>
                </div>
                
                <div class="section">
                    <div class="section-title">Model Predictions</div>
                    <table>
                        <tr><th>Model</th><th>Result</th><th>Confidence</th></tr>
        """
        
        for model_name, prediction in detection_result.predictions.items():
            confidence = detection_result.confidence_scores.get(model_name, 0)
            result = "Deepfake" if prediction else "Authentic"
            html_content += f"""
                        <tr>
                            <td>{model_name}</td>
                            <td>{result}</td>
                            <td>{confidence:.1%}</td>
                        </tr>
            """
        
        html_content += """
                    </table>
                </div>
                
                <div class="section">
                    <div class="section-title">Metadata</div>
                    <table>
        """
        
        for key, value in detection_result.metadata.items():
            html_content += f"""
                        <tr><td>{key}</td><td>{str(value)[:100]}</td></tr>
            """
        
        html_content += f"""
                    </table>
                </div>
                
                <div class="timestamp">
                    Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return output_path
    
    def _generate_case_id(self) -> str:
        """Generate unique case ID."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        import random
        random_part = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"CASE-{timestamp}-{random_part}"
