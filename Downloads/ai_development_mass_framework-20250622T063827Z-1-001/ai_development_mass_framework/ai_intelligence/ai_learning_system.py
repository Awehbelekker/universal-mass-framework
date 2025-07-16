import asyncio
import logging
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from decimal import Decimal
import pickle
import os

logger = logging.getLogger(__name__)

class ModelType(Enum):
    LINEAR_REGRESSION = "linear_regression"
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    NEURAL_NETWORK = "neural_network"
    LSTM = "lstm"
    TRANSFORMER = "transformer"
    ENSEMBLE = "ensemble"

class LearningStatus(Enum):
    IDLE = "idle"
    TRAINING = "training"
    EVALUATING = "evaluating"
    DEPLOYED = "deployed"
    ERROR = "error"

@dataclass
class TrainingData:
    """Training data structure"""
    features: np.ndarray
    targets: np.ndarray
    timestamps: List[datetime]
    metadata: Dict[str, Any]

@dataclass
class ModelPerformance:
    """Model performance metrics"""
    model_id: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    mse: float
    mae: float
    sharpe_ratio: float
    max_drawdown: float
    total_return: float
    win_rate: float
    profit_factor: float
    timestamp: datetime

@dataclass
class ModelConfig:
    """Model configuration"""
    model_type: ModelType
    hyperparameters: Dict[str, Any]
    feature_columns: List[str]
    target_column: str
    training_window: int  # days
    prediction_horizon: int  # days
    retrain_frequency: int  # days
    min_training_samples: int
    validation_split: float
    early_stopping_patience: int

class DataPreprocessor:
    """Data preprocessing for AI models"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.feature_scaler = None
        self.target_scaler = None
        
    async def preprocess_data(self, raw_data: pd.DataFrame) -> TrainingData:
        """Preprocess raw data for training"""
        try:
            # Clean data
            cleaned_data = self._clean_data(raw_data)
            
            # Feature engineering
            engineered_data = await self._engineer_features(cleaned_data)
            
            # Create features and targets
            features, targets = self._create_features_targets(engineered_data)
            
            # Scale features and targets
            scaled_features = self._scale_features(features)
            scaled_targets = self._scale_targets(targets)
            
            # Create training data
            training_data = TrainingData(
                features=scaled_features,
                targets=scaled_targets,
                timestamps=engineered_data.index.tolist(),
                metadata={
                    'original_shape': raw_data.shape,
                    'feature_columns': list(features.columns),
                    'target_column': self.config.get('target_column', 'returns'),
                    'scaling_applied': True
                }
            )
            
            return training_data
            
        except Exception as e:
            logger.error(f"Data preprocessing error: {e}")
            raise
    
    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean raw data"""
        # Remove duplicates
        data = data.drop_duplicates()
        
        # Handle missing values
        data = data.fillna(method='ffill').fillna(method='bfill')
        
        # Remove outliers (simple method)
        for column in data.select_dtypes(include=[np.number]).columns:
            Q1 = data[column].quantile(0.25)
            Q3 = data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
        
        return data
    
    async def _engineer_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Engineer features for the model"""
        try:
            # Technical indicators
            data = self._add_technical_indicators(data)
            
            # Price-based features
            data = self._add_price_features(data)
            
            # Volume-based features
            data = self._add_volume_features(data)
            
            # Time-based features
            data = self._add_time_features(data)
            
            # Market sentiment features
            data = await self._add_sentiment_features(data)
            
            # Remove any remaining NaN values
            data = data.dropna()
            
            return data
            
        except Exception as e:
            logger.error(f"Feature engineering error: {e}")
            raise
    
    def _add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add technical indicators"""
        # Moving averages
        data['sma_5'] = data['close'].rolling(window=5).mean()
        data['sma_20'] = data['close'].rolling(window=20).mean()
        data['ema_12'] = data['close'].ewm(span=12).mean()
        data['ema_26'] = data['close'].ewm(span=26).mean()
        
        # MACD
        data['macd'] = data['ema_12'] - data['ema_26']
        data['macd_signal'] = data['macd'].ewm(span=9).mean()
        data['macd_histogram'] = data['macd'] - data['macd_signal']
        
        # RSI
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        data['bb_middle'] = data['close'].rolling(window=20).mean()
        bb_std = data['close'].rolling(window=20).std()
        data['bb_upper'] = data['bb_middle'] + (bb_std * 2)
        data['bb_lower'] = data['bb_middle'] - (bb_std * 2)
        data['bb_width'] = (data['bb_upper'] - data['bb_lower']) / data['bb_middle']
        
        # Stochastic Oscillator
        low_min = data['low'].rolling(window=14).min()
        high_max = data['high'].rolling(window=14).max()
        data['stoch_k'] = 100 * ((data['close'] - low_min) / (high_max - low_min))
        data['stoch_d'] = data['stoch_k'].rolling(window=3).mean()
        
        return data
    
    def _add_price_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add price-based features"""
        # Returns
        data['returns'] = data['close'].pct_change()
        data['log_returns'] = np.log(data['close'] / data['close'].shift(1))
        
        # Price changes
        data['price_change'] = data['close'] - data['close'].shift(1)
        data['price_change_pct'] = data['price_change'] / data['close'].shift(1)
        
        # Volatility
        data['volatility'] = data['returns'].rolling(window=20).std()
        
        # Price levels
        data['price_high_20'] = data['high'].rolling(window=20).max()
        data['price_low_20'] = data['low'].rolling(window=20).min()
        data['price_position'] = (data['close'] - data['price_low_20']) / (data['price_high_20'] - data['price_low_20'])
        
        return data
    
    def _add_volume_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add volume-based features"""
        # Volume indicators
        data['volume_sma'] = data['volume'].rolling(window=20).mean()
        data['volume_ratio'] = data['volume'] / data['volume_sma']
        
        # Volume-price relationship
        data['volume_price_trend'] = (data['volume'] * data['returns']).rolling(window=20).sum()
        
        # On-balance volume
        data['obv'] = (data['volume'] * np.sign(data['returns'])).cumsum()
        
        return data
    
    def _add_time_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add time-based features"""
        # Day of week
        data['day_of_week'] = pd.to_datetime(data.index).dayofweek
        
        # Month
        data['month'] = pd.to_datetime(data.index).month
        
        # Quarter
        data['quarter'] = pd.to_datetime(data.index).quarter
        
        # Time of day (if available)
        if 'time' in data.columns:
            data['hour'] = pd.to_datetime(data['time']).dt.hour
        else:
            data['hour'] = 12  # Default to noon
        
        return data
    
    async def _add_sentiment_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add sentiment features"""
        # This would integrate with your sentiment analysis API
        # For now, add mock sentiment features
        
        # Mock sentiment scores
        np.random.seed(42)
        data['sentiment_score'] = np.random.normal(0, 1, len(data))
        data['sentiment_momentum'] = data['sentiment_score'].rolling(window=5).mean()
        
        # News sentiment (mock)
        data['news_sentiment'] = np.random.normal(0, 0.5, len(data))
        data['social_sentiment'] = np.random.normal(0, 0.5, len(data))
        
        return data
    
    def _create_features_targets(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Create features and targets for training"""
        # Define feature columns
        feature_columns = [
            'sma_5', 'sma_20', 'ema_12', 'ema_26',
            'macd', 'macd_signal', 'macd_histogram',
            'rsi', 'bb_width', 'stoch_k', 'stoch_d',
            'returns', 'log_returns', 'volatility',
            'price_position', 'volume_ratio',
            'volume_price_trend', 'obv',
            'day_of_week', 'month', 'quarter',
            'sentiment_score', 'sentiment_momentum',
            'news_sentiment', 'social_sentiment'
        ]
        
        # Create features
        features = data[feature_columns].copy()
        
        # Create target (next period returns)
        target = data['returns'].shift(-1)
        
        # Remove rows with NaN values
        valid_idx = features.notna().all(axis=1) & target.notna()
        features = features[valid_idx]
        target = target[valid_idx]
        
        return features, target
    
    def _scale_features(self, features: pd.DataFrame) -> np.ndarray:
        """Scale features using StandardScaler"""
        from sklearn.preprocessing import StandardScaler
        
        if self.feature_scaler is None:
            self.feature_scaler = StandardScaler()
            return self.feature_scaler.fit_transform(features)
        else:
            return self.feature_scaler.transform(features)
    
    def _scale_targets(self, targets: pd.Series) -> np.ndarray:
        """Scale targets using StandardScaler"""
        from sklearn.preprocessing import StandardScaler
        
        if self.target_scaler is None:
            self.target_scaler = StandardScaler()
            return self.target_scaler.fit_transform(targets.values.reshape(-1, 1)).flatten()
        else:
            return self.target_scaler.transform(targets.values.reshape(-1, 1)).flatten()

class ModelTrainer:
    """Model training and evaluation"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.models = {}
        self.performance_history = []
        
    async def train_model(self, training_data: TrainingData, model_id: str) -> Tuple[bool, str]:
        """Train a new model"""
        try:
            logger.info(f"Starting model training for {model_id}")
            
            # Split data
            split_idx = int(len(training_data.features) * (1 - self.config.validation_split))
            X_train = training_data.features[:split_idx]
            y_train = training_data.targets[:split_idx]
            X_val = training_data.features[split_idx:]
            y_val = training_data.targets[split_idx:]
            
            # Create and train model
            model = await self._create_model()
            model = await self._train_model(model, X_train, y_train, X_val, y_val)
            
            # Evaluate model
            performance = await self._evaluate_model(model, X_val, y_val, model_id)
            
            # Store model and performance
            self.models[model_id] = {
                'model': model,
                'config': self.config,
                'training_data': training_data,
                'performance': performance,
                'created_at': datetime.utcnow()
            }
            
            self.performance_history.append(performance)
            
            logger.info(f"Model training completed for {model_id}")
            return True, f"Model trained successfully. Accuracy: {performance.accuracy:.4f}"
            
        except Exception as e:
            logger.error(f"Model training error: {e}")
            return False, f"Model training failed: {str(e)}"
    
    async def _create_model(self):
        """Create model based on configuration"""
        try:
            if self.config.model_type == ModelType.LINEAR_REGRESSION:
                from sklearn.linear_model import LinearRegression
                return LinearRegression(**self.config.hyperparameters)
            
            elif self.config.model_type == ModelType.RANDOM_FOREST:
                from sklearn.ensemble import RandomForestRegressor
                return RandomForestRegressor(**self.config.hyperparameters)
            
            elif self.config.model_type == ModelType.GRADIENT_BOOSTING:
                from sklearn.ensemble import GradientBoostingRegressor
                return GradientBoostingRegressor(**self.config.hyperparameters)
            
            elif self.config.model_type == ModelType.NEURAL_NETWORK:
                from sklearn.neural_network import MLPRegressor
                return MLPRegressor(**self.config.hyperparameters)
            
            else:
                raise ValueError(f"Unsupported model type: {self.config.model_type}")
                
        except Exception as e:
            logger.error(f"Model creation error: {e}")
            raise
    
    async def _train_model(self, model, X_train, y_train, X_val, y_val):
        """Train the model"""
        try:
            # For sklearn models, training is synchronous
            model.fit(X_train, y_train)
            return model
            
        except Exception as e:
            logger.error(f"Model training error: {e}")
            raise
    
    async def _evaluate_model(self, model, X_val, y_val, model_id: str) -> ModelPerformance:
        """Evaluate model performance"""
        try:
            from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
            
            # Make predictions
            y_pred = model.predict(X_val)
            
            # Calculate metrics
            mse = mean_squared_error(y_val, y_pred)
            mae = mean_absolute_error(y_val, y_pred)
            r2 = r2_score(y_val, y_pred)
            
            # Calculate trading metrics
            trading_metrics = self._calculate_trading_metrics(y_val, y_pred)
            
            performance = ModelPerformance(
                model_id=model_id,
                accuracy=r2,
                precision=trading_metrics['precision'],
                recall=trading_metrics['recall'],
                f1_score=trading_metrics['f1_score'],
                mse=mse,
                mae=mae,
                sharpe_ratio=trading_metrics['sharpe_ratio'],
                max_drawdown=trading_metrics['max_drawdown'],
                total_return=trading_metrics['total_return'],
                win_rate=trading_metrics['win_rate'],
                profit_factor=trading_metrics['profit_factor'],
                timestamp=datetime.utcnow()
            )
            
            return performance
            
        except Exception as e:
            logger.error(f"Model evaluation error: {e}")
            raise
    
    def _calculate_trading_metrics(self, y_true, y_pred) -> Dict[str, float]:
        """Calculate trading-specific metrics"""
        try:
            # Create trading signals
            signals = np.where(y_pred > 0, 1, -1)
            actual_returns = y_true
            
            # Calculate cumulative returns
            strategy_returns = signals * actual_returns
            cumulative_returns = np.cumprod(1 + strategy_returns)
            
            # Sharpe ratio
            sharpe_ratio = np.mean(strategy_returns) / np.std(strategy_returns) if np.std(strategy_returns) > 0 else 0
            
            # Maximum drawdown
            peak = np.maximum.accumulate(cumulative_returns)
            drawdown = (cumulative_returns - peak) / peak
            max_drawdown = np.min(drawdown)
            
            # Total return
            total_return = cumulative_returns[-1] - 1
            
            # Win rate
            winning_trades = np.sum(strategy_returns > 0)
            total_trades = len(strategy_returns)
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
            
            # Profit factor
            gross_profit = np.sum(strategy_returns[strategy_returns > 0])
            gross_loss = abs(np.sum(strategy_returns[strategy_returns < 0]))
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
            
            # Precision and recall (for classification-like metrics)
            true_positives = np.sum((signals == 1) & (actual_returns > 0))
            false_positives = np.sum((signals == 1) & (actual_returns <= 0))
            false_negatives = np.sum((signals == -1) & (actual_returns > 0))
            
            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
            
            return {
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'total_return': total_return,
                'win_rate': win_rate,
                'profit_factor': profit_factor
            }
            
        except Exception as e:
            logger.error(f"Trading metrics calculation error: {e}")
            return {
                'precision': 0.0,
                'recall': 0.0,
                'f1_score': 0.0,
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'total_return': 0.0,
                'win_rate': 0.0,
                'profit_factor': 0.0
            }

class AILearningSystem:
    """Main AI learning system that coordinates all AI operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.preprocessor = DataPreprocessor(config.get('preprocessing', {}))
        self.trainer = ModelTrainer(config.get('model_config', {}))
        self.models = {}
        self.performance_history = []
        self.status = LearningStatus.IDLE
        self.last_training = None
        
    async def train_new_model(self, symbol: str, data_source: str = "market_data") -> Tuple[bool, str, Optional[str]]:
        """Train a new model for a symbol"""
        try:
            self.status = LearningStatus.TRAINING
            
            # Generate model ID
            model_id = f"{symbol}_{self.trainer.config.model_type.value}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            # Get training data
            raw_data = await self._get_training_data(symbol, data_source)
            if raw_data is None or raw_data.empty:
                return False, f"No training data available for {symbol}", None
            
            # Preprocess data
            training_data = await self.preprocessor.preprocess_data(raw_data)
            
            # Check if enough data
            if len(training_data.features) < self.trainer.config.min_training_samples:
                return False, f"Insufficient training data. Required: {self.trainer.config.min_training_samples}, Available: {len(training_data.features)}", None
            
            # Train model
            success, message = await self.trainer.train_model(training_data, model_id)
            
            if success:
                self.models[model_id] = {
                    'symbol': symbol,
                    'data_source': data_source,
                    'model': self.trainer.models[model_id],
                    'created_at': datetime.utcnow(),
                    'status': LearningStatus.DEPLOYED
                }
                self.last_training = datetime.utcnow()
                self.status = LearningStatus.IDLE
                
                logger.info(f"Model training completed: {model_id}")
                return True, message, model_id
            else:
                self.status = LearningStatus.ERROR
                return False, message, None
                
        except Exception as e:
            logger.error(f"Model training error: {e}")
            self.status = LearningStatus.ERROR
            return False, f"Model training failed: {str(e)}", None
    
    async def predict(self, model_id: str, features: np.ndarray) -> Tuple[bool, str, Optional[float]]:
        """Make prediction using a trained model"""
        try:
            if model_id not in self.models:
                return False, f"Model {model_id} not found", None
            
            model_info = self.models[model_id]
            model = model_info['model']['model']
            
            # Scale features if needed
            if hasattr(self.preprocessor, 'feature_scaler') and self.preprocessor.feature_scaler:
                features = self.preprocessor.feature_scaler.transform(features.reshape(1, -1))
            
            # Make prediction
            prediction = model.predict(features)[0]
            
            # Inverse scale if needed
            if hasattr(self.preprocessor, 'target_scaler') and self.preprocessor.target_scaler:
                prediction = self.preprocessor.target_scaler.inverse_transform([[prediction]])[0][0]
            
            return True, "Prediction successful", float(prediction)
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return False, f"Prediction failed: {str(e)}", None
    
    async def evaluate_model_performance(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Evaluate performance of a specific model"""
        try:
            if model_id not in self.models:
                return None
            
            model_info = self.models[model_id]
            performance = model_info['model']['performance']
            
            return {
                'model_id': model_id,
                'symbol': model_info['symbol'],
                'accuracy': performance.accuracy,
                'precision': performance.precision,
                'recall': performance.recall,
                'f1_score': performance.f1_score,
                'mse': performance.mse,
                'mae': performance.mae,
                'sharpe_ratio': performance.sharpe_ratio,
                'max_drawdown': performance.max_drawdown,
                'total_return': performance.total_return,
                'win_rate': performance.win_rate,
                'profit_factor': performance.profit_factor,
                'created_at': model_info['created_at'].isoformat(),
                'status': model_info['status'].value
            }
            
        except Exception as e:
            logger.error(f"Performance evaluation error: {e}")
            return None
    
    async def get_all_models(self) -> List[Dict[str, Any]]:
        """Get information about all trained models"""
        try:
            models_info = []
            for model_id, model_info in self.models.items():
                performance = await self.evaluate_model_performance(model_id)
                if performance:
                    models_info.append(performance)
            
            return models_info
            
        except Exception as e:
            logger.error(f"Get models error: {e}")
            return []
    
    async def retrain_model(self, model_id: str) -> Tuple[bool, str]:
        """Retrain an existing model"""
        try:
            if model_id not in self.models:
                return False, f"Model {model_id} not found"
            
            model_info = self.models[model_id]
            symbol = model_info['symbol']
            data_source = model_info['data_source']
            
            # Remove old model
            del self.models[model_id]
            
            # Train new model
            success, message, new_model_id = await self.train_new_model(symbol, data_source)
            
            if success:
                return True, f"Model retrained successfully. New model ID: {new_model_id}"
            else:
                return False, f"Model retraining failed: {message}"
                
        except Exception as e:
            logger.error(f"Model retraining error: {e}")
            return False, f"Model retraining failed: {str(e)}"
    
    async def delete_model(self, model_id: str) -> Tuple[bool, str]:
        """Delete a trained model"""
        try:
            if model_id not in self.models:
                return False, f"Model {model_id} not found"
            
            del self.models[model_id]
            return True, f"Model {model_id} deleted successfully"
            
        except Exception as e:
            logger.error(f"Model deletion error: {e}")
            return False, f"Model deletion failed: {str(e)}"
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        try:
            return {
                'status': self.status.value,
                'total_models': len(self.models),
                'last_training': self.last_training.isoformat() if self.last_training else None,
                'active_models': len([m for m in self.models.values() if m['status'] == LearningStatus.DEPLOYED]),
                'error_models': len([m for m in self.models.values() if m['status'] == LearningStatus.ERROR]),
                'performance_history_count': len(self.trainer.performance_history)
            }
            
        except Exception as e:
            logger.error(f"Status check error: {e}")
            return {
                'status': 'error',
                'total_models': 0,
                'last_training': None,
                'active_models': 0,
                'error_models': 0,
                'performance_history_count': 0
            }
    
    # Helper method to get training data
    async def _get_training_data(self, symbol: str, data_source: str) -> Optional[pd.DataFrame]:
        """Get training data for a symbol"""
        try:
            # This would integrate with your data source
            # For now, generate mock data
            
            # Generate mock OHLCV data
            np.random.seed(42)
            dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='D')
            
            # Generate price data with some trend and volatility
            returns = np.random.normal(0.0005, 0.02, len(dates))  # Daily returns
            prices = 100 * np.cumprod(1 + returns)
            
            # Generate OHLCV data
            data = pd.DataFrame({
                'open': prices * (1 + np.random.normal(0, 0.005, len(dates))),
                'high': prices * (1 + abs(np.random.normal(0, 0.01, len(dates)))),
                'low': prices * (1 - abs(np.random.normal(0, 0.01, len(dates)))),
                'close': prices,
                'volume': np.random.randint(1000000, 10000000, len(dates))
            }, index=dates)
            
            # Add time column
            data['time'] = dates
            
            return data
            
        except Exception as e:
            logger.error(f"Data retrieval error: {e}")
            return None 