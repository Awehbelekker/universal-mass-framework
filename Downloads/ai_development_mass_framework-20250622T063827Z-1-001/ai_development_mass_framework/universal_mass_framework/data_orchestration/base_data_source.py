"""
Base Data Source - Foundation for Universal Data Integration
==========================================================

Abstract base class that defines the interface for all data sources
in the Universal MASS Framework. Ensures consistent behavior across
all data source implementations.

All data sources must implement:
- initialize(): Setup and connectivity testing
- collect_data(): Main data collection method
- get_status(): Health check and status reporting
- close(): Cleanup and resource management

Features:
- Standardized error handling
- Rate limiting and compliance
- Data validation and quality checks
- Security and privacy controls
- Automatic retry and failover
- Performance monitoring
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from ...core.config_manager import MassConfig

logger = logging.getLogger(__name__)

@dataclass
class DataSourceStatus:
    """Status information for a data source"""
    name: str
    status: str  # 'operational', 'degraded', 'error', 'not_initialized'
    last_check: datetime
    error_message: Optional[str] = None
    performance_metrics: Dict[str, Any] = None

class BaseDataSource(ABC):
    """
    Abstract base class for all data sources in the Universal MASS Framework
    """
    
    def __init__(self, config: MassConfig):
        """Initialize base data source"""
        self.config = config
        self.name = self.__class__.__name__
        self.initialized = False
        self.last_status_check = None
        self.error_count = 0
        self.success_count = 0
        self.avg_response_time = 0.0
        
        # Rate limiting
        self.rate_limits = {}
        self.call_history = {}
        
        logger.info(f"Initializing data source: {self.name}")
    
    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the data source
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def collect_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect data from the source
        
        Args:
            parameters: Dictionary containing data collection parameters
            
        Returns:
            Dict containing the collected data or error information
        """
        pass
    
    @abstractmethod
    async def get_status(self) -> str:
        """
        Get current status of the data source
        
        Returns:
            str: Status ('operational', 'degraded', 'error', 'not_initialized')
        """
        pass
    
    async def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate input parameters for data collection
        
        Args:
            parameters: Parameters to validate
            
        Returns:
            bool: True if parameters are valid
        """
        try:
            # Basic validation - subclasses can override for specific validation
            if not isinstance(parameters, dict):
                return False
            
            # Check for required parameters (can be overridden)
            required_params = self.get_required_parameters()
            for param in required_params:
                if param not in parameters:
                    logger.error(f"Missing required parameter: {param}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Parameter validation failed: {e}")
            return False
    
    def get_required_parameters(self) -> List[str]:
        """
        Get list of required parameters for this data source
        
        Returns:
            List of required parameter names
        """
        return []  # Override in subclasses
    
    async def check_rate_limit(self, operation: str) -> bool:
        """
        Check if operation is within rate limits
        
        Args:
            operation: Name of the operation to check
            
        Returns:
            bool: True if within rate limits, False otherwise
        """
        try:
            if operation not in self.rate_limits:
                return True  # No rate limit defined
            
            limit = self.rate_limits[operation]
            now = datetime.now()
            
            # Initialize call history for this operation
            if operation not in self.call_history:
                self.call_history[operation] = []
            
            # Remove old calls outside the time window
            calls = self.call_history[operation]
            if 'per_minute' in limit:
                cutoff = now - timedelta(minutes=1)
                calls = [call for call in calls if call > cutoff]
                
                if len(calls) >= limit['per_minute']:
                    return False
            
            if 'per_hour' in limit:
                cutoff = now - timedelta(hours=1)
                calls = [call for call in calls if call > cutoff]
                
                if len(calls) >= limit['per_hour']:
                    return False
            
            if 'per_day' in limit:
                cutoff = now - timedelta(days=1)
                calls = [call for call in calls if call > cutoff]
                
                if len(calls) >= limit['per_day']:
                    return False
            
            # Update call history
            self.call_history[operation] = calls + [now]
            return True
            
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            return True  # Allow operation if check fails
    
    async def record_operation(self, operation: str, success: bool, response_time: float) -> None:
        """
        Record operation metrics
        
        Args:
            operation: Name of the operation
            success: Whether the operation was successful
            response_time: Time taken for the operation in seconds
        """
        try:
            if success:
                self.success_count += 1
            else:
                self.error_count += 1
            
            # Update average response time
            total_operations = self.success_count + self.error_count
            self.avg_response_time = (
                (self.avg_response_time * (total_operations - 1) + response_time) / total_operations
            )
            
        except Exception as e:
            logger.error(f"Failed to record operation metrics: {e}")
    
    async def get_detailed_status(self) -> DataSourceStatus:
        """
        Get detailed status information
        
        Returns:
            DataSourceStatus object with detailed information
        """
        try:
            status = await self.get_status()
            
            return DataSourceStatus(
                name=self.name,
                status=status,
                last_check=datetime.now(),
                performance_metrics={
                    'success_count': self.success_count,
                    'error_count': self.error_count,
                    'avg_response_time': self.avg_response_time,
                    'success_rate': self.success_count / max(1, self.success_count + self.error_count)
                }
            )
            
        except Exception as e:
            return DataSourceStatus(
                name=self.name,
                status='error',
                last_check=datetime.now(),
                error_message=str(e)
            )
    
    async def test_connectivity(self) -> bool:
        """
        Test connectivity to the data source
        
        Returns:
            bool: True if connectivity test passes
        """
        try:
            # Basic connectivity test - override in subclasses
            status = await self.get_status()
            return status in ['operational', 'degraded']
            
        except Exception as e:
            logger.error(f"Connectivity test failed for {self.name}: {e}")
            return False
    
    async def handle_error(self, error: Exception, operation: str) -> Dict[str, Any]:
        """
        Handle errors in a standardized way
        
        Args:
            error: The exception that occurred
            operation: Name of the operation that failed
            
        Returns:
            Dict containing error information
        """
        self.error_count += 1
        error_info = {
            'error': True,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'operation': operation,
            'timestamp': datetime.now().isoformat(),
            'data_source': self.name
        }
        
        logger.error(f"Error in {self.name}.{operation}: {error}")
        return error_info
    
    async def retry_operation(
        self, 
        operation_func: callable, 
        max_retries: int = 3, 
        delay: float = 1.0
    ) -> Any:
        """
        Retry an operation with exponential backoff
        
        Args:
            operation_func: The function to retry
            max_retries: Maximum number of retry attempts
            delay: Initial delay between retries in seconds
            
        Returns:
            Result of the operation or raises the last exception
        """
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return await operation_func()
                
            except Exception as e:
                last_exception = e
                
                if attempt < max_retries:
                    wait_time = delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Operation failed (attempt {attempt + 1}/{max_retries + 1}), retrying in {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Operation failed after {max_retries + 1} attempts: {e}")
        
        raise last_exception
    
    async def close(self) -> None:
        """
        Close the data source and clean up resources
        """
        try:
            self.initialized = False
            logger.info(f"Data source {self.name} closed")
        except Exception as e:
            logger.error(f"Error closing data source {self.name}: {e}")
    
    def __str__(self) -> str:
        """String representation of the data source"""
        return f"{self.name}(initialized={self.initialized}, status={self.get_status()})"
    
    def __repr__(self) -> str:
        """Detailed string representation"""
        return (f"{self.__class__.__name__}(name='{self.name}', "
                f"initialized={self.initialized}, "
                f"success_count={self.success_count}, "
                f"error_count={self.error_count})")

class MockDataSource(BaseDataSource):
    """
    Mock data source for testing and development
    """
    
    async def initialize(self) -> bool:
        """Initialize mock data source"""
        self.initialized = True
        return True
    
    async def collect_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Collect mock data"""
        await asyncio.sleep(0.1)  # Simulate network delay
        
        return {
            'mock_data': True,
            'parameters': parameters,
            'timestamp': datetime.now().isoformat(),
            'source': self.name
        }
    
    async def get_status(self) -> str:
        """Get mock status"""
        return 'operational' if self.initialized else 'not_initialized'
