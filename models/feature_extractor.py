"""
Feature Extraction Module
Extract visual features from plant leaf images for classification
"""

import cv2
import numpy as np
from skimage.feature import local_binary_pattern
from skimage import color
import warnings
warnings.filterwarnings('ignore')


class LeafFeatureExtractor:
    """Extract features from leaf images"""
    
    def __init__(self, image_size=(128, 128)):
        self.image_size = image_size
        
    def extract_color_histogram(self, image, bins=32):
        """Extract color histogram features (HSV space)"""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        hist_h = cv2.calcHist([hsv], [0], None, [bins], [0, 180])
        hist_s = cv2.calcHist([hsv], [1], None, [bins], [0, 256])
        hist_v = cv2.calcHist([hsv], [2], None, [bins], [0, 256])
        
        # Normalize and flatten
        hist_h = cv2.normalize(hist_h, hist_h).flatten()
        hist_s = cv2.normalize(hist_s, hist_s).flatten()
        hist_v = cv2.normalize(hist_v, hist_v).flatten()
        
        return np.concatenate([hist_h, hist_s, hist_v])
    
    def extract_texture_features(self, image, radius=3, points=24):
        """Extract Local Binary Pattern (LBP) texture features"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Calculate LBP
        lbp = local_binary_pattern(gray, points, radius, method='uniform')
        
        # Create histogram of LBP
        hist, _ = np.histogram(lbp, bins=np.arange(0, points + 3), range=(0, points + 2))
        hist = hist.astype(float) / hist.sum()
        
        return hist
    
    def extract_color_moments(self, image):
        """Extract color moments (mean, variance, skewness)"""
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        features = []
        for channel in cv2.split(image):
            mean = np.mean(channel)
            variance = np.var(channel)
            skewness = np.mean((channel - mean) ** 3) / (np.std(channel) ** 3 + 1e-6)
            features.extend([mean, variance, skewness])
        
        return np.array(features)
    
    def extract_edge_features(self, image):
        """Extract edge-based features"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Canny edge detection
        edges = cv2.Canny(gray, 100, 200)
        
        # Edge density
        edge_density = np.sum(edges > 0) / edges.size
        
        # Contours
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        num_contours = len(contours)
        
        return np.array([edge_density, num_contours])
    
    def extract_shape_features(self, image):
        """Extract shape-based features"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        features = []
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            circularity = 4 * np.pi * area / (perimeter ** 2 + 1e-6)
            
            features = [area, perimeter, circularity]
        else:
            features = [0, 0, 0]
        
        return np.array(features)
    
    def preprocess_image(self, image_path):
        """Load and preprocess image"""
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Resize
        image = cv2.resize(image, self.image_size)
        
        return image
    
    def extract_all_features(self, image_path):
        """Extract all features from an image"""
        image = self.preprocess_image(image_path)
        
        features = {}
        features['color_hist'] = self.extract_color_histogram(image)
        features['texture'] = self.extract_texture_features(image)
        features['color_moments'] = self.extract_color_moments(image)
        features['edge'] = self.extract_edge_features(image)
        features['shape'] = self.extract_shape_features(image)
        
        # Concatenate all features
        all_features = np.concatenate([
            features['color_hist'],
            features['texture'],
            features['color_moments'],
            features['edge'],
            features['shape']
        ])
        
        return all_features, features
    
    def extract_all_features_direct(self, image):
        """Extract all features directly from a loaded image array"""
        features = {}
        features['color_hist'] = self.extract_color_histogram(image)
        features['texture'] = self.extract_texture_features(image)
        features['color_moments'] = self.extract_color_moments(image)
        features['edge'] = self.extract_edge_features(image)
        features['shape'] = self.extract_shape_features(image)
        
        # Concatenate all features
        all_features = np.concatenate([
            features['color_hist'],
            features['texture'],
            features['color_moments'],
            features['edge'],
            features['shape']
        ])
        
        return all_features, features


def extract_batch_features(image_paths, image_size=(128, 128)):
    """Extract features from multiple images"""
    extractor = LeafFeatureExtractor(image_size=image_size)
    features_list = []
    
    for img_path in image_paths:
        try:
            features, _ = extractor.extract_all_features(img_path)
            features_list.append(features)
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            continue
    
    return np.array(features_list)
