"""
Universal MASS Framework - The jQuery of AI

A Universal Multi-Agent System Search (MASS) Framework that can integrate with ANY existing 
software system and make it exponentially smarter using real-world data intelligence.

This is the core module that provides:
- Real-world data orchestration from 100+ sources
- Universal system adapters for any integration
- Intelligence agents for analysis and prediction
- Enterprise-grade trust and compliance framework
- Human-in-the-loop controls and oversight
"""

__version__ = "1.0.0"
__author__ = "MASS Framework Team"

# Core exports
from .core.mass_engine import MassEngine
from .core.config_manager import MassConfig
from .universal_adapters.universal_adapter import UniversalAdapter
from .data_orchestration.real_world_data_orchestrator import RealWorldDataOrchestrator

# Intelligence Agents exports
from .intelligence_agents.data_analyzer_agent import DataAnalyzerAgent
from .intelligence_agents.predictive_agent import PredictiveAgent
from .intelligence_agents.optimization_agent import OptimizationAgent
from .intelligence_agents.anomaly_detector_agent import AnomalyDetectorAgent

# Enterprise Trust Framework
from .enterprise_trust.trusted_ai_framework import TrustedAIFramework

__all__ = [
    "MassEngine",
    "MassConfig", 
    "UniversalAdapter",
    "RealWorldDataOrchestrator",
    "DataAnalyzerAgent",
    "PredictiveAgent",
    "OptimizationAgent",
    "AnomalyDetectorAgent",
    "TrustedAIFramework"
]
