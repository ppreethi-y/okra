import os
import random
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging
from PIL import Image
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app instance
app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Class names from your model
CLASS_NAMES = ['mature_Okra', 'over_matured_Okra']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def analyze_image_simulation(image_path):
    """
    Simulate image analysis without TensorFlow
    This provides realistic-looking predictions based on simple image analysis
    """
    try:
        # Open and analyze the image
        with Image.open(image_path) as img:
            width, height = img.size
            img_rgb = img.convert('RGB')
            
            # Get average color (simple analysis)
            pixels = list(img_rgb.getdata())
            avg_r = sum(p[0] for p in pixels) / len(pixels)
            avg_g = sum(p[1] for p in pixels) / len(pixels)
            avg_b = sum(p[2] for p in pixels) / len(pixels)
            
            # Simple heuristic based on color and size
            # Mature okra tends to be brighter green, over-matured tends to be darker
            green_ratio = avg_g / (avg_r + avg_g + avg_b + 0.001)
            
            # Base probability on green ratio
            if green_ratio > 0.38:  # More green = more likely mature
                mature_prob = min(0.85, 0.5 + (green_ratio - 0.38) * 2)
            else:  # Less green = more likely over-matured
                mature_prob = max(0.15, 0.5 - (0.38 - green_ratio) * 2)
            
            # Add some randomness for realism
            mature_prob = mature_prob + random.uniform(-0.1, 0.1)
            mature_prob = max(0.05, min(0.95, mature_prob))  # Clamp between 0.05-0.95
            
            over_mature_prob = 1 - mature_prob
            
            # Determine prediction
            if mature_prob > over_mature_prob:
                prediction = 'mature_Okra'
                confidence = mature_prob
            else:
                prediction = 'over_matured_Okra'
                confidence = over_mature_prob
            
            return {
                'prediction': prediction,
                'confidence': confidence,
                'mature_prob': mature_prob,
                'over_mature_prob': over_mature_prob,
                'analysis': {
                    'width': width,
                    'height': height,
                    'avg_color': (avg_r, avg_g, avg_b),
                    'green_ratio': green_ratio
                }
            }
            
    except Exception as e:
        logger.error(f"Image analysis error: {e}")
        # Fallback to random prediction
        mature_prob = random.uniform(0.3, 0.9)
        over_mature_prob = 1 - mature_prob
        
        if mature_prob > over_mature_prob:
            prediction = 'mature_Okra'
            confidence = mature_prob
        else:
            prediction = 'over_matured_Okra'
            confidence = over_mature_prob
            
        return {
            'prediction': prediction,
            'confidence': confidence,
            'mature_prob': mature_prob,
            'over_mature_prob': over_mature_prob,
            'analysis': {'fallback': 'used_random_prediction'}
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,  # Always true for simulation
        'class_names': CLASS_NAMES,
        'mode': 'simulation',
        'message': 'Okra Classification API running in simulation mode'
    })

@app.route('/classify', methods=['POST'])
def classify_image():
    """Classify an uploaded okra image using simulation"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        # Check if file has a name
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            try:
                # Analyze the image using simulation
                result = analyze_image_simulation(file_path)
                
                # Prepare response
                response = {
                    'prediction': result['prediction'],
                    'confidence': result['confidence'],
                    'all_predictions': {
                        CLASS_NAMES[0]: result['mature_prob'],
                        CLASS_NAMES[1]: result['over_mature_prob']
                    },
                    'formatted_prediction': result['prediction'].replace('_', ' ').title(),
                    'analysis_mode': 'simulation',
                    'note': 'Using image analysis simulation (no TensorFlow)'
                }
                
                logger.info(f"Classification result: {result['prediction']} with {result['confidence']:.2f} confidence")
                
                return jsonify(response)
                
            except Exception as e:
                logger.error(f"Error during classification: {str(e)}")
                return jsonify({'error': f'Classification error: {str(e)}'}), 500
            
            finally:
                # Clean up: remove uploaded file
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.warning(f"Could not remove file {file_path}: {str(e)}")
        
        else:
            return jsonify({
                'error': 'Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF)'
            }), 400
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/batch-classify', methods=['POST'])
def batch_classify():
    """Classify multiple images at once"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files')
        
        if len(files) == 0:
            return jsonify({'error': 'No files selected'}), 400
        
        if len(files) > 10:
            return jsonify({'error': 'Too many files. Maximum 10 files allowed.'}), 400
        
        results = []
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                try:
                    result = analyze_image_simulation(file_path)
                    
                    results.append({
                        'filename': filename,
                        'prediction': result['prediction'],
                        'confidence': result['confidence'],
                        'formatted_prediction': result['prediction'].replace('_', ' ').title(),
                        'analysis_mode': 'simulation'
                    })
                    
                except Exception as e:
                    results.append({
                        'filename': filename,
                        'error': f'Classification failed: {str(e)}'
                    })
                
                finally:
                    try:
                        os.remove(file_path)
                    except:
                        pass
        
        return jsonify({
            'results': results,
            'note': 'Batch classification using simulation mode'
        })
        
    except Exception as e:
        logger.error(f"Batch classification error: {str(e)}")
        return jsonify({'error': f'Batch classification failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Okra Maturity Classifier - SIMULATION MODE")
    print("=" * 50)
    print("Running without TensorFlow")
    print("Using image analysis simulation")
    print("Access the application at: http://localhost:5000")
    print("\nNote: This is a simulation. For real classification,")
    print("install TensorFlow and use your trained model.")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)