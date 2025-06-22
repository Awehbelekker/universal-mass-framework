#!/usr/bin/env python3
"""
Enterprise Debug Toolkit for MASS Framework
This module provides comprehensive debugging and diagnostic tools for the MASS Framework.
"""

import os
import sys
import time
import asyncio
import logging
import traceback
from typing import Dict, Any, List, Optional, Union, Callable
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, '.')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class MASSDebugger:
    """Enterprise debug toolkit for MASS Framework components"""
    
    def __init__(self, verbose: bool = False):
        """Initialize the debugger
        
        Args:
            verbose: Whether to print verbose debug information
        """
        self.verbose = verbose
        self.start_time = time.time()
        self.components: Dict[str, Any] = {}
        self.benchmark_results: Dict[str, float] = {}
        self.performance_metrics: Dict[str, Any] = {}
        
        logger.info("MASS Framework Enterprise Debugger initialized")
    
    def log(self, message: str) -> None:
        """Log a debug message if verbose mode is enabled
        
        Args:
            message: The message to log
        """
        if self.verbose:
            print(f"[DEBUG] {message}")
        logger.debug(message)
    
    async def benchmark(self, name: str, func: Callable) -> Any:
        """Benchmark a function and record its execution time
        
        Args:
            name: Name of the benchmark
            func: Function to benchmark (can be async)
            
        Returns:
            Result of the function
        """
        self.log(f"Starting benchmark: {name}")
        start = time.time()
        
        try:
            # Check if function is async
            if asyncio.iscoroutinefunction(func):
                result = await func()
            else:
                result = func()
                
            duration = time.time() - start
            self.benchmark_results[name] = duration
            self.log(f"Benchmark {name} completed in {duration:.4f}s")
            return result
            
        except Exception as e:
            self.log(f"Error in benchmark {name}: {str(e)}")
            logger.error(f"Benchmark {name} failed: {str(e)}")
            logger.error(traceback.format_exc())
            self.benchmark_results[name] = -1
            raise
    
    def register_component(self, name: str, component: Any) -> None:
        """Register a component for debugging
        
        Args:
            name: Name of the component
            component: The component instance
        """
        self.components[name] = component
        self.log(f"Registered component: {name}")
    
    async def debug_ai_coordinator(self) -> Dict[str, Any]:
        """Debug the AI coordinator initialization and methods
        
        Returns:
            Dict containing debug results
        """
        self.log("Starting AI Coordinator debug...")
        results = {"components": {}, "performance": {}, "status": "unknown"}
        
        try:
            # Import and initialize components
            from core.mass_coordinator import MASSCoordinator
            from core.ai_coordinator import get_ai_coordinator
            from core.database_manager import DatabaseManager
            
            # Test coordinator
            coordinator = await self.benchmark("mass_coordinator_init", lambda: MASSCoordinator())
            self.register_component("mass_coordinator", coordinator)
            results["components"]["coordinator"] = {"status": "operational"}
            
            # Test AI coordinator
            ai_coordinator = await self.benchmark("ai_coordinator_init", lambda: get_ai_coordinator())
            self.register_component("ai_coordinator", ai_coordinator)
            results["components"]["ai_coordinator"] = {"status": "operational"}
            
            # Test database
            db_manager = await self.benchmark("database_init", lambda: DatabaseManager())
            self.register_component("database", db_manager)
            db_stats = await self.benchmark("database_stats", lambda: db_manager.get_database_stats())
            results["components"]["database"] = {
                "status": "operational",
                "stats": db_stats
            }
            
            # Agent tests
            results["components"]["agents"] = await self.debug_agents()
            
            # Overall status
            all_operational = all(comp.get("status") == "operational" 
                                for comp in results["components"].values() 
                                if isinstance(comp, dict) and "status" in comp)
            
            results["status"] = "operational" if all_operational else "issues_detected"
            results["performance"] = self.benchmark_results
            results["total_time"] = time.time() - self.start_time
            
            self.log(f"AI Coordinator debug complete. Status: {results['status']}")
            return results
            
        except Exception as e:
            self.log(f"Error in AI Coordinator debug: {str(e)}")
            logger.error(f"AI Coordinator debug failed: {str(e)}")
            logger.error(traceback.format_exc())
            results["status"] = "error"
            results["error"] = str(e)
            results["traceback"] = traceback.format_exc()
            return results
    
    async def debug_agents(self) -> Dict[str, Any]:
        """Debug the agent initialization and basic functionality
        
        Returns:
            Dict containing agent debug results
        """
        self.log("Testing enterprise agents...")
        results = {}
        
        # List of agents to test
        agents_to_test = [
            ("InnovationScoutAgent", "agents.innovation.innovation_scout_agent", "InnovationScoutAgent"),
            ("EnhancedCreativeDirectorAgent", "agents.creative.enhanced_creative_director_agent", "EnhancedCreativeDirectorAgent"),
            ("MarketIntelligenceAgent", "agents.research.market_intelligence_agent", "MarketIntelligenceAgent"),
            ("UXDesignAgent", "agents.creative.ux_design_agent", "UXDesignAgent"),
            ("SystemArchitectAgent", "agents.development.system_architect_agent", "SystemArchitectAgent")
        ]
        
        for agent_name, module_path, class_name in agents_to_test:
            try:
                # Import agent module
                module = __import__(module_path, fromlist=[class_name])
                agent_class = getattr(module, class_name)
                
                # Initialize agent
                agent_init_name = f"{agent_name.lower()}_init"
                if class_name == "EnhancedCreativeDirectorAgent":
                    agent = await self.benchmark(agent_init_name, lambda: agent_class())
                elif class_name == "InnovationScoutAgent": 
                    agent = await self.benchmark(agent_init_name, lambda: agent_class("debug_test"))
                else:
                    agent = await self.benchmark(agent_init_name, lambda: agent_class())
                
                self.register_component(agent_name, agent)
                
                # Get agent attributes and check functionality
                attributes = [attr for attr in dir(agent) if not attr.startswith('_')]
                has_required_methods = any('process' in attr.lower() for attr in attributes)
                
                results[agent_name] = {
                    "status": "operational" if has_required_methods else "incomplete",
                    "initialization_time": self.benchmark_results.get(agent_init_name, -1),
                    "attributes": len(attributes)
                }
                
                self.log(f"Agent {agent_name} tested successfully")
                
            except Exception as e:
                self.log(f"Error testing agent {agent_name}: {str(e)}")
                logger.error(f"Agent {agent_name} test failed: {str(e)}")
                results[agent_name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results

    async def diagnostic_summary(self) -> Dict[str, Any]:
        """Generate a diagnostic summary of the system
        
        Returns:
            Dict containing diagnostic information
        """
        # System information
        import platform
        import psutil
        
        self.log("Generating diagnostic summary...")
        summary = {
            "system": {
                "python_version": platform.python_version(),
                "platform": platform.platform(),
                "cpu_count": psutil.cpu_count(),
                "memory_available": f"{psutil.virtual_memory().available / (1024 * 1024 * 1024):.2f} GB",
            },
            "framework": {
                "component_count": len(self.components),
                "benchmark_results": self.benchmark_results,
                "total_time": time.time() - self.start_time
            }
        }
        
        # Check database if available
        if "database" in self.components:
            db_manager = self.components["database"]
            summary["database"] = await self.benchmark("database_diag", lambda: db_manager.get_database_stats())
        
        # Check performance metrics
        avg_benchmark = sum(v for v in self.benchmark_results.values() if v > 0) / len(self.benchmark_results) if self.benchmark_results else 0
        summary["performance"] = {
            "average_benchmark": avg_benchmark,
            "benchmark_count": len(self.benchmark_results),
            "performance_score": 100 - min(100, int(avg_benchmark * 10))  # Lower times = higher score
        }
        
        self.log("Diagnostic summary generated")
        return summary

async def main() -> None:
    """Main debug function"""
    debugger = MASSDebugger(verbose=True)
    
    # Run debug tests
    print("\n🔍 MASS FRAMEWORK ENTERPRISE DEBUG\n")
    print("=" * 50)
    
    results = await debugger.debug_ai_coordinator()
    diagnostics = await debugger.diagnostic_summary()
    
    # Display results
    print("\n📊 DEBUG RESULTS:\n")
    print(f"Status: {results['status'].upper()}")
    print(f"Total Time: {results['total_time']:.4f}s")
    print("\nComponent Status:")
    
    for component, details in results["components"].items():
        if component != "agents":
            if isinstance(details, dict) and "status" in details:
                print(f"- {component}: {details['status'].upper()}")
    
    print("\nAgent Status:")
    if "agents" in results["components"]:
        for agent, details in results["components"]["agents"].items():
            status = details.get("status", "unknown").upper()
            init_time = details.get("initialization_time", -1)
            time_str = f"{init_time:.4f}s" if init_time >= 0 else "N/A"
            print(f"- {agent}: {status} (Init: {time_str})")
    
    print("\nPerformance Summary:")
    print(f"- Average Benchmark: {diagnostics['performance']['average_benchmark']:.4f}s")
    print(f"- Performance Score: {diagnostics['performance']['performance_score']}/100")
    
    print("\n✅ Debug completed")
    
    # Write results to file
    import json
    with open("debug_results.json", "w") as f:
        json.dump({
            "results": results,
            "diagnostics": diagnostics,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    print("\nDetailed results written to debug_results.json")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDebug interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
