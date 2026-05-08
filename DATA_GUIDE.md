# 📊 Data Preparation Guide

## Overview

This guide explains how to prepare and organize your plant leaf disease dataset for training the ML model.

## Dataset Requirements

### Minimum Requirements
- **Minimum classes**: 2 disease types
- **Minimum images per class**: 50 images
- **Image formats**: JPG, PNG, GIF, BMP
- **Image size**: 100x100 to 2000x2000 pixels (will be resized to 128x128)
- **Total dataset**: 300+ images recommended

### Recommended Requirements
- **Classes**: 5-10 disease types
- **Images per class**: 200-500 images
- **Total dataset**: 1000-5000 images
- **Image quality**: Clear, well-lit, focused
- **Class balance**: Equal distribution across classes

## Directory Structure

### Correct Structure ✅

```
data/raw/
├── Healthy/
│   ├── healthy_leaf_001.jpg
│   ├── healthy_leaf_002.jpg
│   ├── healthy_leaf_003.jpg
│   └── ...
├── Leaf_Spot/
│   ├── leaf_spot_001.jpg
│   ├── leaf_spot_002.jpg
│   └── ...
├── Powdery_Mildew/
│   ├── powdery_mildew_001.jpg
│   └── ...
└── Early_Blight/
    ├── early_blight_001.jpg
    └── ...
```

### Important Notes

1. **Folder names** = Disease class names
   - These will appear in predictions
   - Use clear, descriptive names
   - Avoid special characters
   - Use underscores for spaces (e.g., `Leaf_Spot`)

2. **File naming** is flexible
   - Can be anything: `image1.jpg`, `disease_001.png`, etc.
   - Must have valid image extension
   - Special characters should be avoided

3. **No subfolders** inside disease folders
   - Keep images flat in each folder
   - Don't create additional levels

## Popular Datasets

### PlantVillage Dataset (Recommended)
- **Size**: 55,000+ images
- **Classes**: 14 diseases + healthy
- **Source**: https://github.com/spMohanty/PlantVillage-Dataset
- **License**: Open access
- **Setup Time**: 30 minutes (download + organize)

**Steps**:
```
1. Visit: https://github.com/spMohanty/PlantVillage-Dataset
2. Click "Code" → Download ZIP
3. Extract the archive
4. Copy disease folders to: data/raw/
5. Verify structure matches format above
```

### Kaggle Plant Disease Dataset
- **Size**: Varies (1000-50000 images)
- **Classes**: 2-15 diseases
- **Source**: https://www.kaggle.com/
- **License**: Check individual dataset

**Steps**:
```
1. Create Kaggle account
2. Search: "plant disease" or specific crop
3. Download dataset
4. Organize into data/raw/
```

### DIY Dataset (Your Images)
- **Size**: Custom
- **Time**: 1-4 hours collection
- **Quality**: Potentially higher for your crops

**Collection Tips**:
- Take photos in natural sunlight
- Include diseased and healthy leaves
- Photograph from multiple angles
- Focus clearly on affected areas
- Use phone camera or DSLR
- Include reference objects for scale

## Data Organization Steps

### Step 1: Create Main Folder
```bash
mkdir data/raw
```

### Step 2: Create Disease Subfolders
```bash
mkdir data/raw/Healthy
mkdir data/raw/Leaf_Spot
mkdir data/raw/Powdery_Mildew
mkdir data/raw/Rust
mkdir data/raw/Blight
```

### Step 3: Add Images
- Copy/move images to appropriate disease folder
- Verify folder has at least 50 images each

### Step 4: Verify Structure
```bash
# Windows:
dir data/raw
dir data/raw/Healthy

# Mac/Linux:
ls data/raw
ls data/raw/Healthy
```

Should show disease folders and images inside.

## Data Quality Checks

### Before Training

✅ **Check 1**: File Format
```bash
# All images should be .jpg, .png, .gif, or .bmp
# No corrupted files
# No subdirectories within disease folders
```

✅ **Check 2**: Image Quality
```
- Clear and focused
- Good lighting (not too dark)
- Leaf clearly visible
- Affected area visible (for diseased images)
- No watermarks or excessive text
```

✅ **Check 3**: File Count
```python
# Count images per class
# Healthy: 250 images ✅
# Leaf_Spot: 248 images ✅
# Powdery_Mildew: 240 images ✅
# Total: 738 images ✅
```

✅ **Check 4**: Naming
```
# All images have valid extensions
# disease_folder_001.jpg ✅
# image#1.png ✅
# scan (1).jpg ✅
# NOT: image.txt ❌, photo ❌
```

### Runtime Checks

The training script will:
1. Verify folder structure
2. Check for valid image files
3. Count images per class
4. Show warnings for issues
5. Skip corrupted files

## Handling Data Issues

### Problem: Not Enough Images

**Solution**:
```
1. Download more images from Kaggle
2. Use online image sources
3. Collect your own images
4. Use data augmentation (rotation, flip, crop)
```

**Data Augmentation Script** (Optional):
```python
from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    fill_mode='nearest'
)

# Generate augmented images
for X, y in datagen.flow_from_directory(...):
    # Save augmented images
    break
```

### Problem: Unbalanced Classes

**Example**:
```
Healthy: 500 images ← Too many
Leaf_Spot: 50 images ← Too few
Powdery_Mildew: 300 images ← Too many
```

**Solution**:
1. Randomly sample 100-150 from each class
2. Collect more images for underrepresented classes
3. Use class weighting in model (automatically done)

### Problem: Low Quality Images

**Identify**:
```
- Blurry photos
- Too dark/bright
- Leaf not visible
- Wrong object in image
```

**Solution**:
1. Delete problematic images manually
2. Re-collect better quality images
3. Clean dataset script (see below)

### Problem: Wrong Disease Classification

**Identify**:
```
Image in Leaf_Spot folder but shows Powdery_Mildew
```

**Solution**:
1. Move image to correct folder
2. Delete if unsure
3. Verify dataset source credibility

## Optional: Dataset Cleaning Script

Create `clean_dataset.py`:

```python
import os
import cv2
import shutil

def validate_images(data_dir):
    """Check all images for issues"""
    issues = []
    
    for disease in os.listdir(data_dir):
        disease_path = os.path.join(data_dir, disease)
        
        if not os.path.isdir(disease_path):
            continue
        
        for img_file in os.listdir(disease_path):
            img_path = os.path.join(disease_path, img_file)
            
            try:
                # Check if valid image
                img = cv2.imread(img_path)
                if img is None:
                    issues.append(f"Invalid image: {img_path}")
                    continue
                
                # Check image size
                if img.shape[0] < 50 or img.shape[1] < 50:
                    issues.append(f"Too small: {img_path}")
                
            except Exception as e:
                issues.append(f"Error reading {img_path}: {e}")
    
    return issues

# Run validation
data_dir = "data/raw"
issues = validate_images(data_dir)

print(f"Found {len(issues)} issues:")
for issue in issues:
    print(f"  - {issue}")
```

Run it:
```bash
python clean_dataset.py
```

## Pre-Training Checklist

Before running `train_model.py`, verify:

- [ ] `data/raw/` folder exists
- [ ] At least 2-3 disease subfolders
- [ ] Each folder has 50+ images
- [ ] Images are JPG/PNG format
- [ ] No corrupted files
- [ ] Folder structure is correct
- [ ] Images are named properly
- [ ] Enough disk space (5GB+)
- [ ] Python packages installed

## Example: Quick Start with Minimal Dataset

### Create test dataset (500 images):

1. **Download**:
   - 100 healthy leaf images
   - 100 leaf spot images
   - 100 powdery mildew images
   - 100 rust images
   - 100 blight images

2. **Organize**:
   ```
   data/raw/
   ├── Healthy/ (100 images)
   ├── Leaf_Spot/ (100 images)
   ├── Powdery_Mildew/ (100 images)
   ├── Rust/ (100 images)
   └── Blight/ (100 images)
   ```

3. **Train**:
   ```bash
   python models/train_model.py
   ```
   **Time**: ~5 minutes on average computer

4. **Results**: Expect 70-80% accuracy with small dataset

## Scaling Up

### For Better Model

**Increase dataset**:
- 1000 images: ~85% accuracy
- 2000 images: ~90% accuracy
- 5000+ images: ~95%+ accuracy

**Each class should have**:
```
Minimum: 50 images
Good: 200-300 images
Excellent: 500+ images
```

### Progressive Training

1. **Phase 1**: Train with 100-300 images (test pipeline)
2. **Phase 2**: Add more diverse images (300-1000)
3. **Phase 3**: Large-scale training (1000-5000+)

## Summary

| Item | Minimum | Recommended |
|------|---------|------------|
| Total Images | 300 | 1000+ |
| Classes | 2 | 5-10 |
| Per Class | 50 | 200-500 |
| Format | JPG/PNG | JPG/PNG |
| Size | Any | 128x128 to 1024x1024 |
| Quality | Medium | High |
| Balance | Any | Equal |
| Training Time | 2-5 min | 10-30 min |
| Expected Accuracy | 60-70% | 85-95% |

---

**Next**: Run `python models/train_model.py` after data is ready!
