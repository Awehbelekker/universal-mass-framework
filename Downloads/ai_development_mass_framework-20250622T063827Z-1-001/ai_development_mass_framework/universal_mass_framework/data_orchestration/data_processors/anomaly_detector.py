"""
Universal MASS Framework - Anomaly Detector
==========================================

Advanced real-time anomaly detection engine for the Universal MASS Framework.
This component uses multiple algorithms to detect anomalies, outliers, and unusual
patterns across all data sources with confidence scoring and impact assessment.

Key Features:
- Multi-algorithm anomaly detection
- Real-time anomaly monitoring
- Statistical and ML-based detection
- Contextual anomaly analysis
- Adaptive threshold management
- Anomaly pattern recognition
"""

import asyncio
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Set, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import statistics
import json
from collections import deque, defaultdict
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class AnomalyType(Enum):
    """Types of anomalies that can be detected"""
    STATISTICAL = "statistical"
    TEMPORAL = "temporal"
    CONTEXTUAL = "contextual"
    COLLECTIVE = "collective"
    BEHAVIORAL = "behavioral"
    TREND = "trend"
    SEASONAL = "seasonal"
    THRESHOLD = "threshold"


class AnomalySeverity(Enum):
    """Severity levels for anomalies"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DetectionMethod(Enum):
    """Anomaly detection methods"""
    Z_SCORE = "z_score"
    IQR = "iqr"
    ISOLATION_FOREST = "isolation_forest"
    MOVING_AVERAGE = "moving_average"
    SEASONAL_DECOMPOSE = "seasonal_decompose"
    THRESHOLD_BASED = "threshold_based"
    MACHINE_LEARNING = "machine_learning"


@dataclass
class AnomalyDetection:
    """A detected anomaly with comprehensive metadata"""
    anomaly_id: str
    source: str
    metric: str
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    detection_method: DetectionMethod
    
    # Anomaly details
    value: float
    expected_value: float
    deviation: float
    deviation_percent: float
    confidence: float  # 0.0 to 1.0
    
    # Statistical information
    z_score: Optional[float] = None
    p_value: Optional[float] = None
    threshold_violated: Optional[Dict[str, Any]] = None
    
    # Context information
    timestamp: datetime = field(default_factory=datetime.utcnow)
    context: Dict[str, Any] = field(default_factory=dict)
    related_metrics: List[str] = field(default_factory=list)
    
    # Impact assessment
    impact_score: float = 0.0
    business_impact: str = ""
    recommended_actions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "anomaly_id": self.anomaly_id,
            "source": self.source,
            "metric": self.metric,
            "anomaly_type": self.anomaly_type.value,
            "severity": self.severity.value,
            "detection_method": self.detection_method.value,
            "value": self.value,
            "expected_value": self.expected_value,
            "deviation": self.deviation,
            "deviation_percent": self.deviation_percent,
            "confidence": self.confidence,
            "z_score": self.z_score,
            "p_value": self.p_value,
            "threshold_violated": self.threshold_violated,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context,
            "related_metrics": self.related_metrics,
            "impact_score": self.impact_score,
            "business_impact": self.business_impact,
            "recommended_actions": self.recommended_actions
        }


@dataclass
class AnomalyPattern:
    """Pattern of anomalies indicating systematic issues"""
    pattern_id: str
    pattern_type: str
    anomalies: List[AnomalyDetection]
    frequency: float
    confidence: float
    description: str
    potential_causes: List[str]
    recommendations: List[str]


class AnomalyDetectionEngine:
    """
    Universal Anomaly Detection Engine
    
    CAPABILITIES:
    - Real-time statistical anomaly detection
    - Machine learning-based anomaly detection
    - Contextual anomaly analysis
    - Multi-dimensional anomaly detection
    - Adaptive threshold management
    - Anomaly pattern recognition
    - Impact assessment and prioritization
    """
    
    def __init__(self, config=None):
        """Initialize the anomaly detection engine"""
        self.config = config
        self.anomaly_history = []
        self.detection_models = {}
        self.thresholds = defaultdict(dict)
        self.baseline_data = defaultdict(deque)
        self.anomaly_patterns = {}
        
        # Configuration
        self.window_size = 100  # Rolling window for baseline calculation
        self.min_data_points = 10  # Minimum points needed for detection
        self.confidence_threshold = 0.7  # Minimum confidence for reporting
        
        # Detection methods configuration
        self.detection_config = {
            DetectionMethod.Z_SCORE: {"threshold": 2.5, "enabled": True},
            DetectionMethod.IQR: {"multiplier": 1.5, "enabled": True},
            DetectionMethod.ISOLATION_FOREST: {"contamination": 0.1, "enabled": True},
            DetectionMethod.MOVING_AVERAGE: {"window": 20, "std_multiplier": 2.0, "enabled": True},
            DetectionMethod.THRESHOLD_BASED: {"enabled": True}
        }
        
        # Performance tracking
        self.detection_stats = {
            "anomalies_detected": 0,
            "false_positives": 0,
            "avg_confidence": 0.0,
            "processing_time": 0.0,
            "detection_rate": 0.0
        }
    
    async def detect_anomalies(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                             context: Dict[str, Any] = None) -> List[AnomalyDetection]:
        """
        Detect anomalies across multiple data sources
        
        Args:
            data_sets: Dictionary of data sources and their data
            context: Analysis context for contextual anomaly detection
            
        Returns:
            List of detected anomalies
        """
        start_time = datetime.utcnow()
        
        try:
            all_anomalies = []
            
            # Process each data source
            for source_name, data in data_sets.items():
                try:
                    source_anomalies = await self._detect_source_anomalies(source_name, data, context)
                    all_anomalies.extend(source_anomalies)
                except Exception as e:
                    logger.error(f"Error detecting anomalies in {source_name}: {str(e)}")
                    continue
            
            # Detect anomaly patterns
            patterns = await self._detect_anomaly_patterns(all_anomalies)
            
            # Filter and rank anomalies
            filtered_anomalies = self._filter_anomalies(all_anomalies)
            ranked_anomalies = self._rank_anomalies(filtered_anomalies)
            
            # Update models and baselines
            await self._update_models(data_sets)
            
            # Store anomalies in history
            self.anomaly_history.extend(ranked_anomalies)
            
            # Update statistics
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            self._update_detection_stats(ranked_anomalies, processing_time)
            
            logger.info(f"Detected {len(ranked_anomalies)} anomalies across {len(data_sets)} data sources")
            
            return ranked_anomalies
            
        except Exception as e:
            logger.error(f"Error in anomaly detection: {str(e)}")
            return []
    
    async def _detect_source_anomalies(self, source_name: str, data: List[Dict[str, Any]], 
                                     context: Dict[str, Any] = None) -> List[AnomalyDetection]:
        """Detect anomalies in a single data source"""
        anomalies = []
        
        # Extract metrics from data
        metrics = self._extract_metrics(data)
        
        for metric_name, values in metrics.items():
            if len(values) < self.min_data_points:
                continue
            
            # Update baseline data
            metric_key = f"{source_name}_{metric_name}"
            self.baseline_data[metric_key].extend(values)
            if len(self.baseline_data[metric_key]) > self.window_size:
                # Keep only recent data
                while len(self.baseline_data[metric_key]) > self.window_size:
                    self.baseline_data[metric_key].popleft()
            
            # Run different detection methods
            detection_results = []
            
            # Statistical methods
            if self.detection_config[DetectionMethod.Z_SCORE]["enabled"]:
                z_score_anomalies = await self._detect_z_score_anomalies(
                    source_name, metric_name, values, self.baseline_data[metric_key]
                )
                detection_results.extend(z_score_anomalies)
            
            if self.detection_config[DetectionMethod.IQR]["enabled"]:
                iqr_anomalies = await self._detect_iqr_anomalies(
                    source_name, metric_name, values, self.baseline_data[metric_key]
                )
                detection_results.extend(iqr_anomalies)
            
            # Machine learning methods
            if self.detection_config[DetectionMethod.ISOLATION_FOREST]["enabled"]:
                ml_anomalies = await self._detect_isolation_forest_anomalies(
                    source_name, metric_name, values, self.baseline_data[metric_key]
                )
                detection_results.extend(ml_anomalies)
            
            # Time series methods
            if self.detection_config[DetectionMethod.MOVING_AVERAGE]["enabled"]:
                ma_anomalies = await self._detect_moving_average_anomalies(
                    source_name, metric_name, values
                )
                detection_results.extend(ma_anomalies)
            
            # Threshold-based detection
            if self.detection_config[DetectionMethod.THRESHOLD_BASED]["enabled"]:
                threshold_anomalies = await self._detect_threshold_anomalies(
                    source_name, metric_name, values, context
                )
                detection_results.extend(threshold_anomalies)
            
            # Consolidate detections (multiple methods may detect same anomaly)
            consolidated = self._consolidate_detections(detection_results)
            anomalies.extend(consolidated)
        
        return anomalies
    
    async def _detect_z_score_anomalies(self, source: str, metric: str, values: List[float], 
                                       baseline: deque) -> List[AnomalyDetection]:
        """Detect anomalies using Z-score method"""
        anomalies = []
        
        if len(baseline) < self.min_data_points:
            return anomalies
        
        try:
            baseline_array = np.array(list(baseline))
            mean_val = np.mean(baseline_array)
            std_val = np.std(baseline_array)
            
            if std_val == 0:
                return anomalies
            
            threshold = self.detection_config[DetectionMethod.Z_SCORE]["threshold"]
            
            for i, value in enumerate(values[-5:]):  # Check recent values
                z_score = abs((value - mean_val) / std_val)
                
                if z_score > threshold:
                    confidence = min(0.95, z_score / 5.0)
                    
                    if confidence >= self.confidence_threshold:
                        deviation = value - mean_val
                        deviation_percent = (deviation / abs(mean_val)) * 100 if mean_val != 0 else 0
                        
                        anomaly = AnomalyDetection(
                            anomaly_id=f"zscore_{source}_{metric}_{int(datetime.utcnow().timestamp())}_{i}",
                            source=source,
                            metric=metric,
                            anomaly_type=AnomalyType.STATISTICAL,
                            severity=self._determine_severity(z_score, "z_score"),
                            detection_method=DetectionMethod.Z_SCORE,
                            value=value,
                            expected_value=mean_val,
                            deviation=deviation,
                            deviation_percent=abs(deviation_percent),
                            confidence=confidence,
                            z_score=z_score,
                            p_value=2 * (1 - stats.norm.cdf(abs(z_score))),
                            impact_score=min(1.0, z_score / 5.0),
                            business_impact=self._assess_business_impact(source, metric, z_score),
                            recommended_actions=self._generate_anomaly_actions(source, metric, z_score)
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in Z-score detection for {source}.{metric}: {str(e)}")
            return []
    
    async def _detect_iqr_anomalies(self, source: str, metric: str, values: List[float], 
                                  baseline: deque) -> List[AnomalyDetection]:
        """Detect anomalies using Interquartile Range (IQR) method"""
        anomalies = []
        
        if len(baseline) < self.min_data_points:
            return anomalies
        
        try:
            baseline_array = np.array(list(baseline))
            q1 = np.percentile(baseline_array, 25)
            q3 = np.percentile(baseline_array, 75)
            iqr = q3 - q1
            
            multiplier = self.detection_config[DetectionMethod.IQR]["multiplier"]
            lower_bound = q1 - (multiplier * iqr)
            upper_bound = q3 + (multiplier * iqr)
            
            for i, value in enumerate(values[-5:]):
                if value < lower_bound or value > upper_bound:
                    # Calculate confidence based on how far outside bounds
                    if value < lower_bound:
                        distance = abs(value - lower_bound)
                        expected = q1
                    else:
                        distance = abs(value - upper_bound)
                        expected = q3
                    
                    confidence = min(0.95, distance / (iqr + 1))
                    
                    if confidence >= self.confidence_threshold:
                        deviation = value - expected
                        deviation_percent = (abs(deviation) / abs(expected)) * 100 if expected != 0 else 0
                        
                        anomaly = AnomalyDetection(
                            anomaly_id=f"iqr_{source}_{metric}_{int(datetime.utcnow().timestamp())}_{i}",
                            source=source,
                            metric=metric,
                            anomaly_type=AnomalyType.STATISTICAL,
                            severity=self._determine_severity(confidence, "confidence"),
                            detection_method=DetectionMethod.IQR,
                            value=value,
                            expected_value=expected,
                            deviation=deviation,
                            deviation_percent=deviation_percent,
                            confidence=confidence,
                            threshold_violated={
                                "lower_bound": lower_bound,
                                "upper_bound": upper_bound,
                                "iqr": iqr
                            },
                            impact_score=confidence,
                            business_impact=self._assess_business_impact(source, metric, confidence * 5),
                            recommended_actions=self._generate_anomaly_actions(source, metric, confidence * 5)
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in IQR detection for {source}.{metric}: {str(e)}")
            return []
    
    async def _detect_isolation_forest_anomalies(self, source: str, metric: str, values: List[float], 
                                               baseline: deque) -> List[AnomalyDetection]:
        """Detect anomalies using Isolation Forest machine learning method"""
        anomalies = []
        
        if len(baseline) < 20:  # Need more data for ML methods
            return anomalies
        
        try:
            # Prepare data
            baseline_array = np.array(list(baseline)).reshape(-1, 1)
            recent_values = np.array(values[-5:]).reshape(-1, 1)
            
            # Train isolation forest
            contamination = self.detection_config[DetectionMethod.ISOLATION_FOREST]["contamination"]
            model = IsolationForest(contamination=contamination, random_state=42)
            model.fit(baseline_array)
            
            # Predict anomalies
            predictions = model.predict(recent_values)
            scores = model.score_samples(recent_values)
            
            for i, (prediction, score, value) in enumerate(zip(predictions, scores, values[-5:])):
                if prediction == -1:  # Anomaly detected
                    # Convert isolation forest score to confidence
                    confidence = min(0.95, abs(score) * 2)
                    
                    if confidence >= self.confidence_threshold:
                        expected = np.mean(baseline_array)
                        deviation = value - expected
                        deviation_percent = (abs(deviation) / abs(expected)) * 100 if expected != 0 else 0
                        
                        anomaly = AnomalyDetection(
                            anomaly_id=f"iforest_{source}_{metric}_{int(datetime.utcnow().timestamp())}_{i}",
                            source=source,
                            metric=metric,
                            anomaly_type=AnomalyType.BEHAVIORAL,
                            severity=self._determine_severity(confidence, "confidence"),
                            detection_method=DetectionMethod.ISOLATION_FOREST,
                            value=value,
                            expected_value=expected,
                            deviation=deviation,
                            deviation_percent=deviation_percent,
                            confidence=confidence,
                            context={"isolation_score": float(score)},
                            impact_score=confidence,
                            business_impact=self._assess_business_impact(source, metric, confidence * 5),
                            recommended_actions=self._generate_anomaly_actions(source, metric, confidence * 5)
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in Isolation Forest detection for {source}.{metric}: {str(e)}")
            return []
    
    async def _detect_moving_average_anomalies(self, source: str, metric: str, 
                                             values: List[float]) -> List[AnomalyDetection]:
        """Detect anomalies using moving average method"""
        anomalies = []
        
        if len(values) < 20:
            return anomalies
        
        try:
            window = self.detection_config[DetectionMethod.MOVING_AVERAGE]["window"]
            std_multiplier = self.detection_config[DetectionMethod.MOVING_AVERAGE]["std_multiplier"]
            
            # Calculate moving averages and standard deviations
            values_array = np.array(values)
            
            for i in range(window, len(values)):
                window_data = values_array[i-window:i]
                moving_avg = np.mean(window_data)
                moving_std = np.std(window_data)
                
                current_value = values_array[i]
                
                if moving_std > 0:
                    deviation = abs(current_value - moving_avg)
                    threshold = std_multiplier * moving_std
                    
                    if deviation > threshold:
                        confidence = min(0.95, deviation / (threshold * 2))
                        
                        if confidence >= self.confidence_threshold:
                            deviation_percent = (deviation / abs(moving_avg)) * 100 if moving_avg != 0 else 0
                            
                            anomaly = AnomalyDetection(
                                anomaly_id=f"ma_{source}_{metric}_{int(datetime.utcnow().timestamp())}_{i}",
                                source=source,
                                metric=metric,
                                anomaly_type=AnomalyType.TEMPORAL,
                                severity=self._determine_severity(confidence, "confidence"),
                                detection_method=DetectionMethod.MOVING_AVERAGE,
                                value=current_value,
                                expected_value=moving_avg,
                                deviation=current_value - moving_avg,
                                deviation_percent=deviation_percent,
                                confidence=confidence,
                                context={
                                    "window_size": window,
                                    "moving_std": moving_std,
                                    "threshold": threshold
                                },
                                impact_score=confidence,
                                business_impact=self._assess_business_impact(source, metric, confidence * 5),
                                recommended_actions=self._generate_anomaly_actions(source, metric, confidence * 5)
                            )
                            anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error in moving average detection for {source}.{metric}: {str(e)}")
            return []
    
    async def _detect_threshold_anomalies(self, source: str, metric: str, values: List[float], 
                                        context: Dict[str, Any] = None) -> List[AnomalyDetection]:
        """Detect anomalies using predefined thresholds"""
        anomalies = []
        
        # Get thresholds for this metric
        metric_key = f"{source}_{metric}"
        thresholds = self.thresholds.get(metric_key, {})
        
        if not thresholds:
            # Auto-generate thresholds based on historical data
            thresholds = self._auto_generate_thresholds(values)
            self.thresholds[metric_key] = thresholds
        
        for i, value in enumerate(values[-5:]):
            violated_thresholds = []
            
            for threshold_name, threshold_config in thresholds.items():
                if self._check_threshold_violation(value, threshold_config):
                    violated_thresholds.append({
                        "name": threshold_name,
                        "config": threshold_config,
                        "violation_type": self._get_violation_type(value, threshold_config)
                    })
            
            if violated_thresholds:
                # Create anomaly for threshold violations
                most_severe = max(violated_thresholds, key=lambda x: x["config"].get("severity", 0.5))
                confidence = most_severe["config"].get("confidence", 0.8)
                
                expected = most_severe["config"].get("expected", np.mean(values))
                deviation = value - expected
                deviation_percent = (abs(deviation) / abs(expected)) * 100 if expected != 0 else 0
                
                anomaly = AnomalyDetection(
                    anomaly_id=f"threshold_{source}_{metric}_{int(datetime.utcnow().timestamp())}_{i}",
                    source=source,
                    metric=metric,
                    anomaly_type=AnomalyType.THRESHOLD,
                    severity=AnomalySeverity(most_severe["config"].get("severity_level", "medium")),
                    detection_method=DetectionMethod.THRESHOLD_BASED,
                    value=value,
                    expected_value=expected,
                    deviation=deviation,
                    deviation_percent=deviation_percent,
                    confidence=confidence,
                    threshold_violated={
                        "violated_thresholds": violated_thresholds,
                        "most_severe": most_severe
                    },
                    impact_score=most_severe["config"].get("impact", 0.5),
                    business_impact=self._assess_business_impact(source, metric, confidence * 5),
                    recommended_actions=self._generate_threshold_actions(violated_thresholds, metric)
                )
                anomalies.append(anomaly)
        
        return anomalies
    
    def _extract_metrics(self, data: List[Dict[str, Any]]) -> Dict[str, List[float]]:
        """Extract numeric metrics from data"""
        metrics = defaultdict(list)
        
        for item in data:
            for key, value in item.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    metrics[key].append(float(value))
        
        return dict(metrics)
    
    def _consolidate_detections(self, detections: List[AnomalyDetection]) -> List[AnomalyDetection]:
        """Consolidate multiple detections of the same anomaly"""
        if not detections:
            return []
        
        # Group by value and timestamp (similar anomalies)
        groups = defaultdict(list)
        
        for detection in detections:
            key = f"{detection.value:.6f}_{detection.timestamp.isoformat()[:19]}"
            groups[key].append(detection)
        
        consolidated = []
        
        for group in groups.values():
            if len(group) == 1:
                consolidated.append(group[0])
            else:
                # Merge multiple detections
                best_detection = max(group, key=lambda x: x.confidence)
                
                # Combine detection methods
                methods = [d.detection_method.value for d in group]
                best_detection.context["detection_methods"] = methods
                best_detection.context["detection_count"] = len(group)
                
                # Average confidence
                best_detection.confidence = sum(d.confidence for d in group) / len(group)
                
                consolidated.append(best_detection)
        
        return consolidated
    
    def _determine_severity(self, value: float, value_type: str) -> AnomalySeverity:
        """Determine severity based on detection value"""
        if value_type == "z_score":
            if value > 4:
                return AnomalySeverity.CRITICAL
            elif value > 3:
                return AnomalySeverity.HIGH
            elif value > 2.5:
                return AnomalySeverity.MEDIUM
            else:
                return AnomalySeverity.LOW
        elif value_type == "confidence":
            if value > 0.9:
                return AnomalySeverity.CRITICAL
            elif value > 0.8:
                return AnomalySeverity.HIGH
            elif value > 0.7:
                return AnomalySeverity.MEDIUM
            else:
                return AnomalySeverity.LOW
        else:
            return AnomalySeverity.MEDIUM
    
    def _assess_business_impact(self, source: str, metric: str, severity_score: float) -> str:
        """Assess business impact of anomaly"""
        impact_keywords = {
            "revenue": "Direct revenue impact",
            "cost": "Cost efficiency impact",
            "performance": "System performance impact",
            "user": "User experience impact",
            "error": "Service reliability impact",
            "latency": "Response time impact",
            "throughput": "Capacity impact"
        }
        
        metric_lower = metric.lower()
        source_lower = source.lower()
        
        for keyword, impact in impact_keywords.items():
            if keyword in metric_lower or keyword in source_lower:
                if severity_score > 4:
                    return f"Critical {impact.lower()}"
                elif severity_score > 3:
                    return f"High {impact.lower()}"
                elif severity_score > 2:
                    return f"Medium {impact.lower()}"
                else:
                    return f"Low {impact.lower()}"
        
        return "Unknown business impact - requires investigation"
    
    def _generate_anomaly_actions(self, source: str, metric: str, severity_score: float) -> List[str]:
        """Generate recommended actions for anomaly"""
        actions = [
            f"Investigate {metric} anomaly in {source}",
            "Check for data quality issues",
            "Review system logs for errors"
        ]
        
        if severity_score > 4:
            actions.extend([
                "Escalate to operations team immediately",
                "Consider emergency response procedures",
                "Notify stakeholders"
            ])
        elif severity_score > 3:
            actions.extend([
                "Alert relevant team",
                "Monitor closely for additional anomalies",
                "Review recent changes"
            ])
        
        return actions
    
    def _generate_threshold_actions(self, violated_thresholds: List[Dict[str, Any]], metric: str) -> List[str]:
        """Generate actions for threshold violations"""
        actions = [f"Address {metric} threshold violations"]
        
        for violation in violated_thresholds:
            action = violation["config"].get("action", f"Review {violation['name']} threshold")
            actions.append(action)
        
        return actions
    
    def _auto_generate_thresholds(self, values: List[float]) -> Dict[str, Dict[str, Any]]:
        """Auto-generate thresholds based on data distribution"""
        if len(values) < 10:
            return {}
        
        values_array = np.array(values)
        mean_val = np.mean(values_array)
        std_val = np.std(values_array)
        
        thresholds = {
            "upper_warning": {
                "type": "upper",
                "value": mean_val + 2 * std_val,
                "severity": 0.6,
                "severity_level": "medium",
                "confidence": 0.8,
                "expected": mean_val,
                "impact": 0.6,
                "action": "Monitor closely"
            },
            "upper_critical": {
                "type": "upper",
                "value": mean_val + 3 * std_val,
                "severity": 0.9,
                "severity_level": "high",
                "confidence": 0.9,
                "expected": mean_val,
                "impact": 0.9,
                "action": "Immediate investigation required"
            },
            "lower_warning": {
                "type": "lower",
                "value": mean_val - 2 * std_val,
                "severity": 0.6,
                "severity_level": "medium",
                "confidence": 0.8,
                "expected": mean_val,
                "impact": 0.6,
                "action": "Monitor closely"
            },
            "lower_critical": {
                "type": "lower",
                "value": mean_val - 3 * std_val,
                "severity": 0.9,
                "severity_level": "high",
                "confidence": 0.9,
                "expected": mean_val,
                "impact": 0.9,
                "action": "Immediate investigation required"
            }
        }
        
        return thresholds
    
    def _check_threshold_violation(self, value: float, threshold_config: Dict[str, Any]) -> bool:
        """Check if value violates threshold"""
        threshold_type = threshold_config.get("type", "upper")
        threshold_value = threshold_config.get("value", 0)
        
        if threshold_type == "upper":
            return value > threshold_value
        elif threshold_type == "lower":
            return value < threshold_value
        elif threshold_type == "range":
            min_val = threshold_config.get("min", float('-inf'))
            max_val = threshold_config.get("max", float('inf'))
            return value < min_val or value > max_val
        
        return False
    
    def _get_violation_type(self, value: float, threshold_config: Dict[str, Any]) -> str:
        """Get type of threshold violation"""
        threshold_type = threshold_config.get("type", "upper")
        threshold_value = threshold_config.get("value", 0)
        
        if threshold_type == "upper" and value > threshold_value:
            return "exceeded_upper_limit"
        elif threshold_type == "lower" and value < threshold_value:
            return "below_lower_limit"
        elif threshold_type == "range":
            min_val = threshold_config.get("min", float('-inf'))
            max_val = threshold_config.get("max", float('inf'))
            if value < min_val:
                return "below_range"
            elif value > max_val:
                return "above_range"
        
        return "unknown_violation"
    
    def _filter_anomalies(self, anomalies: List[AnomalyDetection]) -> List[AnomalyDetection]:
        """Filter anomalies based on confidence and relevance"""
        return [
            anomaly for anomaly in anomalies 
            if anomaly.confidence >= self.confidence_threshold
        ]
    
    def _rank_anomalies(self, anomalies: List[AnomalyDetection]) -> List[AnomalyDetection]:
        """Rank anomalies by severity and impact"""
        severity_weights = {
            AnomalySeverity.CRITICAL: 4,
            AnomalySeverity.HIGH: 3,
            AnomalySeverity.MEDIUM: 2,
            AnomalySeverity.LOW: 1
        }
        
        return sorted(anomalies, key=lambda x: (
            severity_weights.get(x.severity, 0),
            x.impact_score,
            x.confidence
        ), reverse=True)
    
    async def _detect_anomaly_patterns(self, anomalies: List[AnomalyDetection]) -> List[AnomalyPattern]:
        """Detect patterns in anomalies"""
        patterns = []
        
        if len(anomalies) < 2:
            return patterns
        
        # Group anomalies by source and time
        source_groups = defaultdict(list)
        
        for anomaly in anomalies:
            source_groups[anomaly.source].append(anomaly)
        
        # Detect frequent anomalies in same source
        for source, source_anomalies in source_groups.items():
            if len(source_anomalies) >= 3:
                pattern = AnomalyPattern(
                    pattern_id=f"frequent_{source}_{int(datetime.utcnow().timestamp())}",
                    pattern_type="frequent_anomalies",
                    anomalies=source_anomalies,
                    frequency=len(source_anomalies),
                    confidence=min(0.95, len(source_anomalies) / 10),
                    description=f"Frequent anomalies detected in {source}",
                    potential_causes=[
                        f"Systematic issue in {source}",
                        "Data quality problems",
                        "Configuration issues"
                    ],
                    recommendations=[
                        f"Investigate {source} for underlying issues",
                        "Review data pipeline",
                        "Check system configuration"
                    ]
                )
                patterns.append(pattern)
        
        return patterns
    
    async def _update_models(self, data_sets: Dict[str, List[Dict[str, Any]]]):
        """Update detection models with new data"""
        try:
            # Update baseline data and retrain models if needed
            for source_name, data in data_sets.items():
                metrics = self._extract_metrics(data)
                
                for metric_name, values in metrics.items():
                    metric_key = f"{source_name}_{metric_name}"
                    
                    # Update Isolation Forest model if we have enough data
                    if len(self.baseline_data[metric_key]) > 50:
                        baseline_array = np.array(list(self.baseline_data[metric_key])).reshape(-1, 1)
                        
                        model = IsolationForest(
                            contamination=self.detection_config[DetectionMethod.ISOLATION_FOREST]["contamination"],
                            random_state=42
                        )
                        model.fit(baseline_array)
                        self.detection_models[metric_key] = model
        
        except Exception as e:
            logger.error(f"Error updating models: {str(e)}")
    
    def _update_detection_stats(self, anomalies: List[AnomalyDetection], processing_time: float):
        """Update detection statistics"""
        self.detection_stats["anomalies_detected"] += len(anomalies)
        self.detection_stats["processing_time"] = processing_time
        
        if anomalies:
            avg_confidence = sum(a.confidence for a in anomalies) / len(anomalies)
            
            # Update running average
            total_anomalies = self.detection_stats["anomalies_detected"]
            prev_avg = self.detection_stats["avg_confidence"]
            
            self.detection_stats["avg_confidence"] = (
                (prev_avg * (total_anomalies - len(anomalies))) + (avg_confidence * len(anomalies))
            ) / total_anomalies
    
    async def get_anomaly_summary(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get summary of detected anomalies"""
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        recent_anomalies = [
            anomaly for anomaly in self.anomaly_history 
            if anomaly.timestamp >= cutoff_time
        ]
        
        if not recent_anomalies:
            return {
                "summary": "No recent anomalies detected",
                "time_window_hours": time_window_hours,
                "total_anomalies": 0
            }
        
        # Calculate summary statistics
        severities = [anomaly.severity.value for anomaly in recent_anomalies]
        types = [anomaly.anomaly_type.value for anomaly in recent_anomalies]
        methods = [anomaly.detection_method.value for anomaly in recent_anomalies]
        
        return {
            "time_window_hours": time_window_hours,
            "total_anomalies": len(recent_anomalies),
            "severity_distribution": {s.value: severities.count(s.value) for s in AnomalySeverity},
            "type_distribution": {t.value: types.count(t.value) for t in AnomalyType},
            "method_distribution": {m.value: methods.count(m.value) for m in DetectionMethod},
            "average_confidence": sum(a.confidence for a in recent_anomalies) / len(recent_anomalies),
            "average_impact_score": sum(a.impact_score for a in recent_anomalies) / len(recent_anomalies),
            "detection_stats": self.detection_stats.copy()
        }
    
    async def set_custom_threshold(self, source: str, metric: str, threshold_config: Dict[str, Any]):
        """Set custom threshold for a metric"""
        metric_key = f"{source}_{metric}"
        threshold_name = threshold_config.get("name", "custom")
        
        if metric_key not in self.thresholds:
            self.thresholds[metric_key] = {}
        
        self.thresholds[metric_key][threshold_name] = threshold_config
        
        logger.info(f"Set custom threshold for {metric_key}: {threshold_config}")
    
    async def get_threshold_violations(self, time_window_hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent threshold violations"""
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        
        threshold_anomalies = [
            anomaly for anomaly in self.anomaly_history 
            if anomaly.timestamp >= cutoff_time 
            and anomaly.detection_method == DetectionMethod.THRESHOLD_BASED
        ]
        
        return [anomaly.to_dict() for anomaly in threshold_anomalies]


# Export the main classes
__all__ = ['AnomalyDetectionEngine', 'AnomalyDetection', 'AnomalyPattern', 'AnomalyType', 'AnomalySeverity', 'DetectionMethod']

AnomalyDetector = AnomalyDetectionEngine
