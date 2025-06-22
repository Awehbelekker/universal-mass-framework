
# Enhanced error handling for MASS Framework
import logging
import traceback
from typing import Any, Dict, Optional
from functools import wraps

logger = logging.getLogger(__name__)

class MASSFrameworkError(Exception):
    """Base exception for MASS Framework"""
    pass

class AgentCommunicationError(MASSFrameworkError):
    """Error in agent communication"""
    pass

class WorkflowExecutionError(MASSFrameworkError):
    """Error in workflow execution"""
    pass

def handle_errors(default_return=None):
    """Decorator for consistent error handling"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                logger.debug(traceback.format_exc())
                return default_return
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                logger.debug(traceback.format_exc())
                return default_return
                
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

class ErrorReporter:
    """Centralized error reporting and monitoring"""
    
    def __init__(self):
        self.error_counts: Dict[str, int] = {}
        
    def report_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """Report and track errors"""
        error_type = type(error).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        logger.error(f"Error reported: {error_type} - {str(error)}")
        if context:
            logger.error(f"Context: {context}")
            
    def get_error_summary(self) -> Dict[str, int]:
        """Get summary of reported errors"""
        return self.error_counts.copy()
