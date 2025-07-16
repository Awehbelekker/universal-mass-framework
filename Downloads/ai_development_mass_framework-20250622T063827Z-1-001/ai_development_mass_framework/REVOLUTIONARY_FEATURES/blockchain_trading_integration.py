#!/usr/bin/env python3
"""
Blockchain Trading Integration - Top-Level Proxy
Imports and re-exports the BlockchainTradingIntegration from the blockchain_trading submodule
"""

from .blockchain_trading.blockchain_trading_integration import BlockchainTradingIntegration

__all__ = ['BlockchainTradingIntegration'] 