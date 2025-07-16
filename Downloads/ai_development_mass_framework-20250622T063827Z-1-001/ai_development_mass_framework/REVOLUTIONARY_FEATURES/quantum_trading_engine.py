#!/usr/bin/env python3
"""
Quantum Trading Engine - Top-Level Proxy
Imports and re-exports the QuantumTradingEngine from the quantum_trading submodule
"""

from .quantum_trading.quantum_trading_engine import QuantumTradingEngine

__all__ = ['QuantumTradingEngine'] 