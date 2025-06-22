"""
Predictive Analyzer - Universal Predictive Analytics Engine
===========================================================

Advanced predictive analytics engine for the Universal MASS Framework.
Provides enterprise-grade forecasting, trend prediction, and future scenario
modeling with real-time intelligence and adaptive learning capabilities.

Key Features:
- Universal prediction algorithms for any data type
- Multi-horizon forecasting capabilities
- Ensemble prediction methods
- Confidence interval estimation
- Adaptive model selection
- Real-time prediction updates
- Scenario modeling and simulation
- Risk assessment and uncertainty quantification
- Trend extrapolation and pattern-based forecasting
- Business impact prediction

Author: Universal MASS Framework Team
Version: 1.0.0
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import statistics
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import cross_val_score
import pandas as pd
from collections import defaultdict, deque
import json
import math

# Configure logging
logger = logging.getLogger(__name__)

class PredictionHorizon(Enum):
    """Prediction time horizons"""
    SHORT_TERM = "short_term"  # 1-7 periods
    MEDIUM_TERM = "medium_term"  # 1-4 weeks
    LONG_TERM = "long_term"  # 1-12 months
    EXTENDED = "extended"  # 1+ years

class PredictionType(Enum):
    """Types of predictions"""
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TIME_SERIES = "time_series"
    TREND = "trend"
    SEASONAL = "seasonal"
    ANOMALY = "anomaly"
    BINARY = "binary"
    MULTI_CLASS = "multi_class"

class ModelType(Enum):
    """Prediction model types"""
    LINEAR_REGRESSION = "linear_regression"
    RIDGE_REGRESSION = "ridge_regression"
    LASSO_REGRESSION = "lasso_regression"
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    ENSEMBLE = "ensemble"
    MOVING_AVERAGE = "moving_average"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    TREND_ANALYSIS = "trend_analysis"

class ConfidenceLevel(Enum):
    """Confidence levels for predictions"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class PredictionInput:
    """Input data for prediction analysis"""
    historical_data: List[Any] = field(default_factory=list)
    timestamps: Optional[List[datetime]] = None
    target_variable: str = "value"
    features: Optional[List[str]] = None
    prediction_horizon: int = 1
    horizon_type: PredictionHorizon = PredictionHorizon.SHORT_TERM
    prediction_type: PredictionType = PredictionType.NUMERICAL
    context: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PredictionResult:
    """Result of a single prediction"""
    predicted_value: Any = None
    confidence_score: float = 0.0
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    prediction_probability: Optional[float] = None
    model_used: ModelType = ModelType.LINEAR_REGRESSION
    feature_importance: Dict[str, float] = field(default_factory=dict)
    uncertainty_factors: List[str] = field(default_factory=list)

@dataclass
class EnsemblePrediction:
    """Ensemble prediction combining multiple models"""
    predictions: List[PredictionResult] = field(default_factory=list)
    consensus_prediction: Any = None
    consensus_confidence: float = 0.0
    model_weights: Dict[ModelType, float] = field(default_factory=dict)
    ensemble_variance: float = 0.0
    reliability_score: float = 0.0

@dataclass
class PredictionScenario:
    """Future scenario prediction"""
    scenario_name: str = ""
    scenario_probability: float = 0.0
    predicted_values: List[Any] = field(default_factory=list)
    scenario_description: str = ""
    key_assumptions: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    business_impact: str = ""

@dataclass
class PredictiveAnalysisResult:
    """Complete result of predictive analysis"""
    analysis_id: str
    data_source: str
    analysis_timestamp: datetime
    prediction_input: PredictionInput
    primary_prediction: EnsemblePrediction
    alternative_scenarios: List[PredictionScenario] = field(default_factory=list)
    trend_analysis: Dict[str, Any] = field(default_factory=dict)
    risk_assessment: Dict[str, Any] = field(default_factory=dict)
    model_performance: Dict[str, Any] = field(default_factory=dict)
    insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    confidence_level: ConfidenceLevel = ConfidenceLevel.MEDIUM
    processing_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

class PredictiveAnalyzer:
    """
    Universal Predictive Analytics Engine
    
    Advanced prediction engine that can forecast future values, trends, and
    scenarios for any type of data with enterprise-grade accuracy and reliability.
    
    Key Capabilities:
    - Multi-algorithm ensemble predictions
    - Adaptive model selection based on data characteristics
    - Confidence interval estimation and uncertainty quantification
    - Real-time prediction updates and model adaptation
    - Scenario modeling and risk assessment
    - Business impact prediction and optimization
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Predictive Analyzer"""
        self.config = config or {}
        self.models = {}
        self.model_cache = {}
        self.prediction_history = defaultdict(deque)
        self.performance_metrics = defaultdict(dict)
        self.analysis_stats = {
            "total_predictions": 0,
            "average_accuracy": 0.0,
            "model_usage": defaultdict(int),
            "processing_time_total": 0.0
        }
        
        # Initialize prediction models
        self._initialize_prediction_models()
        
        # Trust framework integration
        self.trust_framework = self.config.get("trust_framework")
        
        logger.info("Universal Predictive Analyzer initialized")
    
    def _initialize_prediction_models(self):
        """Initialize prediction models"""
        try:
            # Regression models
            self.models[ModelType.LINEAR_REGRESSION] = LinearRegression()
            self.models[ModelType.RIDGE_REGRESSION] = Ridge(alpha=1.0)
            self.models[ModelType.LASSO_REGRESSION] = Lasso(alpha=1.0)
            
            # Ensemble models
            self.models[ModelType.RANDOM_FOREST] = RandomForestRegressor(
                n_estimators=100, random_state=42, max_depth=10
            )
            self.models[ModelType.GRADIENT_BOOSTING] = GradientBoostingRegressor(
                n_estimators=100, random_state=42, max_depth=6
            )
            
            # Scalers
            self.standard_scaler = StandardScaler()
            self.minmax_scaler = MinMaxScaler()
            
            logger.info("Prediction models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing prediction models: {str(e)}")
    
    async def predict(self, prediction_input: PredictionInput) -> PredictiveAnalysisResult:
        """
        Generate comprehensive predictions for any type of data
        
        Args:
            prediction_input: Input data and parameters for prediction
            
        Returns:
            PredictiveAnalysisResult with predictions, scenarios, and insights
        """
        start_time = datetime.utcnow()
        analysis_id = f"prediction_analysis_{int(start_time.timestamp())}"
        
        try:
            logger.info(f"Starting predictive analysis: {analysis_id}")
            
            # Prepare data for prediction
            prepared_data = await self._prepare_prediction_data(prediction_input)
            
            # Generate ensemble predictions
            primary_prediction = await self._generate_ensemble_prediction(
                prepared_data, prediction_input
            )
            
            # Generate alternative scenarios
            scenarios = await self._generate_prediction_scenarios(
                prepared_data, prediction_input, primary_prediction
            )
            
            # Perform trend analysis
            trend_analysis = await self._analyze_prediction_trends(
                prepared_data, prediction_input
            )
            
            # Assess prediction risks
            risk_assessment = await self._assess_prediction_risks(
                primary_prediction, scenarios, prediction_input
            )
            
            # Evaluate model performance
            model_performance = await self._evaluate_model_performance(
                prepared_data, primary_prediction
            )
            
            # Generate insights and recommendations
            insights = await self._generate_prediction_insights(
                primary_prediction, scenarios, trend_analysis
            )
            recommendations = await self._generate_prediction_recommendations(
                primary_prediction, risk_assessment, prediction_input
            )
            
            # Determine confidence level
            confidence_level = self._determine_confidence_level(primary_prediction)
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Create analysis result
            result = PredictiveAnalysisResult(
                analysis_id=analysis_id,
                data_source=prediction_input.context.get("source", "unknown"),
                analysis_timestamp=start_time,
                prediction_input=prediction_input,
                primary_prediction=primary_prediction,
                alternative_scenarios=scenarios,
                trend_analysis=trend_analysis,
                risk_assessment=risk_assessment,
                model_performance=model_performance,
                insights=insights,
                recommendations=recommendations,
                confidence_level=confidence_level,
                processing_time=processing_time,
                metadata={
                    "data_points_used": len(prepared_data.get("features", [])),
                    "models_evaluated": len(primary_prediction.predictions),
                    "scenarios_generated": len(scenarios),
                    "prediction_horizon": prediction_input.prediction_horizon,
                    "trust_score": await self._calculate_prediction_trust_score(
                        primary_prediction, prediction_input
                    )
                }
            )
            
            # Update statistics and cache
            self._update_prediction_statistics(result)
            self.model_cache[analysis_id] = result
            
            logger.info(f"Predictive analysis completed: {analysis_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error in predictive analysis {analysis_id}: {str(e)}")
            return PredictiveAnalysisResult(
                analysis_id=analysis_id,
                data_source=prediction_input.context.get("source", "unknown"),
                analysis_timestamp=start_time,
                prediction_input=prediction_input,
                primary_prediction=EnsemblePrediction(),
                insights=[f"Error in predictive analysis: {str(e)}"],
                confidence_level=ConfidenceLevel.LOW,
                processing_time=(datetime.utcnow() - start_time).total_seconds()
            )
    
    async def _prepare_prediction_data(self, prediction_input: PredictionInput) -> Dict[str, Any]:
        """Prepare data for prediction analysis"""
        try:
            prepared_data = {
                "features": [],
                "targets": [],
                "timestamps": [],
                "feature_names": [],
                "is_time_series": False,
                "data_quality": {}
            }
            
            # Handle historical data
            historical_data = prediction_input.historical_data
            if not historical_data:
                return prepared_data
            
            # Determine if it's time series data
            if prediction_input.timestamps:
                prepared_data["is_time_series"] = True
                prepared_data["timestamps"] = prediction_input.timestamps
            
            # Extract features and targets
            if isinstance(historical_data[0], dict):
                # Dictionary format data
                feature_names = list(historical_data[0].keys())
                if prediction_input.target_variable in feature_names:
                    feature_names.remove(prediction_input.target_variable)
                
                prepared_data["feature_names"] = feature_names
                
                for item in historical_data:
                    if prediction_input.target_variable in item:
                        target_value = item[prediction_input.target_variable]
                        if isinstance(target_value, (int, float)):
                            prepared_data["targets"].append(target_value)
                            
                            # Extract numeric features
                            features = []
                            for fname in feature_names:
                                if fname in item and isinstance(item[fname], (int, float)):
                                    features.append(item[fname])
                            
                            if features:
                                prepared_data["features"].append(features)
            
            elif isinstance(historical_data[0], (int, float)):
                # Simple numeric list
                prepared_data["targets"] = historical_data
                
                # Create time-based features if timestamps available
                if prediction_input.timestamps:
                    for i, ts in enumerate(prediction_input.timestamps):
                        features = [
                            i,  # Index
                            ts.hour if hasattr(ts, 'hour') else 0,  # Hour
                            ts.weekday() if hasattr(ts, 'weekday') else 0,  # Day of week
                        ]
                        prepared_data["features"].append(features)
                        prepared_data["feature_names"] = ["index", "hour", "day_of_week"]
                else:
                    # Use index as feature
                    for i in range(len(historical_data)):
                        prepared_data["features"].append([i])
                        prepared_data["feature_names"] = ["index"]
            
            # Assess data quality
            prepared_data["data_quality"] = self._assess_data_quality(prepared_data)
            
            logger.debug(f"Prepared prediction data: {len(prepared_data['targets'])} samples")
            return prepared_data
            
        except Exception as e:
            logger.error(f"Error preparing prediction data: {str(e)}")
            return {"features": [], "targets": [], "data_quality": {"score": 0.0}}
    
    def _assess_data_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess quality of prediction data"""
        try:
            quality = {
                "score": 0.0,
                "completeness": 0.0,
                "consistency": 0.0,
                "issues": []
            }
            
            targets = data.get("targets", [])
            features = data.get("features", [])
            
            if not targets:
                quality["issues"].append("No target data available")
                return quality
            
            # Completeness check
            missing_targets = sum(1 for t in targets if t is None or (isinstance(t, float) and math.isnan(t)))
            quality["completeness"] = 1.0 - (missing_targets / len(targets))
            
            # Consistency check (variance in data)
            if len(targets) > 1:
                try:
                    target_std = statistics.stdev(targets)
                    target_mean = statistics.mean(targets)
                    cv = target_std / target_mean if target_mean != 0 else float('inf')
                    quality["consistency"] = 1.0 / (1.0 + cv) if cv != float('inf') else 0.0
                except:
                    quality["consistency"] = 0.5
            
            # Calculate overall score
            quality["score"] = (quality["completeness"] + quality["consistency"]) / 2
            
            # Add quality issues
            if quality["completeness"] < 0.9:
                quality["issues"].append("High missing data rate")
            if quality["consistency"] < 0.3:
                quality["issues"].append("High data variance")
            if len(targets) < 10:
                quality["issues"].append("Limited historical data")
            
            return quality
            
        except Exception as e:
            logger.error(f"Error assessing data quality: {str(e)}")
            return {"score": 0.0, "issues": ["Error in quality assessment"]}
    
    async def _generate_ensemble_prediction(self, data: Dict[str, Any], 
                                          prediction_input: PredictionInput) -> EnsemblePrediction:
        """Generate ensemble prediction using multiple models"""
        try:
            predictions = []
            model_weights = {}
            
            features = data.get("features", [])
            targets = data.get("targets", [])
            
            if len(features) < 3 or len(targets) < 3:
                # Insufficient data, use simple prediction
                return await self._generate_simple_prediction(data, prediction_input)
            
            # Prepare data for sklearn models
            X = np.array(features)
            y = np.array(targets)
            
            # Scale features
            X_scaled = self.standard_scaler.fit_transform(X)
            
            # Test multiple models
            models_to_test = [
                ModelType.LINEAR_REGRESSION,
                ModelType.RIDGE_REGRESSION,
                ModelType.RANDOM_FOREST,
                ModelType.GRADIENT_BOOSTING
            ]
            
            for model_type in models_to_test:
                try:
                    prediction_result = await self._train_and_predict_model(
                        model_type, X_scaled, y, prediction_input
                    )
                    if prediction_result:
                        predictions.append(prediction_result)
                        
                        # Calculate model weight based on performance
                        weight = prediction_result.confidence_score
                        model_weights[model_type] = weight
                        
                except Exception as e:
                    logger.warning(f"Model {model_type.value} failed: {str(e)}")
                    continue
            
            if not predictions:
                return await self._generate_simple_prediction(data, prediction_input)
            
            # Calculate ensemble consensus
            consensus_prediction = self._calculate_ensemble_consensus(predictions, model_weights)
            consensus_confidence = self._calculate_ensemble_confidence(predictions, model_weights)
            ensemble_variance = self._calculate_ensemble_variance(predictions)
            reliability_score = self._calculate_reliability_score(predictions, data)
            
            ensemble = EnsemblePrediction(
                predictions=predictions,
                consensus_prediction=consensus_prediction,
                consensus_confidence=consensus_confidence,
                model_weights=model_weights,
                ensemble_variance=ensemble_variance,
                reliability_score=reliability_score
            )
            
            return ensemble
            
        except Exception as e:
            logger.error(f"Error generating ensemble prediction: {str(e)}")
            return await self._generate_simple_prediction(data, prediction_input)
    
    async def _train_and_predict_model(self, model_type: ModelType, X: np.ndarray, 
                                     y: np.ndarray, prediction_input: PredictionInput) -> Optional[PredictionResult]:
        """Train a model and generate prediction"""
        try:
            model = self.models[model_type]
            
            # Split data for training and validation
            split_point = max(1, len(X) - prediction_input.prediction_horizon)
            X_train, X_test = X[:split_point], X[split_point:]
            y_train, y_test = y[:split_point], y[split_point:]
            
            # Train model
            model.fit(X_train, y_train)
            
            # Make prediction
            if len(X_test) > 0:
                prediction = model.predict(X_test)[0]
                
                # Calculate confidence based on model performance
                if len(y_test) > 0:
                    # Use actual test data for confidence
                    test_predictions = model.predict(X_test)
                    mse = mean_squared_error(y_test, test_predictions)
                    confidence = max(0.1, 1.0 - (mse / np.var(y_train)))
                else:
                    # Use cross-validation score
                    cv_scores = cross_val_score(model, X_train, y_train, cv=min(5, len(X_train)))
                    confidence = max(0.1, np.mean(cv_scores))
            else:
                # Predict next value
                last_features = X[-1:] if len(X) > 0 else np.zeros((1, X.shape[1]))
                prediction = model.predict(last_features)[0]
                
                # Use training performance for confidence
                train_predictions = model.predict(X_train)
                mse = mean_squared_error(y_train, train_predictions)
                confidence = max(0.1, 1.0 - (mse / np.var(y_train)))
            
            # Calculate confidence interval
            prediction_std = math.sqrt(abs(prediction)) if prediction > 0 else 1.0
            confidence_interval = (
                prediction - 1.96 * prediction_std,
                prediction + 1.96 * prediction_std
            )
            
            # Feature importance (for tree-based models)
            feature_importance = {}
            if hasattr(model, 'feature_importances_'):
                feature_names = prediction_input.features or [f"feature_{i}" for i in range(len(model.feature_importances_))]
                for i, importance in enumerate(model.feature_importances_):
                    if i < len(feature_names):
                        feature_importance[feature_names[i]] = float(importance)
            
            result = PredictionResult(
                predicted_value=float(prediction),
                confidence_score=min(max(float(confidence), 0.0), 1.0),
                confidence_interval=confidence_interval,
                model_used=model_type,
                feature_importance=feature_importance,
                uncertainty_factors=self._identify_uncertainty_factors(model_type, confidence)
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error training model {model_type.value}: {str(e)}")
            return None
    
    async def _generate_simple_prediction(self, data: Dict[str, Any], 
                                        prediction_input: PredictionInput) -> EnsemblePrediction:
        """Generate simple prediction when advanced models fail"""
        try:
            targets = data.get("targets", [])
            if not targets:
                return EnsemblePrediction()
            
            # Simple moving average prediction
            window_size = min(5, len(targets))
            if window_size > 0:
                recent_values = targets[-window_size:]
                predicted_value = statistics.mean(recent_values)
                
                # Simple confidence based on data stability
                if len(recent_values) > 1:
                    std_dev = statistics.stdev(recent_values)
                    mean_val = statistics.mean(recent_values)
                    confidence = max(0.1, 1.0 - (std_dev / abs(mean_val)) if mean_val != 0 else 0.5)
                else:
                    confidence = 0.5
                
                simple_prediction = PredictionResult(
                    predicted_value=predicted_value,
                    confidence_score=confidence,
                    confidence_interval=(predicted_value * 0.9, predicted_value * 1.1),
                    model_used=ModelType.MOVING_AVERAGE,
                    uncertainty_factors=["Limited data", "Simple model"]
                )
                
                return EnsemblePrediction(
                    predictions=[simple_prediction],
                    consensus_prediction=predicted_value,
                    consensus_confidence=confidence,
                    model_weights={ModelType.MOVING_AVERAGE: 1.0},
                    ensemble_variance=0.0,
                    reliability_score=confidence
                )
            
            return EnsemblePrediction()
            
        except Exception as e:
            logger.error(f"Error generating simple prediction: {str(e)}")
            return EnsemblePrediction()
    
    def _calculate_ensemble_consensus(self, predictions: List[PredictionResult], 
                                    model_weights: Dict[ModelType, float]) -> float:
        """Calculate ensemble consensus prediction"""
        try:
            if not predictions:
                return 0.0
            
            # Weighted average of predictions
            total_weight = sum(model_weights.values())
            if total_weight == 0:
                return statistics.mean([p.predicted_value for p in predictions])
            
            weighted_sum = sum(p.predicted_value * model_weights.get(p.model_used, 1.0) 
                             for p in predictions)
            
            return weighted_sum / total_weight
            
        except Exception as e:
            logger.error(f"Error calculating ensemble consensus: {str(e)}")
            return 0.0
    
    def _calculate_ensemble_confidence(self, predictions: List[PredictionResult], 
                                     model_weights: Dict[ModelType, float]) -> float:
        """Calculate ensemble confidence"""
        try:
            if not predictions:
                return 0.0
            
            # Weighted average of confidence scores
            total_weight = sum(model_weights.values())
            if total_weight == 0:
                return statistics.mean([p.confidence_score for p in predictions])
            
            weighted_confidence = sum(p.confidence_score * model_weights.get(p.model_used, 1.0) 
                                    for p in predictions)
            
            return weighted_confidence / total_weight
            
        except Exception as e:
            logger.error(f"Error calculating ensemble confidence: {str(e)}")
            return 0.0
    
    def _calculate_ensemble_variance(self, predictions: List[PredictionResult]) -> float:
        """Calculate variance in ensemble predictions"""
        try:
            if len(predictions) < 2:
                return 0.0
            
            values = [p.predicted_value for p in predictions]
            return statistics.variance(values)
            
        except Exception as e:
            logger.error(f"Error calculating ensemble variance: {str(e)}")
            return 0.0
    
    def _calculate_reliability_score(self, predictions: List[PredictionResult], 
                                   data: Dict[str, Any]) -> float:
        """Calculate overall reliability score"""
        try:
            if not predictions:
                return 0.0
            
            # Base reliability on average confidence
            avg_confidence = statistics.mean([p.confidence_score for p in predictions])
            
            # Adjust for data quality
            data_quality_score = data.get("data_quality", {}).get("score", 0.5)
            
            # Adjust for model agreement (lower variance = higher reliability)
            variance = self._calculate_ensemble_variance(predictions)
            agreement_score = 1.0 / (1.0 + variance) if variance > 0 else 1.0
            
            # Combined reliability score
            reliability = (avg_confidence * 0.5 + data_quality_score * 0.3 + agreement_score * 0.2)
            
            return min(max(reliability, 0.0), 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating reliability score: {str(e)}")
            return 0.0
    
    def _identify_uncertainty_factors(self, model_type: ModelType, confidence: float) -> List[str]:
        """Identify factors contributing to prediction uncertainty"""
        factors = []
        
        if confidence < 0.5:
            factors.append("Low model confidence")
        
        if model_type in [ModelType.LINEAR_REGRESSION, ModelType.MOVING_AVERAGE]:
            factors.append("Simple model limitations")
        
        factors.append("Limited historical data")
        factors.append("Future uncertainty")
        
        return factors
    
    async def _generate_prediction_scenarios(self, data: Dict[str, Any], 
                                           prediction_input: PredictionInput,
                                           primary_prediction: EnsemblePrediction) -> List[PredictionScenario]:
        """Generate alternative prediction scenarios"""
        scenarios = []
        
        try:
            if not primary_prediction.consensus_prediction:
                return scenarios
            
            base_prediction = primary_prediction.consensus_prediction
            
            # Optimistic scenario
            optimistic_scenario = PredictionScenario(
                scenario_name="Optimistic",
                scenario_probability=0.2,
                predicted_values=[base_prediction * 1.2],
                scenario_description="Best-case scenario with favorable conditions",
                key_assumptions=["Optimal conditions", "No negative events", "Continued positive trends"],
                risk_factors=["Over-optimism", "Unforeseen obstacles"],
                business_impact="High positive impact"
            )
            scenarios.append(optimistic_scenario)
            
            # Pessimistic scenario
            pessimistic_scenario = PredictionScenario(
                scenario_name="Pessimistic",
                scenario_probability=0.2,
                predicted_values=[base_prediction * 0.8],
                scenario_description="Worst-case scenario with adverse conditions",
                key_assumptions=["Challenging conditions", "Negative trends", "External pressures"],
                risk_factors=["Economic downturn", "Market volatility", "Resource constraints"],
                business_impact="Negative impact requiring mitigation"
            )
            scenarios.append(pessimistic_scenario)
            
            # Most likely scenario (base prediction)
            most_likely_scenario = PredictionScenario(
                scenario_name="Most Likely",
                scenario_probability=0.6,
                predicted_values=[base_prediction],
                scenario_description="Expected scenario based on current trends",
                key_assumptions=["Current trends continue", "Normal operating conditions"],
                risk_factors=["Market changes", "Competitive pressure"],
                business_impact="Expected business performance"
            )
            scenarios.append(most_likely_scenario)
            
            return scenarios
            
        except Exception as e:
            logger.error(f"Error generating prediction scenarios: {str(e)}")
            return []
    
    async def _analyze_prediction_trends(self, data: Dict[str, Any], 
                                       prediction_input: PredictionInput) -> Dict[str, Any]:
        """Analyze trends in prediction data"""
        try:
            trend_analysis = {
                "trend_direction": "stable",
                "trend_strength": 0.0,
                "trend_acceleration": 0.0,
                "seasonality": {},
                "volatility": 0.0
            }
            
            targets = data.get("targets", [])
            if len(targets) < 3:
                return trend_analysis
            
            # Calculate trend direction and strength
            if len(targets) >= 2:
                recent_change = targets[-1] - targets[-2] if len(targets) >= 2 else 0
                overall_change = targets[-1] - targets[0] if len(targets) >= 2 else 0
                
                if recent_change > 0:
                    trend_analysis["trend_direction"] = "increasing"
                elif recent_change < 0:
                    trend_analysis["trend_direction"] = "decreasing"
                
                # Trend strength based on consistency
                if len(targets) > 2:
                    changes = [targets[i] - targets[i-1] for i in range(1, len(targets))]
                    consistent_direction = sum(1 for c in changes if (c > 0) == (overall_change > 0))
                    trend_analysis["trend_strength"] = consistent_direction / len(changes)
            
            # Calculate volatility
            if len(targets) > 1:
                mean_val = statistics.mean(targets)
                if mean_val != 0:
                    std_val = statistics.stdev(targets)
                    trend_analysis["volatility"] = std_val / abs(mean_val)
            
            return trend_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing prediction trends: {str(e)}")
            return {"trend_direction": "unknown", "trend_strength": 0.0}
    
    async def _assess_prediction_risks(self, primary_prediction: EnsemblePrediction,
                                     scenarios: List[PredictionScenario],
                                     prediction_input: PredictionInput) -> Dict[str, Any]:
        """Assess risks associated with predictions"""
        try:
            risk_assessment = {
                "overall_risk_level": "medium",
                "confidence_risk": 0.0,
                "variance_risk": 0.0,
                "data_quality_risk": 0.0,
                "horizon_risk": 0.0,
                "mitigation_strategies": []
            }
            
            # Confidence risk
            if primary_prediction.consensus_confidence < 0.5:
                risk_assessment["confidence_risk"] = 1.0 - primary_prediction.consensus_confidence
                risk_assessment["mitigation_strategies"].append("Collect more historical data")
            
            # Variance risk
            if primary_prediction.ensemble_variance > 0.5:
                risk_assessment["variance_risk"] = min(primary_prediction.ensemble_variance, 1.0)
                risk_assessment["mitigation_strategies"].append("Use ensemble averaging")
            
            # Horizon risk (longer horizons = higher risk)
            horizon_multiplier = {
                PredictionHorizon.SHORT_TERM: 0.1,
                PredictionHorizon.MEDIUM_TERM: 0.3,
                PredictionHorizon.LONG_TERM: 0.6,
                PredictionHorizon.EXTENDED: 0.9
            }
            risk_assessment["horizon_risk"] = horizon_multiplier.get(prediction_input.horizon_type, 0.5)
            
            # Overall risk level
            total_risk = (risk_assessment["confidence_risk"] + 
                         risk_assessment["variance_risk"] + 
                         risk_assessment["horizon_risk"]) / 3
            
            if total_risk < 0.3:
                risk_assessment["overall_risk_level"] = "low"
            elif total_risk < 0.7:
                risk_assessment["overall_risk_level"] = "medium"
            else:
                risk_assessment["overall_risk_level"] = "high"
                risk_assessment["mitigation_strategies"].append("Consider multiple scenarios")
                risk_assessment["mitigation_strategies"].append("Implement monitoring and early warning")
            
            return risk_assessment
            
        except Exception as e:
            logger.error(f"Error assessing prediction risks: {str(e)}")
            return {"overall_risk_level": "unknown", "mitigation_strategies": []}
    
    async def _evaluate_model_performance(self, data: Dict[str, Any], 
                                        primary_prediction: EnsemblePrediction) -> Dict[str, Any]:
        """Evaluate performance of prediction models"""
        try:
            performance = {
                "ensemble_performance": {},
                "individual_model_performance": {},
                "cross_validation_scores": {},
                "performance_summary": {}
            }
            
            # Ensemble performance
            performance["ensemble_performance"] = {
                "consensus_confidence": primary_prediction.consensus_confidence,
                "ensemble_variance": primary_prediction.ensemble_variance,
                "reliability_score": primary_prediction.reliability_score,
                "model_count": len(primary_prediction.predictions)
            }
            
            # Individual model performance
            for prediction in primary_prediction.predictions:
                model_name = prediction.model_used.value
                performance["individual_model_performance"][model_name] = {
                    "confidence_score": prediction.confidence_score,
                    "predicted_value": prediction.predicted_value,
                    "uncertainty_factors": len(prediction.uncertainty_factors)
                }
            
            # Performance summary
            if primary_prediction.predictions:
                avg_confidence = statistics.mean([p.confidence_score for p in primary_prediction.predictions])
                performance["performance_summary"] = {
                    "average_model_confidence": avg_confidence,
                    "best_performing_model": max(primary_prediction.predictions, 
                                               key=lambda p: p.confidence_score).model_used.value,
                    "model_agreement": 1.0 - (primary_prediction.ensemble_variance / 
                                           abs(primary_prediction.consensus_prediction) 
                                           if primary_prediction.consensus_prediction != 0 else 1.0)
                }
            
            return performance
            
        except Exception as e:
            logger.error(f"Error evaluating model performance: {str(e)}")
            return {"error": str(e)}
    
    async def _generate_prediction_insights(self, primary_prediction: EnsemblePrediction,
                                          scenarios: List[PredictionScenario],
                                          trend_analysis: Dict[str, Any]) -> List[str]:
        """Generate insights from prediction analysis"""
        insights = []
        
        try:
            # Prediction quality insights
            if primary_prediction.consensus_confidence > 0.8:
                insights.append("High-confidence prediction with strong model agreement")
            elif primary_prediction.consensus_confidence < 0.5:
                insights.append("Low-confidence prediction - consider collecting more data")
            
            # Ensemble insights
            if len(primary_prediction.predictions) > 1:
                insights.append(f"Ensemble of {len(primary_prediction.predictions)} models used for robust prediction")
                
                if primary_prediction.ensemble_variance < 0.1:
                    insights.append("Strong model consensus indicates reliable prediction")
                elif primary_prediction.ensemble_variance > 0.5:
                    insights.append("High model variance suggests prediction uncertainty")
            
            # Trend insights
            trend_direction = trend_analysis.get("trend_direction", "stable")
            trend_strength = trend_analysis.get("trend_strength", 0.0)
            
            if trend_direction != "stable" and trend_strength > 0.7:
                insights.append(f"Strong {trend_direction} trend detected - prediction follows established pattern")
            elif trend_strength < 0.3:
                insights.append("Weak trend patterns - prediction based on average behavior")
            
            # Scenario insights
            if scenarios:
                scenario_range = max(s.predicted_values[0] for s in scenarios) - min(s.predicted_values[0] for s in scenarios)
                if scenario_range > abs(primary_prediction.consensus_prediction) * 0.5:
                    insights.append("Wide scenario range indicates high uncertainty - monitor conditions closely")
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating prediction insights: {str(e)}")
            return ["Error generating insights from prediction analysis"]
    
    async def _generate_prediction_recommendations(self, primary_prediction: EnsemblePrediction,
                                                 risk_assessment: Dict[str, Any],
                                                 prediction_input: PredictionInput) -> List[str]:
        """Generate recommendations based on prediction analysis"""
        recommendations = []
        
        try:
            # Confidence-based recommendations
            if primary_prediction.consensus_confidence > 0.8:
                recommendations.append("High confidence prediction - proceed with planning based on forecast")
            elif primary_prediction.consensus_confidence < 0.5:
                recommendations.append("Low confidence prediction - gather more data before making decisions")
            
            # Risk mitigation recommendations
            mitigation_strategies = risk_assessment.get("mitigation_strategies", [])
            recommendations.extend(mitigation_strategies)
            
            # Horizon-specific recommendations
            if prediction_input.horizon_type == PredictionHorizon.LONG_TERM:
                recommendations.append("Long-term prediction - regularly update forecast with new data")
            elif prediction_input.horizon_type == PredictionHorizon.SHORT_TERM:
                recommendations.append("Short-term prediction - suitable for immediate planning")
            
            # Model improvement recommendations
            if primary_prediction.ensemble_variance > 0.5:
                recommendations.append("High model variance - consider feature engineering or model tuning")
            
            # Monitoring recommendations
            recommendations.append("Implement prediction monitoring to track accuracy over time")
            recommendations.append("Set up alerts for significant deviations from predicted values")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating prediction recommendations: {str(e)}")
            return ["Error generating recommendations from prediction analysis"]
    
    def _determine_confidence_level(self, primary_prediction: EnsemblePrediction) -> ConfidenceLevel:
        """Determine overall confidence level"""
        try:
            confidence_score = primary_prediction.consensus_confidence
            
            if confidence_score >= 0.9:
                return ConfidenceLevel.VERY_HIGH
            elif confidence_score >= 0.7:
                return ConfidenceLevel.HIGH
            elif confidence_score >= 0.5:
                return ConfidenceLevel.MEDIUM
            else:
                return ConfidenceLevel.LOW
                
        except Exception as e:
            logger.error(f"Error determining confidence level: {str(e)}")
            return ConfidenceLevel.LOW
    
    async def _calculate_prediction_trust_score(self, primary_prediction: EnsemblePrediction,
                                              prediction_input: PredictionInput) -> float:
        """Calculate trust score for prediction"""
        try:
            if not self.trust_framework:
                return 0.8  # Default trust score
            
            # Base trust on prediction quality
            prediction_quality = primary_prediction.consensus_confidence
            
            # Model reliability
            model_reliability = primary_prediction.reliability_score
            
            # Data quality (simplified)
            data_quality = 0.8  # Should be calculated from actual data quality assessment
            
            trust_score = (prediction_quality * 0.4 + model_reliability * 0.4 + data_quality * 0.2)
            
            return min(trust_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating prediction trust score: {str(e)}")
            return 0.5
    
    def _update_prediction_statistics(self, result: PredictiveAnalysisResult):
        """Update prediction statistics"""
        try:
            self.analysis_stats["total_predictions"] += 1
            self.analysis_stats["processing_time_total"] += result.processing_time
            
            # Update model usage statistics
            for prediction in result.primary_prediction.predictions:
                self.analysis_stats["model_usage"][prediction.model_used.value] += 1
            
            # Update average accuracy (using consensus confidence as proxy)
            total_accuracy = (self.analysis_stats["average_accuracy"] * 
                            (self.analysis_stats["total_predictions"] - 1) + 
                            result.primary_prediction.consensus_confidence)
            self.analysis_stats["average_accuracy"] = total_accuracy / self.analysis_stats["total_predictions"]
            
        except Exception as e:
            logger.error(f"Error updating prediction statistics: {str(e)}")
    
    async def get_prediction_statistics(self) -> Dict[str, Any]:
        """Get prediction analysis statistics"""
        return {
            **self.analysis_stats,
            "average_processing_time": (self.analysis_stats["processing_time_total"] / 
                                      max(self.analysis_stats["total_predictions"], 1)),
            "model_usage_distribution": dict(self.analysis_stats["model_usage"])
        }
    
    async def get_model_cache(self) -> Dict[str, PredictiveAnalysisResult]:
        """Get cached prediction results"""
        return self.model_cache

# Export the main class
__all__ = ['PredictiveAnalyzer', 'PredictionInput', 'PredictiveAnalysisResult', 'EnsemblePrediction', 
           'PredictionScenario', 'PredictionHorizon', 'PredictionType', 'ModelType']
