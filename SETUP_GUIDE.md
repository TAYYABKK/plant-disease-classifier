# 🌿 Plant Leaf Disease Classifier - Setup Guide

## ⚡ Quick Setup (5 minutes)

### Step 1: Install Python Packages
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Get Dataset
1. Download PlantVillage or Kaggle dataset
2. Extract to: `data/raw/`
3. Folder structure:
   ```
   data/raw/
   ├── disease1/ (folder)
   │   ├── img1.jpg
   │   └── img2.jpg
   └── disease2/ (folder)
       ├── img1.jpg
       └── img2.jpg
   ```

### Step 3: Train Model
```bash
cd models
python train_model.py
```
**Wait 5-30 minutes** ☕

### Step 4: Start Backend
```bash
cd backend
python app.py
```

### Step 5: Open Frontend
In browser: `file:///path/to/frontend/index.html`

---

## 📋 Detailed Setup

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Modern web browser
- ~5GB free disk space

### Installation

#### 1. Check Python Version
```bash
python --version
```
Should be 3.9 or higher.

#### 2. Create Virtual Environment (Recommended)
```bash
# Navigate to project root
cd "c:\Users\tayya\Desktop\machine learning project"

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 4. Verify Installation
```bash
python
>>> import cv2
>>> import sklearn
>>> import flask
>>> print("All packages installed!")
>>> exit()
```

### Dataset Preparation

#### Option A: Download PlantVillage Dataset
1. Visit: https://github.com/spMohanty/PlantVillage-Dataset
2. Download and extract
3. Copy disease folders to: `data/raw/`

#### Option B: Download from Kaggle
1. Create Kaggle account: https://www.kaggle.com/
2. Search: "plant disease"
3. Download dataset
4. Extract to: `data/raw/`

#### Option C: Use Your Own Images
1. Create subdirectories in `data/raw/`:
   - One folder per disease
   - Folder name = disease name
2. Add JPG/PNG images to each folder
3. Minimum 50 images per disease

### Model Training

#### Start Training
```bash
cd models
python train_model.py
```

#### What Happens
1. Loads all images from `data/raw/`
2. Extracts visual features (color, texture, shape, edges)
3. Trains 3 different ML models
4. Compares performance
5. Saves best model

#### Expected Output
```
Found 5 disease classes: ['Healthy', 'Leaf_Spot', 'Powdery_Mildew', 'Rust', 'Blight']
Class 'Healthy': 250 images
Class 'Leaf_Spot': 248 images
...
Total dataset size: 1200 samples
Feature dimension: 137

Training Random Forest Classifier...
Random Forest Results:
  Accuracy:  0.9145
  Precision: 0.9123
  Recall:    0.9145
  F1-Score:  0.9129

Training SVM Classifier...
SVM Results:
  Accuracy:  0.8956
  Precision: 0.8923
  Recall:    0.8956
  F1-Score:  0.8934

Training XGBoost Classifier...
XGBoost Results:
  Accuracy:  0.9312
  Precision: 0.9301
  Recall:    0.9312
  F1-Score:  0.9306

==================================================
Best Model: XGBoost
==================================================

Model saved to trained_model.pkl
Scaler saved to scaler.pkl
Encoder saved to label_encoder.pkl
```

### Backend API Server

#### Start Server
```bash
cd backend
python app.py
```

#### Expected Output
```
==================================================
Plant Leaf Disease Classification API
==================================================

Loading model...
✓ Model loaded successfully!
Starting Flask server...
API running at http://localhost:5000
Health check: http://localhost:5000/health
 * Serving Flask app 'app'
 * Debug mode: on
 * WARNING in app.run(), never use the reload debugger with the 'use_reloader=True' in a production environment
 * Running on http://0.0.0.0:5000
```

#### Test API
In another terminal:
```bash
curl http://localhost:5000/health
```

Should return:
```json
{"status": "healthy", "model_loaded": true, "timestamp": "..."}
```

### Frontend Web Application

#### Option A: Direct File Open
1. Open `frontend/index.html` in browser
2. Should load with upload interface

#### Option B: Python HTTP Server
```bash
cd frontend
python -m http.server 8000
```
Then open: http://localhost:8000

#### Option C: VS Code Live Server
1. Install extension: "Live Server"
2. Right-click `index.html`
3. Select "Open with Live Server"

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] All pip packages installed
- [ ] Dataset in `data/raw/` with disease folders
- [ ] Model trained (files in `models/`)
- [ ] Backend running on port 5000
- [ ] Frontend loads in browser
- [ ] Can upload and predict

---

## 🆘 Troubleshooting

### Python Package Installation Issues

**Error**: `ModuleNotFoundError: No module named 'cv2'`

**Solution**:
```bash
pip install --upgrade opencv-python
```

**Error**: `Failed building wheel for xgboost`

**Solution**:
```bash
# Pre-built wheel for your platform
pip install xgboost --only-binary :all:
```

### Dataset Issues

**Error**: `No such file or directory: '../data/raw'`

**Solution**:
1. Check directory structure
2. Create missing folders manually
3. Verify path is correct

**Error**: `ValueError: Could not load image: ...`

**Solution**:
1. Check image file isn't corrupted
2. Verify file format (JPG, PNG)
3. Check file permissions

### Model Training Issues

**Error**: `Memory Error` during training

**Solution**:
1. Reduce dataset size
2. Close other applications
3. Use smaller image size
4. Upgrade RAM

**Error**: Very low accuracy (< 60%)

**Solution**:
1. Check dataset quality
2. Ensure images are properly organized
3. Verify minimum images per class (50+)
4. Check for class imbalance
5. Try data augmentation

### Backend API Issues

**Error**: `Address already in use: ('0.0.0.0', 5000)`

**Solution**:
```bash
# Find process using port 5000 and kill it
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :5000
kill -9 <PID>
```

**Error**: `Model not loaded` in API

**Solution**:
1. Verify model files exist: `models/trained_model.pkl`
2. Run training script: `python train_model.py`
3. Check file permissions

### Frontend Issues

**Error**: "Cannot connect to backend"

**Solution**:
1. Verify Flask server running: `python app.py`
2. Check port 5000 is accessible
3. Disable firewall temporarily
4. Check browser console for CORS errors

**Error**: Images not uploading

**Solution**:
1. Check file size < 5MB
2. Try JPG format
3. Clear browser cache
4. Try different browser

---

## 📊 Performance Tips

### Faster Training
```python
# Reduce dataset for testing
# Use only 100 images per class initially
```

### Faster Predictions
```python
# Use smaller image size
# Reduce feature extraction complexity
# Use RandomForest instead of SVM
```

### Better Accuracy
```python
# Use larger, diverse dataset
# Balance classes (equal images per disease)
# Use data augmentation
# Tune hyperparameters
```

---

## 📱 Running on Different Devices

### On Windows
```bash
venv\Scripts\activate
cd backend
python app.py
```

### On Mac/Linux
```bash
source venv/bin/activate
cd backend
python app.py
```

### Remote Access
To access from another machine:
```python
# In app.py, change:
app.run(host='0.0.0.0', port=5000)
# Then access from: http://YOUR_IP:5000
```

---

## 🎓 Next Steps

1. **Train Model** ← Start here
2. **Start Backend** 
3. **Test in Browser**
4. **Optimize Performance**
5. **Deploy Online** (Heroku, AWS, etc.)

---

## 📞 Need Help?

1. Check README.md
2. Review Project Plan
3. Check error logs
4. Verify all steps completed

**Good luck! 🚀**
