#!/usr/bin/env python3
"""
Script to run the Okra Classification Flask application
"""

import os
import sys
import webbrowser
from threading import Timer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def open_browser():
    """Open browser to the application after a short delay"""
    Timer(2.0, lambda: webbrowser.open('http://localhost:5000')).start()

def main():
    print("=" * 50)
    print("Okra Maturity Classifier")
    print("=" * 50)
    
    # Check if model exists
    model_path = 'okra_vgg19_classifier.h5'
    if not os.path.exists(model_path):
        print(f"WARNING: Model file '{model_path}' not found!")
        print("The application will start but classification will not work.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    try:
        # Import and run the app
        from app import app
        
        print("\nStarting Okra Maturity Classifier Server...")
        print("Server will be available at: http://localhost:5000")
        print("Press Ctrl+C to stop the server\n")
        
        # Open browser automatically
        open_browser()
        
        # Run the application
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"ERROR: Failed to import application: {e}")
        print("This usually means there's an error in app.py")
        print("Please check the error messages above.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"ERROR: Failed to start server: {e}")
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()