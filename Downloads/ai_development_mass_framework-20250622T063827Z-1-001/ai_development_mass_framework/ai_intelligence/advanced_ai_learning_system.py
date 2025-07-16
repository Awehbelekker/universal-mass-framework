"""
Advanced AI Learning System for MASS Framework

This system provides continuous learning, model adaptation, and self-improvement
capabilities for all AI agents in the MASS Framework.
"""

import asyncio
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import pickle
from pathlib import Path
import hashlib
import threading
import queue
from dataclasses import dataclass
from enum import Enum

# Machine Learning imports
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import lightgbm as lgb

# Deep Learning imports
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

logger = logging.getLogger(__name__)

class LearningMode(Enum):
    SUPERVISED = "supervised"
    UNSUPERVISED = "unsupervised"
    REINFORCEMENT = "reinforcement"
    TRANSFER = "transfer"
    META = "meta"

@dataclass
class LearningTask:
    task_id: str
    agent_id: str
    task_type: str
    input_data: Dict[str, Any]
    expected_output: Optional[Dict[str, Any]]
    learning_mode: LearningMode
    priority: int = 1
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    performance_metrics: Dict[str, float] = None

class AdvancedAILearningSystem:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.learning_queue = queue.PriorityQueue()
        self.active_models = {}
        self.model_performance_history = {}
        self.learning_thread = None
        self.is_running = False
        
        # Initialize model storage
        self.model_storage_path = Path(config.get('model_storage_path', './models'))
        self.model_storage_path.mkdir(exist_ok=True)
        
        # Initialize learning components
        self.data_preprocessor = DataPreprocessor()
        self.model_trainer = ModelTrainer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.knowledge_distiller = KnowledgeDistiller()
        
        # Learning configuration
        self.learning_config = {
            'batch_size': config.get('batch_size', 32),
            'learning_rate': config.get('learning_rate', 0.001),
            'epochs': config.get('epochs', 100),
            'validation_split': config.get('validation_split', 0.2),
            'early_stopping_patience': config.get('early_stopping_patience', 10),
            'model_update_threshold': config.get('model_update_threshold', 0.05)
        }
    
    async def start(self):
        """Start the AI learning system"""
        try:
            self.is_running = True
            self.learning_thread = threading.Thread(target=self._learning_worker)
            self.learning_thread.start()
            logger.info("Advanced AI Learning System started")
        except Exception as e:
            logger.error(f"Failed to start AI learning system: {e}")
            raise
    
    async def stop(self):
        """Stop the AI learning system"""
        try:
            self.is_running = False
            if self.learning_thread:
                self.learning_thread.join()
            logger.info("Advanced AI Learning System stopped")
        except Exception as e:
            logger.error(f"Error stopping AI learning system: {e}")
    
    def add_learning_task(self, task: LearningTask):
        """Add a learning task to the queue"""
        try:
            task.created_at = datetime.utcnow()
            self.learning_queue.put((task.priority, task))
            logger.info(f"Added learning task {task.task_id} for agent {task.agent_id}")
        except Exception as e:
            logger.error(f"Error adding learning task: {e}")
    
    def _learning_worker(self):
        """Main learning worker thread"""
        while self.is_running:
            try:
                if not self.learning_queue.empty():
                    priority, task = self.learning_queue.get()
                    self._process_learning_task(task)
                else:
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Error in learning worker: {e}")
    
    def _process_learning_task(self, task: LearningTask):
        """Process a learning task"""
        try:
            logger.info(f"Processing learning task {task.task_id}")
            
            # Preprocess data
            processed_data = self.data_preprocessor.preprocess(task.input_data)
            
            # Train or update model
            if task.agent_id in self.active_models:
                model = self.active_models[task.agent_id]
                updated_model = self.model_trainer.update_model(
                    model, processed_data, task.expected_output, task.learning_mode
                )
            else:
                updated_model = self.model_trainer.train_new_model(
                    processed_data, task.expected_output, task.learning_mode
                )
            
            # Evaluate performance
            performance_metrics = self.performance_analyzer.evaluate_model(
                updated_model, processed_data, task.expected_output
            )
            
            # Update model if performance improved
            if self._should_update_model(task.agent_id, performance_metrics):
                self.active_models[task.agent_id] = updated_model
                self._save_model(task.agent_id, updated_model)
                self.model_performance_history[task.agent_id] = performance_metrics
            
            # Distill knowledge
            distilled_knowledge = self.knowledge_distiller.distill_knowledge(
                task.agent_id, updated_model, performance_metrics
            )
            
            # Mark task as completed
            task.completed_at = datetime.utcnow()
            task.performance_metrics = performance_metrics
            
            logger.info(f"Completed learning task {task.task_id} with performance: {performance_metrics}")
            
        except Exception as e:
            logger.error(f"Error processing learning task {task.task_id}: {e}")
    
    def _should_update_model(self, agent_id: str, new_metrics: Dict[str, float]) -> bool:
        """Determine if model should be updated based on performance"""
        if agent_id not in self.model_performance_history:
            return True
        
        old_metrics = self.model_performance_history[agent_id]
        improvement_threshold = self.learning_config['model_update_threshold']
        
        # Check if new model performs better
        for metric_name, new_value in new_metrics.items():
            if metric_name in old_metrics:
                old_value = old_metrics[metric_name]
                improvement = (new_value - old_value) / old_value
                if improvement > improvement_threshold:
                    return True
        
        return False
    
    def _save_model(self, agent_id: str, model: Any):
        """Save model to storage"""
        try:
            model_path = self.model_storage_path / f"{agent_id}_model.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            logger.info(f"Saved model for agent {agent_id}")
        except Exception as e:
            logger.error(f"Error saving model for agent {agent_id}: {e}")
    
    def load_model(self, agent_id: str) -> Optional[Any]:
        """Load model from storage"""
        try:
            model_path = self.model_storage_path / f"{agent_id}_model.pkl"
            if model_path.exists():
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                self.active_models[agent_id] = model
                logger.info(f"Loaded model for agent {agent_id}")
                return model
            return None
        except Exception as e:
            logger.error(f"Error loading model for agent {agent_id}: {e}")
            return None
    
    def get_model_performance(self, agent_id: str) -> Dict[str, float]:
        """Get performance metrics for a model"""
        return self.model_performance_history.get(agent_id, {})
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning system statistics"""
        return {
            'active_models': len(self.active_models),
            'queued_tasks': self.learning_queue.qsize(),
            'total_tasks_processed': len(self.model_performance_history),
            'average_performance': self._calculate_average_performance(),
            'learning_mode_distribution': self._get_learning_mode_distribution()
        }
    
    def _calculate_average_performance(self) -> Dict[str, float]:
        """Calculate average performance across all models"""
        if not self.model_performance_history:
            return {}
        
        metrics = {}
        for model_metrics in self.model_performance_history.values():
            for metric_name, value in model_metrics.items():
                if metric_name not in metrics:
                    metrics[metric_name] = []
                metrics[metric_name].append(value)
        
        return {metric: np.mean(values) for metric, values in metrics.items()}
    
    def _get_learning_mode_distribution(self) -> Dict[str, int]:
        """Get distribution of learning modes"""
        # This would be implemented based on task tracking
        return {
            'supervised': 0,
            'unsupervised': 0,
            'reinforcement': 0,
            'transfer': 0,
            'meta': 0
        }

class DataPreprocessor:
    """Handles data preprocessing for AI learning"""
    
    def __init__(self):
        self.scalers = {}
        self.feature_encoders = {}
    
    def preprocess(self, data: Dict[str, Any]) -> np.ndarray:
        """Preprocess input data for model training"""
        try:
            # Extract features
            features = self._extract_features(data)
            
            # Normalize numerical features
            features = self._normalize_features(features)
            
            # Encode categorical features
            features = self._encode_categorical_features(features)
            
            return features
        except Exception as e:
            logger.error(f"Error preprocessing data: {e}")
            raise
    
    def _extract_features(self, data: Dict[str, Any]) -> np.ndarray:
        """Extract features from input data"""
        features = []
        
        # Extract numerical features
        numerical_features = [
            data.get('trading_volume', 0),
            data.get('price_change', 0),
            data.get('market_volatility', 0),
            data.get('user_activity', 0),
            data.get('system_load', 0)
        ]
        features.extend(numerical_features)
        
        # Extract categorical features
        categorical_features = [
            data.get('market_condition', 'normal'),
            data.get('user_type', 'standard'),
            data.get('time_of_day', 'day')
        ]
        features.extend(categorical_features)
        
        return np.array(features)
    
    def _normalize_features(self, features: np.ndarray) -> np.ndarray:
        """Normalize numerical features"""
        # Simple min-max normalization
        return (features - np.min(features)) / (np.max(features) - np.min(features))
    
    def _encode_categorical_features(self, features: np.ndarray) -> np.ndarray:
        """Encode categorical features"""
        # Simple one-hot encoding for categorical features
        # In a real implementation, this would be more sophisticated
        return features

class ModelTrainer:
    """Handles model training and updating"""
    
    def __init__(self):
        self.model_types = {
            'regression': RandomForestRegressor,
            'classification': RandomForestRegressor,
            'neural_network': MLPRegressor if not TORCH_AVAILABLE else None
        }
    
    def train_new_model(self, data: np.ndarray, target: Optional[Dict[str, Any]], 
                        learning_mode: LearningMode) -> Any:
        """Train a new model"""
        try:
            if learning_mode == LearningMode.SUPERVISED and target is not None:
                return self._train_supervised_model(data, target)
            elif learning_mode == LearningMode.UNSUPERVISED:
                return self._train_unsupervised_model(data)
            elif learning_mode == LearningMode.REINFORCEMENT:
                return self._train_reinforcement_model(data)
            else:
                raise ValueError(f"Unsupported learning mode: {learning_mode}")
        except Exception as e:
            logger.error(f"Error training new model: {e}")
            raise
    
    def update_model(self, model: Any, data: np.ndarray, target: Optional[Dict[str, Any]], 
                    learning_mode: LearningMode) -> Any:
        """Update an existing model"""
        try:
            if learning_mode == LearningMode.SUPERVISED and target is not None:
                return self._update_supervised_model(model, data, target)
            elif learning_mode == LearningMode.REINFORCEMENT:
                return self._update_reinforcement_model(model, data, target)
            else:
                return model  # No update for unsupervised learning
        except Exception as e:
            logger.error(f"Error updating model: {e}")
            raise
    
    def _train_supervised_model(self, data: np.ndarray, target: Dict[str, Any]) -> Any:
        """Train a supervised learning model"""
        # Extract target values
        target_values = np.array([target.get('prediction', 0)])
        
        # Split data for training
        X_train, X_test, y_train, y_test = train_test_split(
            data, target_values, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        return model
    
    def _train_unsupervised_model(self, data: np.ndarray) -> Any:
        """Train an unsupervised learning model"""
        # For unsupervised learning, we might use clustering or dimensionality reduction
        # For now, return a simple model
        from sklearn.cluster import KMeans
        model = KMeans(n_clusters=3, random_state=42)
        model.fit(data)
        return model
    
    def _train_reinforcement_model(self, data: np.ndarray) -> Any:
        """Train a reinforcement learning model"""
        # Simple Q-learning implementation
        # In a real implementation, this would use a proper RL framework
        return {'type': 'q_learning', 'q_table': {}}
    
    def _update_supervised_model(self, model: Any, data: np.ndarray, target: Dict[str, Any]) -> Any:
        """Update a supervised learning model"""
        target_values = np.array([target.get('prediction', 0)])
        
        # For RandomForest, we can't easily update, so we retrain
        # In a real implementation, you might use online learning algorithms
        return self._train_supervised_model(data, target)
    
    def _update_reinforcement_model(self, model: Any, data: np.ndarray, target: Optional[Dict[str, Any]]) -> Any:
        """Update a reinforcement learning model"""
        # Update Q-table based on new experience
        if target:
            state = hash(str(data)) % 1000  # Simple state representation
            action = target.get('action', 0)
            reward = target.get('reward', 0)
            
            if 'q_table' not in model:
                model['q_table'] = {}
            
            state_key = f"{state}_{action}"
            current_q = model['q_table'].get(state_key, 0)
            new_q = current_q + 0.1 * (reward - current_q)  # Simple Q-learning update
            model['q_table'][state_key] = new_q
        
        return model

class PerformanceAnalyzer:
    """Analyzes model performance and provides insights"""
    
    def evaluate_model(self, model: Any, data: np.ndarray, target: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """Evaluate model performance"""
        try:
            metrics = {}
            
            if target is not None:
                # Supervised learning evaluation
                predictions = self._get_predictions(model, data)
                actual = np.array([target.get('prediction', 0)])
                
                metrics['mse'] = mean_squared_error(actual, predictions)
                metrics['r2'] = r2_score(actual, predictions)
                metrics['accuracy'] = self._calculate_accuracy(predictions, actual)
            else:
                # Unsupervised learning evaluation
                metrics['inertia'] = self._calculate_inertia(model, data)
                metrics['silhouette_score'] = self._calculate_silhouette_score(model, data)
            
            return metrics
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            return {}
    
    def _get_predictions(self, model: Any, data: np.ndarray) -> np.ndarray:
        """Get predictions from model"""
        try:
            if hasattr(model, 'predict'):
                return model.predict(data)
            else:
                return np.array([0])  # Default prediction
        except Exception as e:
            logger.error(f"Error getting predictions: {e}")
            return np.array([0])
    
    def _calculate_accuracy(self, predictions: np.ndarray, actual: np.ndarray) -> float:
        """Calculate prediction accuracy"""
        try:
            return np.mean(np.abs(predictions - actual) < 0.1)
        except Exception as e:
            logger.error(f"Error calculating accuracy: {e}")
            return 0.0
    
    def _calculate_inertia(self, model: Any, data: np.ndarray) -> float:
        """Calculate clustering inertia"""
        try:
            if hasattr(model, 'inertia_'):
                return model.inertia_
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating inertia: {e}")
            return 0.0
    
    def _calculate_silhouette_score(self, model: Any, data: np.ndarray) -> float:
        """Calculate silhouette score for clustering"""
        try:
            from sklearn.metrics import silhouette_score
            if hasattr(model, 'predict'):
                labels = model.predict(data)
                return silhouette_score(data, labels)
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating silhouette score: {e}")
            return 0.0

class KnowledgeDistiller:
    """Distills knowledge from models and creates transferable insights"""
    
    def distill_knowledge(self, agent_id: str, model: Any, performance_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Distill knowledge from a model"""
        try:
            knowledge = {
                'agent_id': agent_id,
                'model_type': type(model).__name__,
                'performance_metrics': performance_metrics,
                'feature_importance': self._extract_feature_importance(model),
                'model_complexity': self._calculate_model_complexity(model),
                'learning_patterns': self._extract_learning_patterns(model),
                'distilled_at': datetime.utcnow().isoformat()
            }
            
            return knowledge
        except Exception as e:
            logger.error(f"Error distilling knowledge: {e}")
            return {}
    
    def _extract_feature_importance(self, model: Any) -> List[float]:
        """Extract feature importance from model"""
        try:
            if hasattr(model, 'feature_importances_'):
                return model.feature_importances_.tolist()
            return []
        except Exception as e:
            logger.error(f"Error extracting feature importance: {e}")
            return []
    
    def _calculate_model_complexity(self, model: Any) -> Dict[str, Any]:
        """Calculate model complexity metrics"""
        try:
            complexity = {
                'parameters': 0,
                'layers': 0,
                'memory_usage': 0
            }
            
            if hasattr(model, 'n_estimators'):
                complexity['parameters'] = model.n_estimators * 10  # Approximate
            elif hasattr(model, 'coef_'):
                complexity['parameters'] = len(model.coef_)
            
            return complexity
        except Exception as e:
            logger.error(f"Error calculating model complexity: {e}")
            return {}
    
    def _extract_learning_patterns(self, model: Any) -> Dict[str, Any]:
        """Extract learning patterns from model"""
        try:
            patterns = {
                'learning_rate': 0.0,
                'convergence_pattern': 'unknown',
                'overfitting_risk': 'low'
            }
            
            # Analyze model for learning patterns
            # This would be more sophisticated in a real implementation
            
            return patterns
        except Exception as e:
            logger.error(f"Error extracting learning patterns: {e}")
            return {}

# Example usage
async def main():
    config = {
        'model_storage_path': './models',
        'batch_size': 32,
        'learning_rate': 0.001,
        'epochs': 100,
        'validation_split': 0.2,
        'early_stopping_patience': 10,
        'model_update_threshold': 0.05
    }
    
    learning_system = AdvancedAILearningSystem(config)
    await learning_system.start()
    
    # Example learning task
    task = LearningTask(
        task_id="task_001",
        agent_id="trading_agent_1",
        task_type="price_prediction",
        input_data={
            'trading_volume': 1000000,
            'price_change': 0.02,
            'market_volatility': 0.15,
            'user_activity': 0.8,
            'system_load': 0.6
        },
        expected_output={'prediction': 150.50},
        learning_mode=LearningMode.SUPERVISED,
        priority=1
    )
    
    learning_system.add_learning_task(task)
    
    # Wait for processing
    await asyncio.sleep(5)
    
    # Get statistics
    stats = learning_system.get_learning_statistics()
    print(f"Learning Statistics: {stats}")
    
    await learning_system.stop()

if __name__ == "__main__":
    asyncio.run(main()) 