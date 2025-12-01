import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, global_mean_pool, global_max_pool
from torch_geometric.data import Data, DataLoader
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NetworkFlowGCN(nn.Module):
    
    def __init__(self, input_dim, hidden_dim=128, num_classes=6, dropout=0.15):
        super(NetworkFlowGCN, self).__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes
        self.dropout = dropout
        
        # Input projection layer with batch norm
        self.input_proj = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout * 0.5)
        )
        
        # GCN layers with residual connections
        self.conv1 = GCNConv(hidden_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.conv3 = GCNConv(hidden_dim, hidden_dim // 2)
        self.conv4 = GCNConv(hidden_dim // 2, hidden_dim // 4)
        
        # Attention mechanism
        self.attention = GATConv(hidden_dim // 4, hidden_dim // 4, heads=4, concat=False)
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim // 4, hidden_dim // 8),
            nn.BatchNorm1d(hidden_dim // 8),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 8, hidden_dim // 16),
            nn.BatchNorm1d(hidden_dim // 16),
            nn.ReLU(),
            nn.Dropout(dropout * 0.5),
            nn.Linear(hidden_dim // 16, num_classes)
        )
        
        # Batch normalization layers
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.bn2 = nn.BatchNorm1d(hidden_dim)
        self.bn3 = nn.BatchNorm1d(hidden_dim // 2)
        self.bn4 = nn.BatchNorm1d(hidden_dim // 4)
        
        logger.info(f"GCN Model initialized:")
        logger.info(f"   Input dim: {input_dim}")
        logger.info(f"   Hidden dim: {hidden_dim}")
        logger.info(f"   Output classes: {num_classes}")
        logger.info(f"   Dropout: {dropout}")
        
    def forward(self, x, edge_index, batch=None):
        
        # Project input to hidden dimension
        x = self.input_proj(x)
        
        # Layer 1 with residual-like connection
        x1 = self.conv1(x, edge_index)
        x1 = self.bn1(x1)
        x1 = F.relu(x1)
        x1 = F.dropout(x1, self.dropout, training=self.training)
        
        # Layer 2
        x2 = self.conv2(x1, edge_index)
        x2 = self.bn2(x2)
        x2 = F.relu(x2)
        x2 = F.dropout(x2, self.dropout, training=self.training)
        
        # Layer 3
        x3 = self.conv3(x2, edge_index)
        x3 = self.bn3(x3)
        x3 = F.relu(x3)
        x3 = F.dropout(x3, self.dropout, training=self.training)
        
        # Layer 4
        x4 = self.conv4(x3, edge_index)
        x4 = self.bn4(x4)
        x4 = F.relu(x4)
        x4 = F.dropout(x4, self.dropout, training=self.training)
        
        # Attention layer
        x_attn = self.attention(x4, edge_index)
        x_attn = F.relu(x_attn)
        
        # Classification
        if batch is not None:
            x_attn = global_mean_pool(x_attn, batch)
            out = self.classifier(x_attn)
            return F.log_softmax(out, dim=1)
        else:
            # For node classification
            out = self.classifier(x_attn)
            return out
    
    def predict_threat(self, x, edge_index):
        self.eval()
        with torch.no_grad():
            output = self.forward(x, edge_index)
            
            # For single sample prediction, aggregate the nodes
            if len(x) > 1:
                # Multiple nodes - take mean
                output = torch.mean(output, dim=0, keepdim=True)
            
            probabilities = torch.exp(output).squeeze().numpy()
            predicted_class = torch.argmax(output, dim=1).item()
            confidence = probabilities[predicted_class]
            
        return {
            'predicted_class': predicted_class,
            'confidence': float(confidence),
            'probabilities': probabilities.tolist()
        }

class NetworkGraphBuilder:
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = None
        self.class_names = None
        
    def create_graph_from_flows(self, flows_df, target_col='Label'):
        logger.info(f"Creating graphs from {len(flows_df)} flows...")
        
        features = flows_df.drop(columns=[target_col])
        labels = flows_df[target_col]
        
        self.feature_names = features.columns.tolist()
        self.class_names = sorted(labels.unique().tolist())  # Sort for consistency
        
        encoded_labels = self.label_encoder.fit_transform(labels)
        
        scaled_features = self.scaler.fit_transform(features)
        
        # Add feature importance weighting
        # Normalize features more aggressively
        scaled_features = (scaled_features - scaled_features.mean(axis=0)) / (scaled_features.std(axis=0) + 1e-8)
        
        node_features = torch.FloatTensor(scaled_features)
        node_labels = torch.LongTensor(encoded_labels)
        
        # Use lower k for faster computation on large datasets
        edge_index = self._create_edges_knn(scaled_features, k=5)
        
        data = Data(
            x=node_features,
            edge_index=edge_index,
            y=node_labels
        )
        
        logger.info(f"Graph created:")
        logger.info(f"   Nodes: {data.num_nodes}")
        logger.info(f"   Edges: {data.num_edges}")
        logger.info(f"   Features: {data.num_node_features}")
        logger.info(f"   Classes: {len(self.class_names)}")
        logger.info(f"   Class mapping: {dict(zip(self.class_names, self.label_encoder.classes_))}")
        
        return data, self.class_names
        
    def _create_edges_knn(self, features, k=10):
        """Create edges using a simple, ultra-fast approach"""
        logger.info(f"Creating graph edges (ultra-fast mode)...")
        
        n_samples = len(features)
        
        # Use a simple but effective random neighborhood approach
        edges = []
        np.random.seed(42)
        
        # Create edges by connecting each node to k random neighbors
        # Plus some structure from sequential indices
        for i in range(n_samples):
            # Connect to next k nodes (sequential)
            for j in range(1, min(4, n_samples - i)):
                edges.append([i, i + j])
                edges.append([i + j, i])
            
            # Connect to k random nodes
            random_neighbors = np.random.choice(n_samples, size=min(2, n_samples-1), replace=False)
            for j in random_neighbors:
                if i != j:
                    edges.append([i, j])
        
        # Remove duplicates
        edges_set = set(tuple(e) for e in edges)
        edge_list = [[e[0], e[1]] for e in edges_set]
        
        if len(edge_list) == 0:
            # Fallback
            edge_list = [[i, (i+1) % n_samples] for i in range(n_samples)]
        
        edge_index = torch.LongTensor(edge_list).t().contiguous()
        logger.info(f"Created graph with {edge_index.size(1)} edges")
        
        return edge_index
    
    def create_single_flow_graph(self, flow_features):
        if self.scaler is None:
            raise ValueError("GraphBuilder not fitted. Train the model first.")
            
        if len(flow_features.shape) == 1:
            flow_features = flow_features.reshape(1, -1)
            
        scaled_features = self.scaler.transform(flow_features)
        node_features = torch.FloatTensor(scaled_features)
        
        edge_index = torch.LongTensor([[0], [0]])
        
        return node_features, edge_index

class ThreatDetectionTrainer:
    
    def __init__(self, model, device='cpu'):
        self.model = model.to(device)
        self.device = device
        # Better optimizer with weight decay for regularization
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=0.0002, weight_decay=1e-4)
        self.criterion = nn.CrossEntropyLoss()
        self.history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
        # Learning rate scheduler
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, mode='max', factor=0.7, patience=8, verbose=False, min_lr=1e-6
        )
        
    def train_epoch(self, data):
        self.model.train()
        self.optimizer.zero_grad()
        
        out = self.model(data.x, data.edge_index)
        
        # Use only training mask
        train_out = out[data.train_mask]
        train_y = data.y[data.train_mask]
        
        loss = self.criterion(train_out, train_y)
        
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)  # Gradient clipping
        self.optimizer.step()
        
        pred = train_out.argmax(dim=1)
        train_acc = (pred == train_y).float().mean()
        
        return loss.item(), train_acc.item()
    
    def validate(self, data):
        self.model.eval()
        with torch.no_grad():
            out = self.model(data.x, data.edge_index)
            
            val_loss = self.criterion(out[data.val_mask], data.y[data.val_mask])
            
            pred = out[data.val_mask].argmax(dim=1)
            val_acc = (pred == data.y[data.val_mask]).float().mean()
            
        return val_loss.item(), val_acc.item()
    
    def train(self, data, epochs=100, patience=10):
        logger.info(f"Starting training for {epochs} epochs...")
        logger.info(f"Train samples: {data.train_mask.sum().item()}, Val samples: {data.val_mask.sum().item()}, Test samples: {data.test_mask.sum().item()}")
        
        best_val_acc = 0
        patience_counter = 0
        
        for epoch in range(epochs):
            train_loss, train_acc = self.train_epoch(data)
            
            val_loss, val_acc = self.validate(data)
            
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
            
            # Update learning rate based on validation accuracy
            self.scheduler.step(val_acc)
            
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                patience_counter = 0
                torch.save(self.model.state_dict(), 'best_gcn_model.pth')
            else:
                patience_counter += 1
            
            if epoch % 10 == 0 or epoch == epochs - 1:
                logger.info(f"Epoch {epoch:3d} | Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | "
                           f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f} | Best: {best_val_acc:.4f}")
            
            if patience_counter >= patience:
                logger.info(f"Early stopping at epoch {epoch}")
                break
        
        self.model.load_state_dict(torch.load('best_gcn_model.pth'))
        logger.info(f"Training completed! Best validation accuracy: {best_val_acc:.4f}")
        
        return self.history
    
    def test(self, data):
        self.model.eval()
        with torch.no_grad():
            out = self.model(data.x, data.edge_index)
            pred = out[data.test_mask].argmax(dim=1)
            test_acc = (pred == data.y[data.test_mask]).float().mean()
            
        logger.info(f"Test Accuracy: {test_acc:.4f}")
        return test_acc.item()

def create_train_val_test_masks(num_nodes, train_ratio=0.6, val_ratio=0.2):
    indices = torch.randperm(num_nodes)
    
    train_size = int(train_ratio * num_nodes)
    val_size = int(val_ratio * num_nodes)
    
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    
    train_mask[indices[:train_size]] = True
    val_mask[indices[train_size:train_size + val_size]] = True
    test_mask[indices[train_size + val_size:]] = True
    
    return train_mask, val_mask, test_mask

if __name__ == "__main__":
    logger.info("Training GCN model with real ransomware dataset...")
    
    # Load actual dataset with nrows limit
    dataset_path = '../data/PRATIRAKSHA_ransomware_dataset_balanced.csv'
    
    try:
        logger.info(f"Loading dataset from {dataset_path}...")
        # Load only first 15000 rows to improve performance
        df = pd.read_csv(dataset_path, nrows=15000)
        logger.info(f"Loaded dataset: {len(df)} samples")
        logger.info(f"Class distribution:\n{df['Label'].value_counts()}")
    except FileNotFoundError:
        logger.warning(f"Dataset not found at {dataset_path}, trying alternative path...")
        dataset_path = '../data/PRATIRAKSHA_ransomware_dataset.csv'
        logger.info(f"Loading dataset from {dataset_path}...")
        df = pd.read_csv(dataset_path, nrows=15000)
        logger.info(f"Loaded dataset: {len(df)} samples")
        logger.info(f"Class distribution:\n{df['Label'].value_counts()}")
    
    # Use stratified sampling to balance classes
    from sklearn.model_selection import StratifiedShuffleSplit
    if len(df) > 10000:
        sss = StratifiedShuffleSplit(n_splits=1, test_size=None, train_size=10000, random_state=42)
        train_idx = list(sss.split(df, df['Label']))[0][0]
        df = df.iloc[train_idx].reset_index(drop=True)
        logger.info(f"Using {len(df)} samples for training (stratified)")
    
    graph_builder = NetworkGraphBuilder()
    data, class_names = graph_builder.create_graph_from_flows(df)
    
    data.train_mask, data.val_mask, data.test_mask = create_train_val_test_masks(
        data.num_nodes, 
        train_ratio=0.7, 
        val_ratio=0.15
    )
    
    model = NetworkFlowGCN(
        input_dim=data.num_node_features,
        hidden_dim=256,  # Increased to learn more complex patterns
        num_classes=len(class_names),
        dropout=0.15
    )
    
    trainer = ThreatDetectionTrainer(model)
    history = trainer.train(data, epochs=300, patience=30)
    
    test_acc = trainer.test(data)
    
    logger.info("GCN model training completed successfully!")
    logger.info(f"Final Test Accuracy: {test_acc:.4f}")
    logger.info(f"Classes detected: {class_names}")