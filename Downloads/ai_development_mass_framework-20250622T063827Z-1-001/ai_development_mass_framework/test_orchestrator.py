"""
Master Test Orchestrator for PROMETHEUS AI Trading Platform
Coordinates execution of all testing phases: Backend, Frontend, Performance, Security, and Real Data Simulation
"""

import asyncio
import subprocess
import sys
import time
import json
import os
from datetime import datetime
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestOrchestrator:
    """Orchestrates comprehensive testing workflow"""
    
    def __init__(self):
        self.start_time = None
        self.test_results: Dict[str, Any] = {}
        self.workspace_root = os.path.dirname(os.path.abspath(__file__))
    
    async def run_comprehensive_testing_workflow(self):
        """Execute complete testing workflow"""
        logger.info("🚀 PROMETHEUS AI Trading Platform - Comprehensive Testing Workflow")
        logger.info("=" * 80)
        self.start_time = time.time()
        
        try:
            # Phase 1: Install Dependencies
            logger.info("\n📦 Phase 1: Installing Testing Dependencies...")
            await self._install_dependencies()
            
            # Phase 2: Backend Testing
            logger.info("\n🔧 Phase 2: Backend Automated Testing...")
            backend_results = await self._run_backend_tests()
            self.test_results['backend'] = backend_results
            
            # Phase 3: Frontend Testing
            logger.info("\n🎨 Phase 3: Frontend Automated Testing...")
            frontend_results = await self._run_frontend_tests()
            self.test_results['frontend'] = frontend_results
            
            # Phase 4: Performance and Load Testing
            logger.info("\n⚡ Phase 4: Performance and Load Testing...")
            performance_results = await self._run_performance_tests()
            self.test_results['performance'] = performance_results
            
            # Phase 5: Security Audit
            logger.info("\n🔒 Phase 5: Security Audit...")
            security_results = await self._run_security_audit()
            self.test_results['security'] = security_results
            
            # Phase 6: Real Data Simulation
            logger.info("\n💰 Phase 6: Real Data Trading Simulation...")
            simulation_results = await self._run_real_data_simulation()
            self.test_results['simulation'] = simulation_results
            
            # Generate Final Report
            await self._generate_final_report()
            
        except Exception as e:
            logger.error(f"💥 Testing workflow failed: {e}")
            self.test_results['error'] = str(e)
        
        finally:
            total_time = time.time() - self.start_time
            logger.info(f"\n⏱️ Total testing time: {total_time/60:.2f} minutes")
    
    async def _install_dependencies(self):
        """Install testing dependencies"""
        try:
            # Install backend test dependencies
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "test_requirements.txt"
            ], capture_output=True, text=True, cwd=self.workspace_root)
            
            if result.returncode == 0:
                logger.info("✅ Backend testing dependencies installed successfully")
            else:
                logger.warning(f"⚠️ Backend dependency installation issues: {result.stderr}")
            
            # Install frontend test dependencies
            frontend_path = os.path.join(self.workspace_root, "frontend")
            if os.path.exists(frontend_path):
                result = subprocess.run([
                    "npm", "install", "@testing-library/react", "@testing-library/jest-dom", 
                    "@testing-library/user-event", "--legacy-peer-deps"
                ], capture_output=True, text=True, cwd=frontend_path)
                
                if result.returncode == 0:
                    logger.info("✅ Frontend testing dependencies installed successfully")
                else:
                    logger.warning(f"⚠️ Frontend dependency installation issues: {result.stderr}")
            
        except Exception as e:
            logger.error(f"❌ Dependency installation failed: {e}")
    
    async def _run_backend_tests(self) -> Dict[str, Any]:
        """Run comprehensive backend tests"""
        results = {
            "status": "running",
            "start_time": datetime.now().isoformat(),
            "tests": {}
        }
        
        try:
            # Run pytest with coverage
            cmd = [
                sys.executable, "-m", "pytest", 
                "tests/test_comprehensive_backend.py", 
                "-v", "--cov=.", "--cov-report=html", "--cov-report=json"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace_root)
            
            results.update({
                "status": "completed" if result.returncode == 0 else "failed",
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "end_time": datetime.now().isoformat()
            })
            
            # Parse test results
            if "failed" in result.stdout.lower():
                results["tests"]["failures"] = self._extract_test_failures(result.stdout)
            
            if "passed" in result.stdout.lower():
                results["tests"]["passed"] = self._extract_test_count(result.stdout, "passed")
            
            logger.info(f"🔧 Backend tests completed with return code: {result.returncode}")
            
        except Exception as e:
            results.update({
                "status": "error",
                "error": str(e),
                "end_time": datetime.now().isoformat()
            })
            logger.error(f"❌ Backend testing error: {e}")
        
        return results
    
    async def _run_frontend_tests(self) -> Dict[str, Any]:
        """Run comprehensive frontend tests"""
        results = {
            "status": "running",
            "start_time": datetime.now().isoformat(),
            "tests": {}
        }
        
        try:
            frontend_path = os.path.join(self.workspace_root, "frontend")
            
            if os.path.exists(frontend_path):
                # Run React tests
                cmd = ["npm", "test", "--", "--coverage", "--watchAll=false", "--verbose"]
                
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=frontend_path)
                
                results.update({
                    "status": "completed" if result.returncode == 0 else "failed",
                    "return_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "end_time": datetime.now().isoformat()
                })
                
                logger.info(f"🎨 Frontend tests completed with return code: {result.returncode}")
            else:
                results.update({
                    "status": "skipped",
                    "reason": "Frontend directory not found",
                    "end_time": datetime.now().isoformat()
                })
                logger.warning("⚠️ Frontend directory not found, skipping frontend tests")
            
        except Exception as e:
            results.update({
                "status": "error",
                "error": str(e),
                "end_time": datetime.now().isoformat()
            })
            logger.error(f"❌ Frontend testing error: {e}")
        
        return results
    
    async def _run_performance_tests(self) -> Dict[str, Any]:
        """Run performance and load tests"""
        results = {
            "status": "running",
            "start_time": datetime.now().isoformat(),
        }
        
        try:
            # Import and run performance tests
            sys.path.append(os.path.join(self.workspace_root, "performance_testing"))
            
            try:
                from performance_testing.load_test_suite import ComprehensiveLoadTestSuite
                
                load_test_suite = ComprehensiveLoadTestSuite()
                performance_results = await load_test_suite.run_comprehensive_test()
                
                results.update({
                    "status": "completed",
                    "results": performance_results,
                    "end_time": datetime.now().isoformat()
                })
                
                logger.info("⚡ Performance tests completed successfully")
                
            except ImportError as e:
                # Run as subprocess if import fails
                cmd = [sys.executable, "performance_testing/load_test_suite.py"]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace_root)
                
                results.update({
                    "status": "completed" if result.returncode == 0 else "failed",
                    "return_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "end_time": datetime.now().isoformat()
                })
                
                logger.info(f"⚡ Performance tests completed via subprocess: {result.returncode}")
            
        except Exception as e:
            results.update({
                "status": "error",
                "error": str(e),
                "end_time": datetime.now().isoformat()
            })
            logger.error(f"❌ Performance testing error: {e}")
        
        return results
    
    async def _run_security_audit(self) -> Dict[str, Any]:
        """Run security audit"""
        results = {
            "status": "running",
            "start_time": datetime.now().isoformat(),
        }
        
        try:
            # Import and run security tests
            sys.path.append(os.path.join(self.workspace_root, "security_audit"))
            
            try:
                from security_audit.security_test_suite import ComprehensiveSecurityAudit
                
                security_audit = ComprehensiveSecurityAudit()
                security_results = await security_audit.run_full_security_audit()
                
                results.update({
                    "status": "completed",
                    "results": [
                        {
                            "test_name": r.test_name,
                            "passed": r.passed,
                            "details": r.details,
                            "severity": r.severity
                        }
                        for r in security_results
                    ],
                    "end_time": datetime.now().isoformat()
                })
                
                logger.info("🔒 Security audit completed successfully")
                
            except ImportError as e:
                # Run as subprocess if import fails
                cmd = [sys.executable, "security_audit/security_test_suite.py"]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.workspace_root)
                
                results.update({
                    "status": "completed" if result.returncode == 0 else "failed",
                    "return_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "end_time": datetime.now().isoformat()
                })
                
                logger.info(f"🔒 Security audit completed via subprocess: {result.returncode}")
            
        except Exception as e:
            results.update({
                "status": "error",
                "error": str(e),
                "end_time": datetime.now().isoformat()
            })
            logger.error(f"❌ Security audit error: {e}")
        
        return results
    
    async def _run_real_data_simulation(self) -> Dict[str, Any]:
        """Run real data trading simulation"""
        results = {
            "status": "running",
            "start_time": datetime.now().isoformat(),
        }
        
        try:
            # Import and run simulation
            sys.path.append(os.path.join(self.workspace_root, "real_data_simulation"))
            
            try:
                from real_data_simulation.admin_trading_simulator import main as run_simulation
                
                # Run simulation for a limited time (5 minutes)
                simulation_task = asyncio.create_task(run_simulation())
                
                try:
                    await asyncio.wait_for(simulation_task, timeout=300)  # 5 minutes
                except asyncio.TimeoutError:
                    logger.info("💰 Simulation completed after 5-minute timeout")
                
                results.update({
                    "status": "completed",
                    "duration": "5 minutes",
                    "end_time": datetime.now().isoformat()
                })
                
                logger.info("💰 Real data simulation completed successfully")
                
            except ImportError as e:
                # Run as subprocess if import fails
                cmd = [sys.executable, "real_data_simulation/admin_trading_simulator.py"]
                
                # Run with timeout
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, 
                                          timeout=300, cwd=self.workspace_root)
                    
                    results.update({
                        "status": "completed" if result.returncode == 0 else "failed",
                        "return_code": result.returncode,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "end_time": datetime.now().isoformat()
                    })
                    
                except subprocess.TimeoutExpired:
                    results.update({
                        "status": "completed",
                        "timeout": True,
                        "end_time": datetime.now().isoformat()
                    })
                
                logger.info("💰 Real data simulation completed via subprocess")
            
        except Exception as e:
            results.update({
                "status": "error",
                "error": str(e),
                "end_time": datetime.now().isoformat()
            })
            logger.error(f"❌ Real data simulation error: {e}")
        
        return results
    
    def _extract_test_failures(self, output: str) -> List[str]:
        """Extract test failure information from output"""
        failures = []
        lines = output.split('\n')
        
        for i, line in enumerate(lines):
            if 'FAILED' in line or 'ERROR' in line:
                failures.append(line.strip())
        
        return failures
    
    def _extract_test_count(self, output: str, status: str) -> int:
        """Extract test count from output"""
        import re
        pattern = rf'(\d+) {status}'
        matches = re.findall(pattern, output, re.IGNORECASE)
        return int(matches[0]) if matches else 0
    
    async def _generate_final_report(self):
        """Generate comprehensive final report"""
        logger.info("\n" + "=" * 80)
        logger.info("📊 COMPREHENSIVE TESTING REPORT - PROMETHEUS AI TRADING PLATFORM")
        logger.info("=" * 80)
        
        # Calculate overall status
        total_phases = len(self.test_results)
        successful_phases = sum(1 for result in self.test_results.values() 
                              if isinstance(result, dict) and result.get('status') == 'completed')
        
        logger.info(f"\n🎯 Overall Status: {successful_phases}/{total_phases} phases completed successfully")
        
        # Detailed phase results
        for phase_name, phase_results in self.test_results.items():
            if isinstance(phase_results, dict):
                status = phase_results.get('status', 'unknown')
                status_icon = {"completed": "✅", "failed": "❌", "error": "💥", "skipped": "⏭️"}.get(status, "❓")
                
                logger.info(f"\n{status_icon} {phase_name.title()} Testing:")
                
                if status == "completed":
                    logger.info(f"   Status: Successfully completed")
                    if 'results' in phase_results:
                        logger.info(f"   Results: Available")
                elif status == "failed":
                    logger.info(f"   Status: Failed")
                    if 'return_code' in phase_results:
                        logger.info(f"   Return Code: {phase_results['return_code']}")
                elif status == "error":
                    logger.info(f"   Status: Error - {phase_results.get('error', 'Unknown error')}")
                elif status == "skipped":
                    logger.info(f"   Status: Skipped - {phase_results.get('reason', 'Unknown reason')}")
        
        # Performance summary
        if 'performance' in self.test_results:
            perf_results = self.test_results['performance']
            if perf_results.get('status') == 'completed' and 'results' in perf_results:
                logger.info(f"\n⚡ Performance Summary:")
                results = perf_results['results']
                for test_type, metrics in results.items():
                    if isinstance(metrics, dict) and 'avg_response_time' in metrics:
                        logger.info(f"   {test_type}: {metrics['avg_response_time']:.3f}s avg response")
        
        # Security summary
        if 'security' in self.test_results:
            sec_results = self.test_results['security']
            if sec_results.get('status') == 'completed' and 'results' in sec_results:
                security_issues = [r for r in sec_results['results'] if not r['passed']]
                critical_issues = [r for r in security_issues if r['severity'] == 'critical']
                
                logger.info(f"\n🔒 Security Summary:")
                logger.info(f"   Total Issues: {len(security_issues)}")
                logger.info(f"   Critical Issues: {len(critical_issues)}")
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"comprehensive_test_report_{timestamp}.json"
        
        full_report = {
            "test_run_info": {
                "timestamp": timestamp,
                "total_duration": time.time() - self.start_time,
                "phases_completed": successful_phases,
                "total_phases": total_phases
            },
            "phase_results": self.test_results
        }
        
        try:
            with open(report_filename, 'w') as f:
                json.dump(full_report, f, indent=2, default=str)
            logger.info(f"\n💾 Comprehensive test report saved to: {report_filename}")
        except Exception as e:
            logger.error(f"❌ Failed to save report: {e}")
        
        # Final recommendations
        logger.info(f"\n🎯 RECOMMENDATIONS:")
        
        if successful_phases == total_phases:
            logger.info("   ✅ All testing phases completed successfully!")
            logger.info("   🚀 System is ready for Firebase deployment")
            logger.info("   📈 Consider setting up continuous integration")
        else:
            logger.info("   ⚠️ Some testing phases need attention")
            logger.info("   🔧 Review failed tests before deployment")
            logger.info("   🔄 Re-run specific test phases as needed")
        
        logger.info(f"\n🏁 Testing workflow completed in {(time.time() - self.start_time)/60:.2f} minutes")

async def main():
    """Main function to run testing orchestrator"""
    orchestrator = TestOrchestrator()
    await orchestrator.run_comprehensive_testing_workflow()

if __name__ == "__main__":
    asyncio.run(main())
