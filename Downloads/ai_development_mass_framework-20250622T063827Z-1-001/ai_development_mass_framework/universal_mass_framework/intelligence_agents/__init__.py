"""
Intelligence Agents Module

This module contains universal AI agents that can analyze any data type,
detect patterns, predict outcomes, optimize processes, and provide recommendations.
"""

from .data_analyzer_agent import DataAnalyzerAgent
from .predictive_agent import PredictiveAgent
from .optimization_agent import OptimizationAgent
from .anomaly_detector_agent import AnomalyDetectorAgent
from .pattern_detector_agent import PatternDetectorAgent
from .recommendation_agent import RecommendationAgent

__all__ = [
    "DataAnalyzerAgent",
    "PredictiveAgent", 
    "OptimizationAgent",
    "AnomalyDetectorAgent",
    "PatternDetectorAgent",
    "RecommendationAgent"
]
