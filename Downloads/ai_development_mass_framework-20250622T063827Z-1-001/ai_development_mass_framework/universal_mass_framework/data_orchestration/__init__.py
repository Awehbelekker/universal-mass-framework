"""
Universal MASS Framework - Data Orchestration Module
===================================================

The "jQuery of AI" - Real-World Data Intelligence Engine

This module provides the core data orchestration capabilities that enable
the Universal MASS Framework to work with ANY data source in real-time.

Key Features:
- Universal data source integration (financial, social, IoT, web, etc.)
- Real-time data streaming and processing
- Intelligent data fusion and correlation
- Enterprise-grade security and compliance
- Automated data quality assessment
- Smart caching and optimization
- Conflict resolution and data reconciliation

The data orchestration layer is the foundation that makes any software
system exponentially smarter by providing real-world intelligence.

Usage:
    from universal_mass_framework.data_orchestration import RealWorldDataOrchestrator
    
    orchestrator = RealWorldDataOrchestrator()
    await orchestrator.initialize()
    
    # Get real-time intelligence for any context
    intelligence = await orchestrator.get_contextual_intelligence(
        context="financial_analysis",
        parameters={"symbol": "AAPL", "timeframe": "1d"}
    )

Components:
- RealWorldDataOrchestrator: Main orchestration engine
- DataSources: Financial, social, IoT, web, and more data sources
- DataProcessors: Real-time processing and analysis engines  
- DataValidators: Quality assessment and validation systems
- CacheManager: Intelligent caching and optimization
- SecurityManager: Enterprise-grade security and compliance
"""

from .real_world_data_orchestrator import RealWorldDataOrchestrator
from .data_sources import *
from .data_processors import *
from .data_validators import DataQualityValidator, SourceReliabilityValidator
from .cache_manager import IntelligentCacheManager
from .security_manager import DataSecurityManager

__all__ = [
    'RealWorldDataOrchestrator',
    'DataQualityValidator',
    'SourceReliabilityValidator', 
    'IntelligentCacheManager',
    'DataSecurityManager'
]

__version__ = "1.0.0"
__author__ = "Universal MASS Framework Team"
__description__ = "Real-World Data Intelligence Engine - The Foundation of Universal AI Integration"
