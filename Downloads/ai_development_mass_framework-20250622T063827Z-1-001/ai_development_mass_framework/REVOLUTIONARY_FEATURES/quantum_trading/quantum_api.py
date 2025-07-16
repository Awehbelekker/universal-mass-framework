import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Pydantic models for API
class PortfolioOptimizationRequest(BaseModel):
    assets: List[str]
    returns_data: List[List[float]]
    risk_free_rate: float = 0.02
    optimization_target: str = "sharpe_ratio"

class RiskOptimizationRequest(BaseModel):
    portfolio_data: Dict[str, Any]
    risk_metrics: List[str] = ["var", "cvar", "max_drawdown"]

class ArbitrageDetectionRequest(BaseModel):
    market_data: Dict[str, Any]
    detection_threshold: float = 0.001

class QuantumTradeRequest(BaseModel):
    symbol: str
    side: str
    quantity: float
    order_type: str = "market"
    price: Optional[float] = None

# Initialize quantum trading engine
from .quantum_trading_engine import QuantumTradingEngine

quantum_config = {
    'portfolio': {
        'max_qubits': 50,
        'optimization_level': 'high'
    },
    'risk': {
        'max_risk_qubits': 20
    },
    'arbitrage': {
        'detection_sensitivity': 0.001
    }
}

quantum_engine = QuantumTradingEngine(quantum_config)

# API Router
router = APIRouter(prefix="/quantum", tags=["quantum-trading"])

@router.post("/connect")
async def connect_quantum():
    """Connect to quantum computing resources"""
    try:
        success = await quantum_engine.connect()
        if success:
            return {"status": "connected", "message": "Successfully connected to quantum resources"}
        else:
            raise HTTPException(status_code=500, detail="Failed to connect to quantum resources")
    except Exception as e:
        logger.error(f"Quantum connection error: {e}")
        raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")

@router.post("/portfolio/optimize")
async def optimize_portfolio_quantum(request: PortfolioOptimizationRequest):
    """Optimize portfolio using quantum algorithms"""
    try:
        # Convert returns data to numpy array
        import numpy as np
        returns_array = np.array(request.returns_data)
        
        result = await quantum_engine.optimize_portfolio_quantum(
            request.assets, 
            returns_array, 
            request.risk_free_rate
        )
        
        if result['success']:
            return {
                "success": True,
                "optimization_id": result['optimization_id'],
                "optimal_weights": result['optimal_weights'],
                "expected_return": result['expected_return'],
                "sharpe_ratio": result['sharpe_ratio'],
                "quantum_advantage": result['quantum_advantage'],
                "execution_time_ms": result['execution_time_ms'],
                "confidence": result['confidence']
            }
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Portfolio optimization error: {e}")
        raise HTTPException(status_code=500, detail=f"Optimization error: {str(e)}")

@router.post("/risk/optimize")
async def optimize_risk_quantum(request: RiskOptimizationRequest):
    """Optimize risk using quantum algorithms"""
    try:
        result = await quantum_engine.optimize_risk_quantum(request.portfolio_data)
        
        if result['success']:
            return {
                "success": True,
                "optimization_id": result['optimization_id'],
                "var_95": result['var_95'],
                "cvar_95": result['cvar_95'],
                "max_drawdown": result['max_drawdown'],
                "risk_score": result['risk_score'],
                "quantum_advantage": result['quantum_advantage'],
                "execution_time_ms": result['execution_time_ms'],
                "confidence": result['confidence']
            }
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Risk optimization error: {e}")
        raise HTTPException(status_code=500, detail=f"Risk optimization error: {str(e)}")

@router.post("/arbitrage/detect")
async def detect_arbitrage_quantum(request: ArbitrageDetectionRequest):
    """Detect arbitrage opportunities using quantum algorithms"""
    try:
        result = await quantum_engine.detect_arbitrage_quantum(request.market_data)
        
        if result['success']:
            return {
                "success": True,
                "optimization_id": result['optimization_id'],
                "arbitrage_opportunities": result['arbitrage_opportunities'],
                "total_opportunities": result['total_opportunities'],
                "expected_profit": result['expected_profit'],
                "quantum_advantage": result['quantum_advantage'],
                "execution_time_ms": result['execution_time_ms'],
                "confidence": result['confidence']
            }
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Arbitrage detection error: {e}")
        raise HTTPException(status_code=500, detail=f"Arbitrage detection error: {str(e)}")

@router.post("/trade/execute")
async def execute_quantum_trade(request: QuantumTradeRequest):
    """Execute trade using quantum optimization"""
    try:
        order = {
            'id': f"quantum_order_{datetime.utcnow().timestamp()}",
            'symbol': request.symbol,
            'side': request.side,
            'quantity': request.quantity,
            'order_type': request.order_type,
            'price': request.price
        }
        
        result = await quantum_engine.execute_quantum_trade(order)
        
        if result['status'] == 'executed':
            return {
                "success": True,
                "order_id": result['order_id'],
                "status": result['status'],
                "quantum_optimization": result['quantum_optimization'],
                "execution_details": result['execution_details'],
                "quantum_advantage": result['quantum_advantage'],
                "execution_time_ms": result['execution_time_ms']
            }
        else:
            raise HTTPException(status_code=500, detail=result['error'])
            
    except Exception as e:
        logger.error(f"Quantum trade execution error: {e}")
        raise HTTPException(status_code=500, detail=f"Trade execution error: {str(e)}")

@router.get("/optimization/history")
async def get_optimization_history():
    """Get quantum optimization history"""
    try:
        history = await quantum_engine.get_optimization_history()
        return {
            "success": True,
            "history": history,
            "total_optimizations": len(history)
        }
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"History retrieval error: {str(e)}")

@router.get("/statistics")
async def get_quantum_statistics():
    """Get quantum computing statistics"""
    try:
        stats = await quantum_engine.get_quantum_statistics()
        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Statistics retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Statistics retrieval error: {str(e)}")

@router.get("/status")
async def get_quantum_status():
    """Get quantum system status"""
    try:
        stats = await quantum_engine.get_quantum_statistics()
        return {
            "connected": quantum_engine.connected,
            "total_optimizations": stats['total_optimizations'],
            "quantum_advantages": stats['quantum_advantages'],
            "advantage_rate": stats['advantage_rate'],
            "algorithms_used": stats['algorithms_used']
        }
    except Exception as e:
        logger.error(f"Status retrieval error: {e}")
        raise HTTPException(status_code=500, detail=f"Status retrieval error: {str(e)}") 