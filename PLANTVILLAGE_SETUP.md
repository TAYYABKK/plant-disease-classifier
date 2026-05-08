# 🌾 PlantVillage Dataset Setup Guide

**Reference**: Mohanty et al., 2016 - PlantVillage: A Large-Scale Crowdsourced Dataset of Leaf Images

## Quick Download (5 minutes)

### Option 1: GitHub Direct Download (Recommended)

1. **Visit GitHub Repository**:
   ```
   https://github.com/spMohanty/PlantVillage-Dataset
   ```

2. **Download the Dataset**:
   - Click the green "Code" button
   - Select "Download ZIP"
   - Wait for download (~3-4 GB)

3. **Extract Files**:
   ```bash
   # Extract the ZIP file
   # Result: PlantVillage-Dataset-master/ folder
   ```

4. **Organize for Your Project**:
   ```bash
   # Inside the extracted folder, find:
   # PlantVillage-Dataset-master/raw/color/
   
   # Copy all disease folders to your project:
   copy "PlantVillage-Dataset-master/raw/color/*" "data/raw/"
   
   # On Mac/Linux:
   cp PlantVillage-Dataset-master/raw/color/* data/raw/
   ```

### Option 2: Kaggle Download

1. **Install Kaggle CLI**:
   ```bash
   pip install kaggle
   ```

2. **Search for PlantVillage**:
   - Go to: https://www.kaggle.com/
   - Search: "plantvillage"
   - Look for: "PlantVillage Dataset"

3. **Download via Command Line**:
   ```bash
   kaggle datasets download -d easonlai/plant-disease-dataset-original-sized
   ```

4. **Extract and organize** to `data/raw/`

### Option 3: Direct GitHub Clone (For Developers)

```bash
# Clone the repository
git clone https://github.com/spMohanty/PlantVillage-Dataset.git

# Navigate to color folder
cd PlantVillage-Dataset/raw/color

# Copy to your project
copy * path/to/your/data/raw/
```

---

## PlantVillage Dataset Details

### Dataset Statistics
- **Total Images**: 55,448 images
- **Plant Species**: 14 species
- **Disease Classes**: 38 disease categories + 1 healthy
- **Total Classes**: 39
- **Image Resolution**: 256 × 256 pixels
- **Image Format**: JPG
- **Size on Disk**: ~4 GB
- **License**: Public domain

### Disease Categories Included

**Crop: Apple** (4 diseases)
- Apple_Scab
- Apple_Black_Rot
- Apple_Rust
- Apple_Healthy

**Crop: Corn** (4 diseases)
- Corn_Cercospora_Leaf_Spot
- Corn_Common_Rust
- Corn_Northern_Leaf_Blight
- Corn_Healthy

**Crop: Grape** (4 diseases)
- Grape_Black_Rot
- Grape_Black_Measles
- Grape_Leaf_Blight
- Grape_Healthy

**Crop: Peach** (2 diseases)
- Peach_Bacterial_Spot
- Peach_Healthy

**Crop: Potato** (3 diseases)
- Potato_Early_Blight
- Potato_Late_Blight
- Potato_Healthy

**Crop: Strawberry** (2 diseases)
- Strawberry_Healthy
- Strawberry_Leaf_Scorch

**Crop: Tomato** (9 diseases)
- Tomato_Bacterial_Spot
- Tomato_Early_Blight
- Tomato_Late_Blight
- Tomato_Leaf_Mold
- Tomato_Septoria_Leaf_Spot
- Tomato_Spider_Mites
- Tomato_Target_Spot
- Tomato_Yellow_Leaf_Curl_Virus
- Tomato_Healthy

**Crop: Bell_Pepper** (2 diseases)
- Pepper_Bell_Bacterial_Spot
- Pepper_Bell_Healthy

**Crop: Blueberry** (1 disease)
- Blueberry_Healthy

**Crop: Cherry** (2 diseases)
- Cherry_Powdery_Mildew
- Cherry_Healthy

**Crop: Orange** (1 disease)
- Orange_Haunglongbing

**Crop: Raspberry** (1 disease)
- Raspberry_Healthy

**Crop: Soybean** (1 disease)
- Soybean_Frogeye_Leaf_Spot

**Crop: Squash** (1 disease)
- Squash_Powdery_Mildew

---

## Directory Structure After Download

After extracting PlantVillage dataset, your structure should look like:

```
your_project/data/raw/
├── Apple_Healthy/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ... (200+ images)
├── Apple_Scab/
│   ├── image1.jpg
│   └── ...
├── Corn_Healthy/
│   ├── image1.jpg
│   └── ...
├── Corn_Cercospora_Leaf_Spot/
│   ├── image1.jpg
│   └── ...
├── Grape_Black_Rot/
│   ├── image1.jpg
│   └── ...
├── Tomato_Early_Blight/
│   ├── image1.jpg
│   └── ...
└── ... (39 total disease folders)
```

**Total**: 39 disease classes, ~55,000 images

---

## Step-by-Step Setup

### Step 1: Download Dataset
```bash
# Visit: https://github.com/spMohanty/PlantVillage-Dataset
# Click: Code → Download ZIP
# Wait for download (~3-4 GB)
```

### Step 2: Extract ZIP
```bash
# Extract the archive
# You'll get: PlantVillage-Dataset-master/
```

### Step 3: Locate Images
```bash
# Navigate to:
PlantVillage-Dataset-master/raw/color/

# This folder contains all 39 disease class folders
```

### Step 4: Copy to Project
```bash
# Copy the disease folders to your project:

# Windows:
cd PlantVillage-Dataset-master/raw/color
copy * "C:\Users\tayya\Desktop\machine learning project\data\raw\"

# Mac/Linux:
cp -r PlantVillage-Dataset-master/raw/color/* data/raw/
```

### Step 5: Verify Structure
```bash
# Check the structure
dir data/raw
# Should show 39 folders

# Count images in a folder
dir data/raw/Apple_Healthy
# Should show ~200+ JPG files
```

### Step 6: Start Training
```bash
cd models
python train_model.py
```

**Expected Output**:
```
Found 39 disease classes: ['Apple_Healthy', 'Apple_Scab', 'Apple_Black_Rot', ...]
Class 'Apple_Healthy': 247 images
Class 'Apple_Scab': 852 images
...
Total dataset size: 55448 samples
Feature dimension: 137

Training Random Forest Classifier...
Random Forest Results:
  Accuracy:  0.9562
  Precision: 0.9541
  Recall:    0.9562
  F1-Score:  0.9541
  
... (SVM and XGBoost results)

Best Model: XGBoost
Model saved to trained_model.pkl
```

---

## Dataset Variants

The PlantVillage dataset has different versions:

### 1. **Color Images** (Recommended) ✅
- `raw/color/`
- 256×256 pixels
- Full color (RGB)
- Size: ~4 GB
- **USE THIS ONE**

### 2. **Grayscale Images**
- `raw/grayscale/`
- 256×256 pixels
- Black and white
- Size: ~1.5 GB
- Good for texture analysis

### 3. **Segmented Images**
- `raw/segmented/`
- 256×256 pixels
- Leaf isolated from background
- Size: ~2 GB
- Great for leaf-focused analysis

---

## Expected Results with PlantVillage

### Accuracy Metrics
```
Random Forest:  92-95% accuracy
SVM:           89-92% accuracy
XGBoost:       94-97% accuracy (usually best)
```

### Training Time
```
- Feature Extraction:  2-5 minutes
- Random Forest:       3-5 minutes
- SVM:                 5-10 minutes
- XGBoost:            3-5 minutes
- Total:              15-25 minutes
```

### System Requirements
```
- RAM:        8GB minimum (16GB recommended)
- Disk:       10GB (4GB for dataset + 2GB for models)
- CPU:        Multi-core recommended
- GPU:        Not required (but speeds up if available)
```

---

## Citation

If you use this dataset in your project, cite it as:

```
Mohanty, S. P., Hughes, D. P., & Salathé, M. (2016).
"Using Deep Convolutional Networks for Image-Based Plant Disease Detection."
Frontiers in Plant Science, 7, 1419.

Dataset: https://github.com/spMohanty/PlantVillage-Dataset
```

---

## Quick Checklist

Before training:

- [ ] PlantVillage dataset downloaded
- [ ] ZIP file extracted
- [ ] 39 disease folders in `data/raw/`
- [ ] Each folder contains JPG images
- [ ] Total ~55,000 images
- [ ] Python packages installed
- [ ] Enough disk space (10GB)
- [ ] Enough RAM (8GB+)

---

## Troubleshooting

### Issue: Download is too slow

**Solution**:
1. Try different internet connection
2. Download at night (less congestion)
3. Use download manager (IDM, Aria2c)
4. Try Kaggle mirror

### Issue: ZIP file is corrupted

**Solution**:
```bash
# Re-download the file
# Verify checksum if available
# Try extracting with 7-Zip instead
```

### Issue: Disk space not enough

**Solution**:
```
Option 1: Use segmented images (smaller, 2GB)
Option 2: Use only subset of diseases
Option 3: Delete after training (keep model only)
Option 4: Upgrade storage
```

### Issue: Training takes too long

**Solution**:
1. Use Random Forest instead (faster)
2. Reduce image count (use subset)
3. Upgrade CPU/RAM
4. Use GPU acceleration

### Issue: Low accuracy

**Solution with PlantVillage**:
- Model should get 92%+ accuracy
- If lower, check:
  1. All 55,000 images present
  2. No corrupted images
  3. Python packages updated
  4. No interruptions during training

---

## File Sizes Reference

For planning your storage:

```
Dataset Size:           ~4 GB
Extracted Size:         ~8 GB
Model Files:            ~200 MB
Working Space Needed:   ~2 GB
Total Recommended:      ~15 GB free
```

---

## Next Steps

1. ✅ Download PlantVillage dataset
2. ✅ Extract to `data/raw/`
3. ✅ Verify 39 disease folders
4. ✅ Run `python train_model.py`
5. ✅ Start Flask backend
6. ✅ Test in browser

---

## Performance Tips

### For Faster Training
```python
# Use only top 10 diseases (faster)
# Reduces training time from 20 min to 5 min
```

### For Better Accuracy
```python
# Use all 39 diseases (slower but more accurate)
# Accuracy: 94-97%
```

### For Testing
```python
# Use subset: Apple, Tomato, Grape diseases
# Quick test before full training
```

---

## Support

For PlantVillage dataset issues:
- GitHub Issues: https://github.com/spMohanty/PlantVillage-Dataset/issues
- Citation paper: https://www.frontiersin.org/articles/10.3389/fpls.2016.01419

For your project issues:
- See SETUP_GUIDE.md
- See README.md

---

**Ready to download and train? Let's go! 🚀**

**Estimated Time**: 30-45 minutes (download + extract + organize)
