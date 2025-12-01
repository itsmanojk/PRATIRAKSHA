"""
Final training script that trains the model and properly saves it for deployment
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, global_mean_pool
from torch_geometric.data import Data
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
import logging
import json
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the training classes from training_gcn_model
import sys
sys.path.insert(0, os.path.dirname(__file__))
from training_gcn_model import (
    NetworkFlowGCN, 
    NetworkGraphBuilder, 
    ThreatDetectionTrainer,
    create_train_val_test_masks
)

def train_final_model():
    """Train the model and save it with metadata"""
    
    logger.info("="*60)
    logger.info("PRATIRAKSHA FINAL MODEL TRAINING & DEPLOYMENT")
    logger.info("="*60)
    
    # Load dataset in chunks to avoid memory issues
    dataset_path = '../data/PRATIRAKSHA_ransomware_dataset_balanced.csv'
    try:
        logger.info("Loading dataset in chunks...")
        chunks = []
        for chunk in pd.read_csv(dataset_path, chunksize=5000):
            chunks.append(chunk)
            if len(chunks) >= 3:  # Load 15k samples
                break
        df = pd.concat(chunks, ignore_index=True)
        logger.info(f"✓ Loaded dataset: {len(df)} samples")
        logger.info(f"  Class distribution:\n{df['Label'].value_counts()}")
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        return False
    
    # Use stratified sampling
    from sklearn.model_selection import StratifiedShuffleSplit
    if len(df) > 10000:
        sss = StratifiedShuffleSplit(n_splits=1, test_size=None, train_size=10000, random_state=42)
        train_idx = list(sss.split(df, df['Label']))[0][0]
        df = df.iloc[train_idx].reset_index(drop=True)
        logger.info(f"✓ Using {len(df)} samples (stratified)")
    
    # Build graph
    graph_builder = NetworkGraphBuilder()
    data, class_names = graph_builder.create_graph_from_flows(df)
    
    data.train_mask, data.val_mask, data.test_mask = create_train_val_test_masks(
        data.num_nodes, train_ratio=0.7, val_ratio=0.15
    )
    
    # Create model
    model = NetworkFlowGCN(
        input_dim=data.num_node_features,
        hidden_dim=256,
        num_classes=len(class_names),
        dropout=0.15
    )
    
    # Train
    trainer = ThreatDetectionTrainer(model)
    logger.info(f"\n{'='*60}")
    logger.info("TRAINING PHASE")
    logger.info(f"{'='*60}")
    history = trainer.train(data, epochs=200, patience=25)
    
    # Test
    test_acc = trainer.test(data)
    
    # Save model
    model_save_path = 'models/trained_model.pth'
    torch.save(trainer.model.state_dict(), model_save_path)
    logger.info(f"\n✓ Model saved to {model_save_path}")
    
    # Save model metadata
    model_info = {
        "model_architecture": "Graph Convolutional Network with Attention",
        "parameter_count": sum(p.numel() for p in trainer.model.parameters()),
        "number_of_classes": len(class_names),
        "class_labels": sorted(class_names),
        "training_date": datetime.now().isoformat(),
        "accuracy_percentage": float(test_acc) * 100,
        "description": "GCN-based ransomware threat detector trained on balanced dataset",
        "hidden_dims": 256,
        "input_dims": data.num_node_features,
        "dropout": 0.15,
        "final_test_accuracy": float(test_acc),
        "best_val_accuracy": max(history['val_acc'])
    }
    
    model_info_path = 'models/model_info.json'
    with open(model_info_path, 'w') as f:
        json.dump(model_info, f, indent=2)
    logger.info(f"✓ Model metadata saved to {model_info_path}")
    
    # Print summary
    logger.info(f"\n{'='*60}")
    logger.info("TRAINING SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    logger.info(f"Best Validation Accuracy: {max(history['val_acc']):.4f}")
    logger.info(f"Classes: {sorted(class_names)}")
    logger.info(f"Model Parameters: {model_info['parameter_count']:,}")
    logger.info(f"✓ Model ready for deployment!")
    
    return True

if __name__ == "__main__":
    success = train_final_model()
    if success:
        logger.info("\n✓✓✓ TRAINING COMPLETED SUCCESSFULLY ✓✓✓")
    else:
        logger.error("\n✗✗✗ TRAINING FAILED ✗✗✗")
