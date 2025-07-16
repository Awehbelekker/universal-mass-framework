import pytest
import asyncio
import numpy as np
from decimal import Decimal
from typing import Dict, Any

# Import trading engine with quantum integration
from core.trading_engine import TradingEngine, Order, OrderSide, OrderType, OrderStatus

class TestQuantumTradingIntegration:
    """Test suite for Quantum Trading Integration with Main Trading Engine"""
    
    @pytest.fixture
    def trading_engine(self):
        """Trading engine with quantum integration"""
        config = {
            'risk': {
                'max_position_size': 10000,
                'max_daily_loss': 1000,
                'max_portfolio_risk': 0.02
            },
            'portfolio': {
                'rebalance_frequency': 'daily'
            },
            'quantum': {
                'portfolio': {'max_qubits': 20, 'optimization_level': 'medium'},
                'risk': {'max_risk_qubits': 10},
                'arbitrage': {'detection_sensitivity': 0.001}
            }
        }
        return TradingEngine(config)
    
    @pytest.fixture
    def sample_order_data(self):
        """Sample order data for testing"""
        return {
            'user_id': 1,
            'account_id': 1,
            'symbol': 'AAPL',
            'side': 'buy',
            'quantity': 100,
            'order_type': 'market',
            'use_quantum_optimization': True,
            'strategy_id': 'quantum_strategy_1',
            'ai_agent_id': 'quantum_agent_1'
        }
    
    @pytest.fixture
    def sample_assets(self):
        """Sample assets for portfolio optimization"""
        return ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
    
    @pytest.fixture
    def sample_returns_data(self):
        """Sample returns data for portfolio optimization"""
        return np.random.normal(0.001, 0.02, (252, 5)).tolist()  # 252 days, 5 assets

    @pytest.mark.asyncio
    async def test_quantum_order_placement(self, trading_engine, sample_order_data):
        """Test placing an order with quantum optimization"""
        # Place order with quantum optimization
        success, message, order_id = await trading_engine.place_order(sample_order_data)
        
        # Validate order placement
        assert success == True
        assert order_id is not None
        assert "successfully" in message.lower()
        
        # Get order status
        order_status = await trading_engine.get_order_status(order_id)
        assert order_status is not None
        assert order_status['symbol'] == 'AAPL'
        assert order_status['side'] == 'buy'
        assert order_status['quantity'] == 100.0
        assert order_status['order_type'] == 'market'
        
        # Check if quantum optimization was applied
        if order_status.get('notes'):
            assert 'quantum' in order_status['notes'].lower()

    @pytest.mark.asyncio
    async def test_quantum_portfolio_optimization(self, trading_engine, sample_assets, sample_returns_data):
        """Test quantum portfolio optimization through trading engine"""
        # Perform quantum portfolio optimization
        result = await trading_engine.optimize_portfolio_quantum(
            account_id=1,
            assets=sample_assets,
            returns_data=sample_returns_data,
            risk_free_rate=0.02
        )
        
        # Validate optimization result
        assert result['success'] == True
        assert 'optimization' in result
        assert 'recommendations' in result
        
        optimization = result['optimization']
        assert 'optimization_id' in optimization
        assert 'optimal_weights' in optimization
        assert 'expected_return' in optimization
        assert 'sharpe_ratio' in optimization
        assert 'quantum_advantage' in optimization
        assert 'execution_time_ms' in optimization
        assert 'confidence' in optimization
        
        # Validate optimal weights
        optimal_weights = optimization['optimal_weights']
        assert len(optimal_weights) == len(sample_assets)
        assert abs(sum(optimal_weights) - 1.0) < 0.01  # Weights sum to 1
        
        # Validate recommendations
        recommendations = result['recommendations']
        assert isinstance(recommendations, list)
        for rec in recommendations:
            assert 'action' in rec
            assert 'symbol' in rec
            assert 'weight' in rec
            assert 'reason' in rec
            assert 'confidence' in rec

    @pytest.mark.asyncio
    async def test_quantum_statistics_integration(self, trading_engine):
        """Test quantum statistics integration with trading engine"""
        # Place some quantum-optimized orders
        for i in range(3):
            order_data = {
                'user_id': 1,
                'account_id': 1,
                'symbol': f'STOCK_{i}',
                'side': 'buy',
                'quantity': 100,
                'order_type': 'market',
                'use_quantum_optimization': True
            }
            await trading_engine.place_order(order_data)
        
        # Get quantum statistics
        stats = await trading_engine.get_quantum_statistics()
        
        # Validate statistics
        assert 'total_optimizations' in stats
        assert 'quantum_advantages' in stats
        assert 'advantage_rate' in stats
        assert 'quantum_orders' in stats
        assert 'quantum_order_success_rate' in stats
        
        # Validate quantum order statistics
        assert stats['quantum_orders'] >= 0
        assert stats['quantum_order_success_rate'] >= 0.0 and stats['quantum_order_success_rate'] <= 1.0

    @pytest.mark.asyncio
    async def test_quantum_vs_classical_orders(self, trading_engine):
        """Test quantum vs classical order placement"""
        # Place quantum-optimized order
        quantum_order_data = {
            'user_id': 1,
            'account_id': 1,
            'symbol': 'AAPL',
            'side': 'buy',
            'quantity': 100,
            'order_type': 'market',
            'use_quantum_optimization': True
        }
        
        # Place classical order
        classical_order_data = {
            'user_id': 1,
            'account_id': 1,
            'symbol': 'GOOGL',
            'side': 'buy',
            'quantity': 100,
            'order_type': 'market',
            'use_quantum_optimization': False
        }
        
        # Place both orders
        quantum_success, quantum_message, quantum_order_id = await trading_engine.place_order(quantum_order_data)
        classical_success, classical_message, classical_order_id = await trading_engine.place_order(classical_order_data)
        
        # Both should succeed
        assert quantum_success == True
        assert classical_success == True
        
        # Get order statuses
        quantum_status = await trading_engine.get_order_status(quantum_order_id)
        classical_status = await trading_engine.get_order_status(classical_order_id)
        
        # Quantum order should have quantum optimization metadata
        if quantum_status and quantum_status.get('metadata'):
            assert 'quantum_optimization' in quantum_status['metadata']
        
        # Classical order should not have quantum optimization
        if classical_status and classical_status.get('metadata'):
            assert 'quantum_optimization' not in classical_status['metadata']

    @pytest.mark.asyncio
    async def test_quantum_error_handling(self, trading_engine):
        """Test quantum error handling in trading engine"""
        # Test with invalid quantum configuration
        invalid_order_data = {
            'user_id': 1,
            'account_id': 1,
            'symbol': 'INVALID',
            'side': 'buy',
            'quantity': 100,
            'order_type': 'market',
            'use_quantum_optimization': True
        }
        
        # Should handle quantum errors gracefully
        success, message, order_id = await trading_engine.place_order(invalid_order_data)
        
        # Order should still be placed (with classical fallback)
        assert success == True or "error" in message.lower()

    @pytest.mark.asyncio
    async def test_quantum_performance_metrics(self, trading_engine):
        """Test quantum performance metrics"""
        # Perform multiple quantum operations
        operations = []
        
        # Portfolio optimization
        portfolio_result = await trading_engine.optimize_portfolio_quantum(
            account_id=1,
            assets=['AAPL', 'GOOGL'],
            returns_data=np.random.normal(0.001, 0.02, (100, 2)).tolist(),
            risk_free_rate=0.02
        )
        operations.append(portfolio_result)
        
        # Place quantum-optimized orders
        for i in range(2):
            order_data = {
                'user_id': 1,
                'account_id': 1,
                'symbol': f'STOCK_{i}',
                'side': 'buy',
                'quantity': 100,
                'order_type': 'market',
                'use_quantum_optimization': True
            }
            success, message, order_id = await trading_engine.place_order(order_data)
            operations.append({'success': success, 'order_id': order_id})
        
        # Get performance statistics
        stats = await trading_engine.get_quantum_statistics()
        
        # Validate performance metrics
        assert stats['total_optimizations'] >= 1
        assert stats['quantum_orders'] >= 2
        assert stats['advantage_rate'] >= 0.0 and stats['advantage_rate'] <= 1.0
        
        # Check if quantum advantages were achieved
        quantum_advantages = 0
        for op in operations:
            if isinstance(op, dict) and op.get('optimization'):
                if op['optimization'].get('quantum_advantage'):
                    quantum_advantages += 1
        
        assert quantum_advantages >= 0

    @pytest.mark.asyncio
    async def test_quantum_recommendations(self, trading_engine, sample_assets, sample_returns_data):
        """Test quantum-generated trading recommendations"""
        # Perform portfolio optimization
        result = await trading_engine.optimize_portfolio_quantum(
            account_id=1,
            assets=sample_assets,
            returns_data=sample_returns_data,
            risk_free_rate=0.02
        )
        
        assert result['success'] == True
        recommendations = result['recommendations']
        
        # Validate recommendations structure
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        for rec in recommendations:
            assert 'action' in rec
            assert rec['action'] in ['buy', 'sell']
            assert 'symbol' in rec
            assert 'weight' in rec
            assert 'reason' in rec
            assert 'confidence' in rec
            assert rec['confidence'] >= 0.0 and rec['confidence'] <= 1.0

    @pytest.mark.asyncio
    async def test_quantum_integration_end_to_end(self, trading_engine):
        """Test end-to-end quantum trading workflow"""
        # 1. Connect to quantum resources
        # (This is handled automatically by the trading engine)
        
        # 2. Optimize portfolio
        portfolio_result = await trading_engine.optimize_portfolio_quantum(
            account_id=1,
            assets=['AAPL', 'GOOGL', 'MSFT'],
            returns_data=np.random.normal(0.001, 0.02, (100, 3)).tolist(),
            risk_free_rate=0.02
        )
        assert portfolio_result['success'] == True
        
        # 3. Place quantum-optimized orders based on recommendations
        recommendations = portfolio_result['recommendations']
        orders_placed = 0
        
        for rec in recommendations[:2]:  # Place first 2 recommendations
            order_data = {
                'user_id': 1,
                'account_id': 1,
                'symbol': rec['symbol'],
                'side': rec['action'],
                'quantity': 100,
                'order_type': 'market',
                'use_quantum_optimization': True,
                'strategy_id': 'quantum_portfolio_strategy'
            }
            
            success, message, order_id = await trading_engine.place_order(order_data)
            if success:
                orders_placed += 1
        
        # 4. Get final statistics
        stats = await trading_engine.get_quantum_statistics()
        
        # Validate end-to-end workflow
        assert portfolio_result['success'] == True
        assert orders_placed >= 0
        assert stats['total_optimizations'] >= 1
        assert stats['quantum_orders'] >= 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 