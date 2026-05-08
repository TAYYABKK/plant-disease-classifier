"""
Flask Backend API for Plant Leaf Disease Classification
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports FIRST
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)
models_dir = os.path.join(project_root, 'models')
sys.path.insert(0, models_dir)
sys.path.insert(0, project_root)

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import pickle
from werkzeug.utils import secure_filename
import io

try:
    from feature_extractor import LeafFeatureExtractor
except ImportError as e:
    print(f"ERROR: Could not import LeafFeatureExtractor: {e}")
    print(f"Looked in: {models_dir}")
    raise

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Get base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

# Create Flask app with static and template folders
app = Flask(__name__, 
            static_folder=os.path.join(FRONTEND_DIR),
            static_url_path='',
            template_folder=FRONTEND_DIR)
CORS(app)  # Enable CORS for frontend

# Configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables for model
model = None
scaler = None
label_encoder = None
feature_extractor = None

# Disease information database
DISEASE_INFO = {
    "Healthy": {
        "description": "The plant leaf appears healthy with no visible signs of disease.",
        "treatment": "Continue regular maintenance and monitoring.",
        "confidence": "High"
    },
    "Leaf Spot": {
        "description": "Fungal or bacterial leaf spot characterized by brown/yellow spots.",
        "treatment": "Remove infected leaves, apply fungicide, improve air circulation.",
        "severity": "Moderate"
    },
    "Powdery Mildew": {
        "description": "White powdery coating on leaves caused by fungal infection.",
        "treatment": "Apply sulfur-based fungicide, increase air circulation.",
        "severity": "Moderate"
    },
    "Rust": {
        "description": "Orange/brown pustules on leaf undersides caused by rust fungi.",
        "treatment": "Remove infected leaves, apply fungicide, improve drainage.",
        "severity": "Moderate"
    },
    "Blight": {
        "description": "Rapid leaf wilting and discoloration caused by fungal/bacterial pathogens.",
        "treatment": "Prune affected areas, apply copper fungicide, ensure good ventilation.",
        "severity": "High"
    },
    "Wilt": {
        "description": "Drooping and discoloration of leaves due to vascular disease.",
        "treatment": "Remove infected plants, sanitize soil, improve drainage.",
        "severity": "High"
    },
    "Mosaic": {
        "description": "Mottled yellow and green patterns on leaves caused by viral infection.",
        "treatment": "Remove infected plants, control aphids, clean tools.",
        "severity": "High"
    }
}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_model_files():
    """Load trained model and preprocessing objects"""
    global model, scaler, label_encoder, feature_extractor
    
    # Get base directory (project root)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, 'models', 'trained_model.pkl')
    scaler_path = os.path.join(base_dir, 'models', 'scaler.pkl')
    encoder_path = os.path.join(base_dir, 'models', 'label_encoder.pkl')
    
    try:
        # Check if model files exist
        if not all([os.path.exists(p) for p in [model_path, scaler_path, encoder_path]]):
            print("WARNING: Model files not found!")
            print("Please run: python ../models/train_model.py")
            return False
        
        # Load model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Load scaler
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        # Load label encoder
        with open(encoder_path, 'rb') as f:
            label_encoder = pickle.load(f)
        
        # Initialize feature extractor
        feature_extractor = LeafFeatureExtractor()
        
        print("✓ Model loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return False


def preprocess_image(image_data):
    """Preprocess image from file upload"""
    try:
        # Read image from file
        nparr = np.frombuffer(image_data.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Could not decode image")
        
        # Check image size
        if image.shape[0] == 0 or image.shape[1] == 0:
            raise ValueError("Image size is invalid")
        
        return image
        
    except Exception as e:
        raise ValueError(f"Image preprocessing error: {str(e)}")


def extract_features(image):
    """Extract features from image"""
    try:
        # Resize image
        image = cv2.resize(image, (128, 128))
        
        # Extract features
        features, _ = feature_extractor.extract_all_features_direct(image)
        
        return features
        
    except Exception as e:
        raise ValueError(f"Feature extraction error: {str(e)}")


@app.route('/', methods=['GET'])
def index():
    """Serve the frontend"""
    from flask import send_from_directory
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    model_loaded = model is not None
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'timestamp': str(pd.Timestamp.now())
    })


@app.route('/predict', methods=['POST'])
def predict():
    """Make prediction on uploaded image"""
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please train the model first.'
            }), 500
        
        # Check if file was uploaded
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file extension
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Preprocess image
        image = preprocess_image(file)
        
        # Extract features (using direct method)
        image_resized = cv2.resize(image, (128, 128))
        extractor = LeafFeatureExtractor()
        
        # Extract all features
        color_hist = extractor.extract_color_histogram(image_resized)
        texture = extractor.extract_texture_features(image_resized)
        color_moments = extractor.extract_color_moments(image_resized)
        edge = extractor.extract_edge_features(image_resized)
        shape = extractor.extract_shape_features(image_resized)
        
        features = np.concatenate([color_hist, texture, color_moments, edge, shape])
        
        # Scale features
        features_scaled = scaler.transform([features])
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        # Get disease name and confidence
        disease_class = label_encoder.inverse_transform([prediction])[0]
        confidence = float(np.max(probabilities)) * 100
        
        # Get disease information
        disease_info = DISEASE_INFO.get(disease_class, {
            "description": "Unknown disease",
            "treatment": "Please consult an expert",
            "severity": "Unknown"
        })
        
        # Prepare all predictions with probabilities
        all_predictions = []
        for idx, prob in enumerate(probabilities):
            class_name = label_encoder.inverse_transform([idx])[0]
            all_predictions.append({
                'disease': class_name,
                'probability': float(prob) * 100
            })
        
        # Sort by probability
        all_predictions.sort(key=lambda x: x['probability'], reverse=True)
        
        return jsonify({
            'success': True,
            'prediction': disease_class,
            'confidence': confidence,
            'description': disease_info.get('description', ''),
            'treatment': disease_info.get('treatment', ''),
            'severity': disease_info.get('severity', 'Unknown'),
            'all_predictions': all_predictions,
            'timestamp': str(pd.Timestamp.now())
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({
            'success': False,
            'error': f'Prediction error: {str(e)}'
        }), 500


@app.route('/info', methods=['GET'])
def info():
    """Get information about available diseases"""
    return jsonify({
        'diseases': DISEASE_INFO,
        'total_classes': len(label_encoder.classes_) if label_encoder else 0,
        'classes': list(label_encoder.classes_) if label_encoder else []
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': f'File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f}MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


if __name__ == '__main__':
    import pandas as pd
    
    print("="*50)
    print("Plant Leaf Disease Classification API")
    print("="*50)
    
    # Load model on startup
    print("\nLoading model...")
    if load_model_files():
        print("Starting Flask server...")
        
        # Get port from environment or use default
        port = int(os.environ.get('PORT', 5000))
        host = '0.0.0.0'
        
        print(f"API running at http://localhost:{port}")
        print(f"Health check: http://localhost:{port}/health")
        app.run(debug=False, host=host, port=port)
    else:
        print("ERROR: Could not start server without trained model!")
        print("Please train the model first by running:")
        print("  cd models")
        print("  python train_model.py")
