"""Custom Data Sources - User-Defined Adapters==========================================Provides a framework for creating custom data source adaptersto enable integration with any data source not covered bythe built-in adapters."""import asyncioimport loggingfrom datetime import datetimefrom typing import Dict, Any, List, Callablefrom ...core.config_manager import MassConfigfrom ..base_data_source import BaseDataSourcelogger = logging.getLogger(__name__)class CustomDataSources(BaseDataSource):    """Custom data source adapter framework"""        def __init__(self, config: MassConfig):        super().__init__(config)        self.custom_adapters = {}            async def initialize(self) -> bool:        """Initialize custom data sources"""        try:
            self.initialized = True
            logger.info("✅ Custom Data Sources initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Custom Data Sources: {e}")
            return False
    
    def register_adapter(self, name: str, adapter_func: Callable) -> None:
        """Register a custom data adapter"""
        self.custom_adapters[name] = adapter_func
        logger.info(f"Registered custom adapter: {name}")
    
    async def collect_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data using custom adapters"""
        try:
            adapter_name = parameters.get('adapter_name')
            if adapter_name and adapter_name in self.custom_adapters:
                adapter = self.custom_adapters[adapter_name]
                return await adapter(parameters)
            
            return {
                "source": "custom",
                "data": {"available_adapters": list(self.custom_adapters.keys())},
                "metadata": {"collected_at": datetime.now().isoformat()}
            }
        except Exception as e:
            return await self.handle_error(e, "collect_data")
    
    async def get_status(self) -> str:
        """Get status of custom data sources"""
        return "operational" if self.initialized else "not_initialized"
