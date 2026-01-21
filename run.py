#!/usr/bin/env python3
"""
Main entry point for Deepfake Detection System
"""

import sys
import argparse
from deepfake_detector.web.app import create_app


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Educational Deepfake Detection System'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to bind to (default: 5000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )
    
    args = parser.parse_args()
    
    # Create and run app
    app = create_app()
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
