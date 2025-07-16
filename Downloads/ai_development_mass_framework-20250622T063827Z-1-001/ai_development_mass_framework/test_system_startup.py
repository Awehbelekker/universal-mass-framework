"""
MASS Framework System Test Script

This script validates all components of the MASS Framework and ensures
the system is ready for deployment.
"""

import asyncio
import sys
import os
import logging
from datetime import datetime
from typing import Dict, Any, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SystemValidator:
    """System validation and testing"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = datetime.utcnow()
    
    async def run_full_system_test(self) -> Dict[str, Any]:
        """Run comprehensive system test"""
        logger.info("Starting MASS Framework system validation...")
        
        try:
            # Test 1: Core Dependencies
            await self._test_core_dependencies()
            
            # Test 2: Agent System
            await self._test_agent_system()
            
            # Test 3: Coordination Engine
            await self._test_coordination_engine()
            
            # Test 4: MASS Engine
            await self._test_mass_engine()
            
            # Test 5: API Endpoints
            await self._test_api_endpoints()
            
            # Test 6: Frontend Components
            await self._test_frontend_components()
            
            # Test 7: Database Connectivity
            await self._test_database_connectivity()
            
            # Test 8: Security Framework
            await self._test_security_framework()
            
            # Generate final report
            return await self._generate_test_report()
            
        except Exception as e:
            logger.error(f"System test failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _test_core_dependencies(self) -> None:
        """Test core dependencies"""
        logger.info("Testing core dependencies...")
        
        try:
            # Test FastAPI
            import fastapi
            logger.info("✓ FastAPI imported successfully")
            
            # Test uvicorn
            import uvicorn
            logger.info("✓ Uvicorn imported successfully")
            
            # Test other core dependencies
            import numpy
            import pandas
            import pydantic
            logger.info("✓ Core data processing libraries imported")
            
            self.test_results["core_dependencies"] = {
                "status": "passed",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except ImportError as e:
            logger.error(f"✗ Core dependency test failed: {e}")
            self.test_results["core_dependencies"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _test_agent_system(self) -> None:
        """Test agent system"""
        logger.info("Testing agent system...")
        
        try:
            from core.enhanced_agent_base import EnhancedAgentBase, TrustLevel, AgentCapability
            
            # Create test agent
            capabilities = [
                AgentCapability(
                    name="test_task",
                    description="Test task capability",
                    trust_required=TrustLevel.LOW,
                    max_execution_time=30
                )
            ]
            
            test_agent = EnhancedAgentBase(
                agent_id="test_agent",
                specialization="testing",
                capabilities=capabilities,
                trust_level=TrustLevel.MEDIUM
            )
            
            await test_agent.initialize()
            metrics = await test_agent.get_metrics()
            
            logger.info(f"✓ Agent system test passed: {metrics['agent_id']}")
            
            self.test_results["agent_system"] = {
                "status": "passed",
                "agent_id": test_agent.agent_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"✗ Agent system test failed: {e}")
            self.test_results["agent_system"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _test_coordination_engine(self) -> None:
        """Test coordination engine"""
        logger.info("Testing coordination engine...")
        
        try:
            from core.advanced_mass_coordinator import AdvancedMASSCoordinator
            
            coordinator = AdvancedMASSCoordinator()
            
            # Test basic functionality
            metrics = await coordinator.get_enterprise_metrics()
            
            logger.info("✓ Coordination engine test passed")
            
            self.test_results["coordination_engine"] = {
                "status": "passed",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"✗ Coordination engine test failed: {e}")
            self.test_results["coordination_engine"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _test_mass_engine(self) -> None:
        """Test MASS engine"""
        logger.info("Testing MASS engine...")
        
        try:
            from universal_mass_framework.core.mass_engine import MassEngine
            
            engine = MassEngine()
            
            # Test initialization
            await engine.start()
            
            # Test basic operation
            test_data = {"test": "data"}
            result = await engine.integrate_system({"test": "config"}, test_data)
            
            await engine.stop()
            
            logger.info("✓ MASS engine test passed")
            
            self.test_results["mass_engine"] = {
                "status": "passed",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"✗ MASS engine test failed: {e}")
            self.test_results["mass_engine"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _test_api_endpoints(self) -> None:
        """Test API endpoints"""
        logger.info("Testing API endpoints...")
        
        try:
            import httpx
            
            # Test health endpoint
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/health")
                
                if response.status_code == 200:
                    logger.info("✓ Health endpoint test passed")
                else:
                    raise Exception(f"Health endpoint returned {response.status_code}")
            
            self.test_results["api_endpoints"] = {
                "status": "passed",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"✗ API endpoints test failed: {e}")
            self.test_results["api_endpoints"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _test_frontend_components(self) -> None:
        """Test frontend components"""
        logger.info("Testing frontend components...")
        
        try:
            # Check if frontend files exist
            frontend_files = [
                "frontend/index.html",
                "frontend/package.json",
                "frontend/src/app/App.tsx"
            ]
            
            for file_path in frontend_files:
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Frontend file not found: {file_path}")
            
            logger.info("✓ Frontend components test passed")
            
            self.test_results["frontend_components"] = {
                "status": "passed",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"✗ Frontend components test failed: {e}")
            self.test_results["frontend_components"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _test_database_connectivity(self) -> None:
        """Test database connectivity"""
        logger.info("Testing database connectivity...")
        
        try:
            # Test SQLAlchemy
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            
            # Test with SQLite for now
            engine = create_engine("sqlite:///test.db")
            
            # Test connection
            with engine.connect() as conn:
                result = conn.execute("SELECT 1")
                result.fetchone()
            
            logger.info("✓ Database connectivity test passed")
            
            self.test_results["database_connectivity"] = {
                "status": "passed",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"✗ Database connectivity test failed: {e}")
            self.test_results["database_connectivity"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _test_security_framework(self) -> None:
        """Test security framework"""
        logger.info("Testing security framework...")
        
        try:
            # Test basic security imports
            import cryptography
            import jwt
            
            logger.info("✓ Security framework test passed")
            
            self.test_results["security_framework"] = {
                "status": "passed",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"✗ Security framework test failed: {e}")
            self.test_results["security_framework"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        end_time = datetime.utcnow()
        duration = (end_time - self.start_time).total_seconds()
        
        # Calculate overall status
        passed_tests = sum(1 for result in self.test_results.values() if result.get("status") == "passed")
        total_tests = len(self.test_results)
        overall_status = "passed" if passed_tests == total_tests else "failed"
        
        report = {
            "overall_status": overall_status,
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": (passed_tests / total_tests) * 100 if total_tests > 0 else 0
            },
            "test_results": self.test_results,
            "duration_seconds": duration,
            "timestamp": end_time.isoformat()
        }
        
        # Log summary
        logger.info(f"System test completed: {passed_tests}/{total_tests} tests passed")
        logger.info(f"Overall status: {overall_status}")
        logger.info(f"Duration: {duration:.2f} seconds")
        
        return report


async def main():
    """Main test execution"""
    validator = SystemValidator()
    report = await validator.run_full_system_test()
    
    # Print detailed results
    print("\n" + "="*60)
    print("MASS FRAMEWORK SYSTEM TEST REPORT")
    print("="*60)
    
    print(f"Overall Status: {report['overall_status'].upper()}")
    print(f"Tests Passed: {report['test_summary']['passed_tests']}/{report['test_summary']['total_tests']}")
    print(f"Success Rate: {report['test_summary']['success_rate']:.1f}%")
    print(f"Duration: {report['test_summary']['duration_seconds']:.2f} seconds")
    
    print("\nDetailed Results:")
    print("-" * 40)
    
    for test_name, result in report['test_results'].items():
        status_icon = "✓" if result['status'] == 'passed' else "✗"
        print(f"{status_icon} {test_name}: {result['status']}")
        if result['status'] == 'failed' and 'error' in result:
            print(f"    Error: {result['error']}")
    
    print("\n" + "="*60)
    
    # Exit with appropriate code
    if report['overall_status'] == 'passed':
        print("🎉 All tests passed! System is ready for deployment.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please fix issues before deployment.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 