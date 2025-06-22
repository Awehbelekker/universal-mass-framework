"""
Data Processors Module - Real-Time Intelligence Processing
=========================================================

This module provides advanced data processing capabilities for the
Universal MASS Framework, enabling real-time data transformation,
correlation, and insight generation.

Processors:
- RealTimeDataProcessor: Real-time data processing and transformation
- DataCorrelationEngine: Cross-source data correlation and pattern detection
- InsightGenerator: AI-powered insight generation and recommendation
- AnomalyDetector: Real-time anomaly detection and alerting
- PatternAnalyzer: Pattern recognition and trend analysis
- PredictiveAnalyzer: Predictive analytics and forecasting

Features:
- Real-time stream processing
- Advanced correlation algorithms
- Machine learning-powered insights
- Anomaly detection and alerting
- Pattern recognition and analysis
- Predictive analytics
- Natural language generation
"""

from .real_time_processor import RealTimeDataProcessor
from .correlation_engine import DataCorrelationEngine
from .insight_generator import InsightGenerator
from .anomaly_detector import AnomalyDetector
from .pattern_analyzer import PatternAnalyzer
from .predictive_analyzer import PredictiveAnalyzer

__all__ = [
    'RealTimeDataProcessor',
    'DataCorrelationEngine',
    'InsightGenerator',
    'AnomalyDetector',
    'PatternAnalyzer',
    'PredictiveAnalyzer'
]
