"""
Model Training Script
Train and evaluate plant leaf disease classification models
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, confusion_matrix, classification_report)
import xgboost as xgb
from feature_extractor import extract_batch_features
import warnings
warnings.filterwarnings('ignore')


class ModelTrainer:
    """Train and evaluate ML models for leaf disease classification"""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.best_model = None
        self.best_model_name = None
        
    def load_data(self, data_dir, train_split=0.7, val_split=0.15, test_split=0.15):
        """Load images and labels from directory structure"""
        X = []
        y = []
        
        # Assuming data_dir contains subdirectories for each disease class
        classes = sorted([d for d in os.listdir(data_dir) 
                         if os.path.isdir(os.path.join(data_dir, d))])
        
        print(f"Found {len(classes)} disease classes: {classes}")
        
        for class_name in classes:
            class_dir = os.path.join(data_dir, class_name)
            image_files = [f for f in os.listdir(class_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            print(f"Class '{class_name}': {len(image_files)} images")
            
            image_paths = [os.path.join(class_dir, f) for f in image_files]
            features = extract_batch_features(image_paths)
            
            X.extend(features)
            y.extend([class_name] * len(features))
        
        X = np.array(X)
        y = np.array(y)
        
        print(f"\nTotal dataset size: {len(X)} samples")
        print(f"Feature dimension: {X.shape[1]}")
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y_encoded, test_size=(1-train_split), 
            random_state=self.random_state, stratify=y_encoded
        )
        
        val_size = val_split / (val_split + test_split)
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=1-val_size, 
            random_state=self.random_state, stratify=y_temp
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        return (X_train_scaled, X_val_scaled, X_test_scaled,
                y_train, y_val, y_test)
    
    def train_random_forest(self, X_train, y_train):
        """Train Random Forest classifier"""
        print("\n" + "="*50)
        print("Training Random Forest Classifier...")
        print("="*50)
        
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=self.random_state,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        self.models['Random Forest'] = model
        
        return model
    
    def train_svm(self, X_train, y_train):
        """Train Support Vector Machine classifier"""
        print("\n" + "="*50)
        print("Training SVM Classifier...")
        print("="*50)
        
        model = SVC(
            kernel='rbf',
            C=10,
            gamma='scale',
            probability=True,
            random_state=self.random_state
        )
        
        model.fit(X_train, y_train)
        self.models['SVM'] = model
        
        return model
    
    def train_xgboost(self, X_train, y_train):
        """Train XGBoost classifier"""
        print("\n" + "="*50)
        print("Training XGBoost Classifier...")
        print("="*50)
        
        model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=self.random_state,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        self.models['XGBoost'] = model
        
        return model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        print(f"\n{model_name} Results:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        
        print(f"\nClassification Report for {model_name}:")
        print(classification_report(y_test, y_pred, 
                                   target_names=self.label_encoder.classes_))
        
        return {
            'model': model_name,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
    
    def train_all_models(self, X_train, y_train, X_test, y_test):
        """Train and evaluate all models"""
        results = []
        
        # Random Forest
        rf_model = self.train_random_forest(X_train, y_train)
        rf_results = self.evaluate_model(rf_model, X_test, y_test, "Random Forest")
        results.append(rf_results)
        
        # SVM
        svm_model = self.train_svm(X_train, y_train)
        svm_results = self.evaluate_model(svm_model, X_test, y_test, "SVM")
        results.append(svm_results)
        
        # XGBoost
        xgb_model = self.train_xgboost(X_train, y_train)
        xgb_results = self.evaluate_model(xgb_model, X_test, y_test, "XGBoost")
        results.append(xgb_results)
        
        # Select best model
        results_df = pd.DataFrame(results)
        best_idx = results_df['f1_score'].idxmax()
        self.best_model_name = results_df.loc[best_idx, 'model']
        self.best_model = self.models[self.best_model_name]
        
        print("\n" + "="*50)
        print(f"Best Model: {self.best_model_name}")
        print("="*50)
        
        return results_df
    
    def save_model(self, model_path, scaler_path, encoder_path):
        """Save trained model and preprocessing objects"""
        if self.best_model is None:
            raise ValueError("No model trained yet!")
        
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.best_model, f)
        
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        print(f"\nModel saved to {model_path}")
        print(f"Scaler saved to {scaler_path}")
        print(f"Encoder saved to {encoder_path}")


def main():
    """Main training pipeline"""
    
    # Configuration
    data_dir = "data/raw"  # Directory with disease folders
    model_path = "models/trained_model.pkl"
    scaler_path = "models/scaler.pkl"
    encoder_path = "models/label_encoder.pkl"
    
    # Check if data exists
    if not os.path.exists(data_dir) or len(os.listdir(data_dir)) == 0:
        print("ERROR: Data directory is empty!")
        print(f"Please add disease subdirectories to: {data_dir}")
        print("Expected structure:")
        print(f"  {data_dir}/")
        print("    disease1/")
        print("      image1.jpg")
        print("      image2.jpg")
        print("    disease2/")
        print("      image1.jpg")
        return
    
    # Initialize trainer
    trainer = ModelTrainer(random_state=42)
    
    # Load and split data
    print("Loading data...")
    X_train, X_val, X_test, y_train, y_val, y_test = trainer.load_data(data_dir)
    
    print(f"\nData split:")
    print(f"  Training:   {len(X_train)} samples")
    print(f"  Validation: {len(X_val)} samples")
    print(f"  Testing:    {len(X_test)} samples")
    
    # Train models
    results_df = trainer.train_all_models(X_train, y_train, X_test, y_test)
    
    print("\n" + "="*50)
    print("Model Comparison Summary:")
    print("="*50)
    print(results_df.to_string(index=False))
    
    # Save best model
    trainer.save_model(model_path, scaler_path, encoder_path)


if __name__ == "__main__":
    main()
