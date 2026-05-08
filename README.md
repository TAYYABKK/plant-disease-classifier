# Plant Leaf Disease Classification Web Application

A machine learning-powered web application for classifying plant leaf diseases from images using traditional ML algorithms (Random Forest, SVM, XGBoost).

## 📋 Project Overview

This project aims to help farmers and gardeners identify plant diseases early by uploading leaf images to a web application. The system uses computer vision feature extraction combined with traditional machine learning algorithms to classify diseases and provide treatment recommendations.

### Features

✅ **Web-based Interface**: User-friendly upload interface  
✅ **Real-time Predictions**: Instant disease classification  
✅ **Multiple Algorithms**: Random Forest, SVM, and XGBoost comparison  
✅ **Confidence Scores**: Probability estimates for each disease  
✅ **Disease Information**: Treatment recommendations and severity levels  
✅ **Prediction History**: View all classification results  
✅ **Download Reports**: Export predictions as text files  
✅ **Mobile-Friendly**: Responsive design for all devices  

## 🏗️ Project Structure

```
plant-leaf-disease-classifier/
├── data/
│   ├── raw/                    # Original disease images
│   ├── processed/              # Preprocessed images
│   └── splits/                 # Train/validation/test splits
├── models/
│   ├── feature_extractor.py    # Feature extraction pipeline
│   ├── train_model.py          # Model training script
│   ├── trained_model.pkl       # Saved trained model
│   ├── scaler.pkl              # Preprocessing scaler
│   └── label_encoder.pkl       # Class label encoder
├── backend/
│   ├── app.py                  # Flask API server
│   ├── requirements.txt         # Python dependencies
│   └── uploads/                # Temporary image storage
├── frontend/
│   ├── index.html              # Main webpage
│   ├── style.css               # Styling
│   └── script.js               # Interactive functionality
├── tests/
│   ├── test_model.py           # Model tests
│   └── test_api.py             # API tests
└── PROJECT_PLAN.md             # Detailed project plan
```

## 🚀 Quick Start

### Phase 1: Setup Environment

#### 1.1 Install Python Dependencies

```bash
# Navigate to backend directory
cd backend

# Install required packages
pip install -r requirements.txt
```

#### 1.2 Install Additional Tools (if needed)

```bash
# For feature extraction
pip install scikit-image

# For XGBoost
pip install xgboost

# For OpenCV
pip install opencv-python
```

### Phase 2: Prepare Dataset

#### 2.1 Download Dataset

Options:
- **PlantVillage Dataset**: https://github.com/spMohanty/PlantVillage-Dataset
- **Kaggle Plant Disease**: https://www.kaggle.com/datasets
- Your own dataset (required format: folder per disease class)

#### 2.2 Organize Dataset

```
data/raw/
├── Healthy/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Leaf_Spot/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Powdery_Mildew/
│   ├── image1.jpg
│   └── ...
└── ...
```

**Each subdirectory should contain images of that disease class.**

### Phase 3: Train Model

```bash
# Navigate to models directory
cd models

# Run training script
python train_model.py
```

This script will:
1. Load and preprocess images
2. Extract visual features (color, texture, shape, edges)
3. Train Random Forest, SVM, and XGBoost models
4. Evaluate all models
5. Save the best model to `trained_model.pkl`

**Training time**: 5-30 minutes depending on dataset size

### Phase 4: Start Backend API

```bash
# From backend directory
cd backend

# Start Flask server
python app.py
```

Expected output:
```
==================================================
Plant Leaf Disease Classification API
==================================================

Loading model...
✓ Model loaded successfully!
Starting Flask server...
API running at http://localhost:5000
Health check: http://localhost:5000/health
```

### Phase 5: Open Frontend

1. **Open the web application**:
   ```bash
   # Simply open the frontend HTML file in a browser
   # Option 1: File Explorer → Right-click → Open with Browser
   # Option 2: Use Python's simple HTTP server
   cd frontend
   python -m http.server 8000
   # Then open: http://localhost:8000
   ```

2. **Or use VS Code Live Server extension**:
   - Install "Live Server" extension
   - Right-click `index.html` → "Open with Live Server"

## 📖 Usage Guide

### 1. Upload Image

- Click the upload area or drag-drop an image
- Supported formats: JPG, PNG, GIF, BMP
- Maximum size: 5MB
- Image requirements:
  - Clear focus on leaf
  - Good lighting
  - Include affected area
  - Avoid excessive blur

### 2. Analyze

- Click "Analyze Image" button or press Enter
- Wait for processing (usually < 1 second)

### 3. Review Results

- **Disease Name**: Primary disease classification
- **Confidence Score**: Model certainty (0-100%)
- **Description**: What the disease is
- **Treatment**: Recommended treatment
- **Severity**: High/Moderate/Low
- **All Predictions**: Full list with probabilities

### 4. Download Report

- Click "📥 Download Report" to save results as text file
- Share with agricultural experts if needed

### 5. Analyze Another

- Click "📷 Analyze Another Image" to reset

## 🔬 Technical Details

### Feature Extraction

The system extracts multiple types of features from leaf images:

1. **Color Histogram** (96 features)
   - HSV color space analysis
   - Captures color distribution

2. **Texture Features** (LBP - 27 features)
   - Local Binary Pattern
   - Captures surface texture patterns

3. **Color Moments** (9 features)
   - Mean, variance, skewness per channel
   - LAB color space

4. **Edge Features** (2 features)
   - Edge density
   - Number of contours

5. **Shape Features** (3 features)
   - Area, perimeter, circularity

**Total Feature Dimension**: 137 features per image

### Machine Learning Models

#### Random Forest
- **Ensemble**: 200 decision trees
- **Strengths**: Robust, handles non-linearity well
- **Speed**: Fast inference
- **Interpretability**: Feature importance

#### Support Vector Machine (SVM)
- **Kernel**: RBF (Radial Basis Function)
- **Strengths**: Excellent for high-dimensional data
- **Speed**: Moderate inference
- **Tuning**: C=10, gamma='scale'

#### XGBoost
- **Boosting**: Gradient boosting algorithm
- **Strengths**: State-of-the-art performance
- **Speed**: Fast training and inference
- **Regularization**: Prevents overfitting

### Model Selection

The system automatically:
1. Trains all three models
2. Evaluates on test set
3. Compares F1-scores
4. Deploys the best model
5. Reports performance metrics

## 📊 Expected Performance

- **Accuracy**: 85-95% (varies by dataset)
- **Inference Time**: <500ms per image
- **Upload Size**: <5MB
- **Model Size**: ~50-100MB

## 🐛 Troubleshooting

### Issue: "Model not loaded" error

**Solution**:
1. Ensure `trained_model.pkl` exists in `models/` directory
2. Run `python models/train_model.py` to train
3. Check file paths are correct

### Issue: "Cannot connect to backend"

**Solution**:
1. Ensure Flask server is running on port 5000
2. Check firewall allows localhost connections
3. Verify `python app.py` started successfully
4. Check for port conflicts: `netstat -an | grep 5000`

### Issue: "Image preprocessing error"

**Solution**:
1. Ensure image format is valid (JPG, PNG, GIF, BMP)
2. Check file is not corrupted
3. Verify file size < 5MB
4. Try a different image

### Issue: Low accuracy predictions

**Solution**:
1. Check dataset quality and size (minimum 100 images per class)
2. Ensure images are representative
3. Verify dataset is balanced across classes
4. Consider data augmentation
5. Train with more epochs/iterations

### Issue: API timeout

**Solution**:
1. Check feature extraction isn't too slow
2. Verify system has sufficient RAM
3. Try a smaller image size
4. Close other applications

## 🔄 Workflow Overview

```
┌─────────────────────┐
│  Upload Image       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Preprocess         │◄──── Resize to 128x128
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Extract Features   │◄──── 137-D feature vector
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Scale Features     │◄──── Normalize using scaler
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Predict with ML    │◄──── Load trained model
│  Model              │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Get Probabilities  │◄──── All classes
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Display Results    │
└─────────────────────┘
```

## 🔐 Security Notes

1. **File Upload Validation**: Only image files allowed
2. **File Size Limit**: 5MB maximum
3. **Temporary Storage**: Uploads cleaned automatically
4. **API Authentication**: Add for production
5. **Rate Limiting**: Implement to prevent abuse

## 📈 Future Enhancements

1. **Deep Learning**: Implement CNN-based classification
2. **User Accounts**: Track prediction history
3. **Mobile App**: Native iOS/Android versions
4. **Real-time Detection**: Webcam support
5. **Model Explainability**: LIME/SHAP visualizations
6. **Cloud Deployment**: AWS/Azure/GCP
7. **Batch Processing**: Multiple images at once
8. **Expert Integration**: Connect to agriculture experts
9. **Treatment Marketplace**: Link to products/services
10. **Community**: User-submitted corrections

## 📚 References

### Datasets
- PlantVillage: https://github.com/spMohanty/PlantVillage-Dataset
- Kaggle: https://www.kaggle.com/

### Libraries
- scikit-learn: https://scikit-learn.org/
- OpenCV: https://opencv.org/
- Flask: https://flask.palletsprojects.com/
- XGBoost: https://xgboost.readthedocs.io/

### Papers
- Plant Disease Detection using Deep Learning
- Traditional ML for Plant Pathology
- Computer Vision in Agriculture

## 👥 Team

**University Project** for [Your University]  
**Course**: [Your Course]  
**Semester**: [Your Semester]

## 📝 License

This project is for educational purposes.

## 📧 Support

For issues or questions:
1. Check this README
2. Review troubleshooting section
3. Check project logs
4. Contact project maintainer

---

**Last Updated**: 2024  
**Status**: Ready for Phase 1 (Data Preparation)
