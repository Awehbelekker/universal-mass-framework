#!/usr/bin/env python3
"""
Prometheus AI Integration - Top-Level Proxy
Imports and re-exports the PrometheusAIIntegration from the prometheus_ai submodule
"""

from .prometheus_ai.prometheus_ai_integration import PrometheusAIIntegration

__all__ = ['PrometheusAIIntegration'] 