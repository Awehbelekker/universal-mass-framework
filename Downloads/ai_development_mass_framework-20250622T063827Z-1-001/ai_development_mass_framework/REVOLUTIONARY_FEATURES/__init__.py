# Revolutionary Features Module
# This module contains all revolutionary trading features

__version__ = "1.0.0"
__author__ = "Universal MASS Framework Team"

# Import all revolutionary features
from .quantum_trading.quantum_trading_engine import QuantumTradingEngine
from .blockchain_trading.blockchain_trading_integration import BlockchainTradingIntegration
from .neural_interface.neural_interface_integration import NeuralInterfaceIntegration
from .holographic_ui.holographic_ui_integration import HolographicUIIntegration
from .prometheus_ai.prometheus_ai_integration import PrometheusAIIntegration

__all__ = [
    'QuantumTradingEngine',
    'BlockchainTradingIntegration', 
    'NeuralInterfaceIntegration',
    'HolographicUIIntegration',
    'PrometheusAIIntegration'
] 