#!/usr/bin/env python3
"""
Simple test to check if the app can be imported
"""

try:
    from app import app
    print("✓ Successfully imported app from app.py")
    print(f"✓ App type: {type(app)}")
    print("✓ App should be working correctly!")
    
    # Check if model is loaded
    from app import model
    if model:
        print("✓ Model is loaded")
    else:
        print("✗ Model is not loaded")
        
except ImportError as e:
    print(f"✗ Import error: {e}")
except Exception as e:
    print(f"✗ Other error: {e}")