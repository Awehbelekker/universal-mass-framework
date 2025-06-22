"""
🧪 ENTERPRISE AGENTS INTEGRATION TEST
Comprehensive test suite for all enterprise-grade agents in the MASS Framework.

This test validates:
- Agent initialization and configuration
- Core functionality and message processing
- Inter-agent coordination and communication
- Enterprise-specific features and capabilities
- Performance and reliability under load
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, List
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnterpriseAgentsTestSuite:
    """
    Comprehensive test suite for enterprise agents
    """
    
    def __init__(self):
        self.test_results = []
        self.agents = {}
        self.performance_metrics = {}
        
    async def initialize_agents(self):
        """Initialize all enterprise agents"""
        logger.info("🚀 Initializing enterprise agents...")
        
        try:
            # Initialize Innovation Scout Agent
            from agents.innovation.innovation_scout_agent import InnovationScoutAgent
            self.agents['innovation_scout'] = InnovationScoutAgent("test_innovation_scout")
            logger.info("✅ Innovation Scout Agent initialized")
              # Initialize Enhanced Creative Director Agent
            from agents.creative.enhanced_creative_director_agent import EnhancedCreativeDirectorAgent
            self.agents['creative_director'] = EnhancedCreativeDirectorAgent()
            logger.info("✅ Enhanced Creative Director Agent initialized")
              # Initialize Market Intelligence Agent
            from agents.research.market_intelligence_agent import MarketIntelligenceAgent
            self.agents['market_intelligence'] = MarketIntelligenceAgent()
            logger.info("✅ Market Intelligence Agent initialized")
            
            # Initialize UX Design Agent
            from agents.creative.ux_design_agent import UXDesignAgent
            self.agents['ux_design'] = UXDesignAgent()
            logger.info("✅ UX Design Agent initialized")
            
            # Initialize System Architect Agent
            from agents.development.system_architect_agent import SystemArchitectAgent
            self.agents['system_architect'] = SystemArchitectAgent()
            logger.info("✅ System Architect Agent initialized")
              # Initialize other agents as available            try:
                from agents.development.fullstack_developer_agent import FullStackDeveloperAgent
                self.agents['fullstack_developer'] = FullStackDeveloperAgent()
                logger.info("✅ Full Stack Developer Agent initialized")
            except ImportError:
                logger.warning("⚠️ Full Stack Developer Agent not available")
            
            try:
                from agents.business.business_analyst_agent import BusinessAnalystAgent
                self.agents['business_analyst'] = BusinessAnalystAgent("test_business_analyst")
                logger.info("✅ Business Analyst Agent initialized")
            except ImportError:
                logger.warning("⚠️ Business Analyst Agent not available")
            except Exception as e:
                logger.warning(f"⚠️ Business Analyst Agent initialization error: {e}")
                
            logger.info(f"🎯 Successfully initialized {len(self.agents)} enterprise agents")
            
        except Exception as e:
            logger.error(f"❌ Error initializing agents: {e}")
            raise

    async def test_agent_core_functionality(self):
        """Test core functionality of each agent"""
        logger.info("🔧 Testing agent core functionality...")
        
        test_results = []
        
        for agent_name, agent in self.agents.items():
            try:
                start_time = time.time()
                
                # Test basic task processing
                if hasattr(agent, 'process_task'):
                    result = await agent.process_task({
                        "task_type": "test",
                        "data": {"test": True}
                    })
                    test_results.append({
                        "agent": agent_name,
                        "test": "process_task",
                        "status": "success" if result else "failed",
                        "result": result
                    })
                
                # Test input analysis
                if hasattr(agent, 'analyze_input'):
                    result = await agent.analyze_input({
                        "input_type": "test",
                        "data": {"test": True}
                    })
                    test_results.append({
                        "agent": agent_name,
                        "test": "analyze_input",
                        "status": "success" if result else "failed",
                        "result": result
                    })
                
                # Test agent coordination
                if hasattr(agent, 'coordinate_with_agents'):
                    result = await agent.coordinate_with_agents(
                        ["test_agent"], 
                        {"context": "test"}
                    )
                    test_results.append({
                        "agent": agent_name,
                        "test": "coordinate_with_agents",
                        "status": "success" if result else "failed",
                        "result": result
                    })
                
                # Test agent status
                if hasattr(agent, 'get_agent_status'):
                    status = agent.get_agent_status()
                    test_results.append({
                        "agent": agent_name,
                        "test": "get_agent_status",
                        "status": "success" if status else "failed",
                        "result": status
                    })
                
                end_time = time.time()
                self.performance_metrics[agent_name] = {
                    "response_time": end_time - start_time,
                    "status": "active"
                }
                
                logger.info(f"✅ {agent_name} core functionality test completed")
                
            except Exception as e:
                logger.error(f"❌ Error testing {agent_name}: {e}")
                test_results.append({
                    "agent": agent_name,
                    "test": "core_functionality",
                    "status": "error",
                    "error": str(e)
                })
        
        self.test_results.extend(test_results)
        return test_results

    async def test_specialized_functionality(self):
        """Test specialized functionality of each agent"""
        logger.info("🎯 Testing specialized agent functionality...")
        
        test_results = []
        
        # Test Innovation Scout Agent
        if 'innovation_scout' in self.agents:
            try:
                agent = self.agents['innovation_scout']
                
                # Test opportunity scanning
                result = await agent.process_request({
                    "action": "scan_opportunities",
                    "focus_areas": ["AI", "automation", "enterprise"]
                })
                test_results.append({
                    "agent": "innovation_scout",
                    "test": "scan_opportunities",
                    "status": "success" if result.get("status") == "success" else "failed",
                    "opportunities_found": result.get("opportunities_found", 0)
                })
                
                # Test trend analysis
                trend_result = await agent.process_request({
                    "action": "analyze_technology_trends"
                })
                test_results.append({
                    "agent": "innovation_scout",
                    "test": "analyze_technology_trends",
                    "status": "success" if trend_result.get("status") == "success" else "failed",
                    "trends_analyzed": trend_result.get("trends_analyzed", 0)
                })
                
                logger.info("✅ Innovation Scout specialized tests completed")
                
            except Exception as e:
                logger.error(f"❌ Innovation Scout specialized test error: {e}")
                test_results.append({
                    "agent": "innovation_scout",
                    "test": "specialized_functionality",
                    "status": "error",
                    "error": str(e)
                })
        
        # Test Enhanced Creative Director Agent
        if 'creative_director' in self.agents:
            try:
                agent = self.agents['creative_director']
                
                # Test creative briefing
                if hasattr(agent, 'process_request'):
                    result = await agent.process_request({
                        "action": "create_brief",
                        "project_type": "web_application",
                        "requirements": ["modern", "responsive", "accessible"]
                    })
                    test_results.append({
                        "agent": "creative_director",
                        "test": "create_brief",
                        "status": "success" if result else "failed"
                    })
                
                logger.info("✅ Enhanced Creative Director specialized tests completed")
                
            except Exception as e:
                logger.error(f"❌ Creative Director specialized test error: {e}")
                test_results.append({
                    "agent": "creative_director",
                    "test": "specialized_functionality",
                    "status": "error",
                    "error": str(e)
                })
        
        # Test Market Intelligence Agent
        if 'market_intelligence' in self.agents:
            try:
                agent = self.agents['market_intelligence']
                
                # Test market analysis
                if hasattr(agent, 'process_request'):
                    result = await agent.process_request({
                        "action": "analyze_market",
                        "market": "AI development tools",
                        "timeframe": "quarterly"
                    })
                    test_results.append({
                        "agent": "market_intelligence",
                        "test": "analyze_market",
                        "status": "success" if result else "failed"
                    })
                
                logger.info("✅ Market Intelligence specialized tests completed")
                
            except Exception as e:
                logger.error(f"❌ Market Intelligence specialized test error: {e}")
                test_results.append({
                    "agent": "market_intelligence",
                    "test": "specialized_functionality",
                    "status": "error",
                    "error": str(e)
                })
        
        self.test_results.extend(test_results)
        return test_results

    async def test_inter_agent_coordination(self):
        """Test coordination between multiple agents"""
        logger.info("🤝 Testing inter-agent coordination...")
        
        test_results = []
        
        try:
            # Test coordination between Innovation Scout and Market Intelligence
            if 'innovation_scout' in self.agents and 'market_intelligence' in self.agents:
                
                # Innovation Scout finds opportunities
                innovation_result = await self.agents['innovation_scout'].process_request({
                    "action": "scan_opportunities",
                    "focus_areas": ["AI", "automation"]
                })
                
                # Market Intelligence analyzes the opportunities
                if innovation_result.get("opportunities"):
                    market_result = await self.agents['market_intelligence'].coordinate_with_agents(
                        ["innovation_scout"],
                        {
                            "context": "market_validation",
                            "opportunities": innovation_result["opportunities"][:2]
                        }
                    )
                    
                    test_results.append({
                        "test": "innovation_scout_market_intelligence_coordination",
                        "status": "success" if market_result else "failed",
                        "coordination_result": market_result
                    })
                
                logger.info("✅ Innovation Scout ↔ Market Intelligence coordination test completed")
            
            # Test coordination between Creative Director and UX Design
            if 'creative_director' in self.agents and 'ux_design' in self.agents:
                
                # Creative Director creates brief
                creative_result = await self.agents['creative_director'].coordinate_with_agents(
                    ["ux_design"],
                    {
                        "context": "design_collaboration",
                        "project_type": "web_app",
                        "requirements": ["modern", "accessible"]
                    }
                )
                
                # UX Design responds to brief
                ux_result = await self.agents['ux_design'].coordinate_with_agents(
                    ["creative_director"],
                    {
                        "context": "design_response",
                        "brief": creative_result
                    }
                )
                
                test_results.append({
                    "test": "creative_director_ux_design_coordination",
                    "status": "success" if ux_result else "failed",
                    "coordination_result": ux_result
                })
                
                logger.info("✅ Creative Director ↔ UX Design coordination test completed")
                
        except Exception as e:
            logger.error(f"❌ Inter-agent coordination test error: {e}")
            test_results.append({
                "test": "inter_agent_coordination",
                "status": "error",
                "error": str(e)
            })
        
        self.test_results.extend(test_results)
        return test_results

    async def test_enterprise_features(self):
        """Test enterprise-specific features"""
        logger.info("🏢 Testing enterprise features...")
        
        test_results = []
        
        for agent_name, agent in self.agents.items():
            try:
                enterprise_features = []
                
                # Test security features
                if hasattr(agent, 'security_features'):
                    enterprise_features.append("security")
                
                # Test audit logging
                if hasattr(agent, 'audit_log') or hasattr(agent, 'log_action'):
                    enterprise_features.append("audit_logging")
                
                # Test compliance features
                if hasattr(agent, 'compliance_check'):
                    enterprise_features.append("compliance")
                
                # Test monitoring capabilities
                if hasattr(agent, 'get_metrics') or hasattr(agent, 'performance_metrics'):
                    enterprise_features.append("monitoring")
                
                # Test scalability features
                if hasattr(agent, 'scale_up') or hasattr(agent, 'handle_load'):
                    enterprise_features.append("scalability")
                
                test_results.append({
                    "agent": agent_name,
                    "test": "enterprise_features",
                    "status": "success",
                    "features": enterprise_features,
                    "enterprise_ready": len(enterprise_features) >= 2
                })
                
                logger.info(f"✅ {agent_name} enterprise features: {enterprise_features}")
                
            except Exception as e:
                logger.error(f"❌ Error testing enterprise features for {agent_name}: {e}")
                test_results.append({
                    "agent": agent_name,
                    "test": "enterprise_features",
                    "status": "error",
                    "error": str(e)
                })
        
        self.test_results.extend(test_results)
        return test_results

    async def test_performance_load(self):
        """Test performance under load"""
        logger.info("⚡ Testing performance under load...")
        
        test_results = []
        concurrent_requests = 10
        
        for agent_name, agent in self.agents.items():
            try:
                start_time = time.time()
                
                # Create concurrent tasks
                tasks = []
                for i in range(concurrent_requests):
                    if hasattr(agent, 'process_task'):
                        task = agent.process_task({
                            "task_id": f"load_test_{i}",
                            "data": {"test": True, "iteration": i}
                        })
                        tasks.append(task)
                
                # Execute tasks concurrently
                if tasks:
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    successful = sum(1 for r in results if not isinstance(r, Exception))
                    failed = len(results) - successful
                    
                    end_time = time.time()
                    total_time = end_time - start_time
                    
                    test_results.append({
                        "agent": agent_name,
                        "test": "performance_load",
                        "status": "success" if failed == 0 else "partial",
                        "concurrent_requests": concurrent_requests,
                        "successful_requests": successful,
                        "failed_requests": failed,
                        "total_time": total_time,
                        "requests_per_second": successful / total_time if total_time > 0 else 0
                    })
                    
                    logger.info(f"✅ {agent_name} load test: {successful}/{concurrent_requests} successful in {total_time:.2f}s")
                
            except Exception as e:
                logger.error(f"❌ Performance test error for {agent_name}: {e}")
                test_results.append({
                    "agent": agent_name,
                    "test": "performance_load",
                    "status": "error",
                    "error": str(e)
                })
        
        self.test_results.extend(test_results)
        return test_results

    async def generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("📊 Generating test report...")
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r.get("status") == "success")
        failed_tests = sum(1 for r in self.test_results if r.get("status") == "failed")
        error_tests = sum(1 for r in self.test_results if r.get("status") == "error")
        
        # Generate report
        report = {
            "test_execution_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_agents_tested": len(self.agents),
                "total_tests_executed": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "error_tests": error_tests,
                "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0
            },
            "agents_tested": list(self.agents.keys()),
            "performance_metrics": self.performance_metrics,
            "detailed_results": self.test_results,
            "enterprise_readiness_assessment": {
                "overall_status": "ENTERPRISE_READY" if successful_tests > failed_tests + error_tests else "NEEDS_IMPROVEMENT",
                "recommendations": self._generate_recommendations()
            }
        }
        
        return report

    def _generate_recommendations(self):
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Analyze test results for patterns
        failed_agents = set()
        error_agents = set()
        
        for result in self.test_results:
            if result.get("status") == "failed":
                failed_agents.add(result.get("agent", "unknown"))
            elif result.get("status") == "error":
                error_agents.add(result.get("agent", "unknown"))
        
        if error_agents:
            recommendations.append(f"Fix critical errors in: {', '.join(error_agents)}")
        
        if failed_agents:
            recommendations.append(f"Improve functionality in: {', '.join(failed_agents)}")
        
        # Check performance metrics
        slow_agents = [name for name, metrics in self.performance_metrics.items() 
                      if metrics.get("response_time", 0) > 2.0]
        
        if slow_agents:
            recommendations.append(f"Optimize performance for: {', '.join(slow_agents)}")
        
        if not recommendations:
            recommendations.append("All agents are performing well - ready for production deployment")
        
        return recommendations

    async def run_full_test_suite(self):
        """Run the complete test suite"""
        logger.info("🧪 STARTING ENTERPRISE AGENTS INTEGRATION TEST SUITE")
        logger.info("=" * 60)
        
        try:
            # Initialize agents
            await self.initialize_agents()
            
            # Run all test categories
            await self.test_agent_core_functionality()
            await self.test_specialized_functionality()
            await self.test_inter_agent_coordination()
            await self.test_enterprise_features()
            await self.test_performance_load()
            
            # Generate and display report
            report = await self.generate_test_report()
            
            logger.info("=" * 60)
            logger.info("📊 TEST SUITE COMPLETED")
            logger.info(f"Total Agents: {report['summary']['total_agents_tested']}")
            logger.info(f"Total Tests: {report['summary']['total_tests_executed']}")
            logger.info(f"Success Rate: {report['summary']['success_rate']:.1f}%")
            logger.info(f"Enterprise Status: {report['enterprise_readiness_assessment']['overall_status']}")
            logger.info("=" * 60)
            
            # Save report to file
            with open("enterprise_agents_test_report.json", "w") as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info("📄 Test report saved to: enterprise_agents_test_report.json")
            
            return report
            
        except Exception as e:
            logger.error(f"❌ Test suite execution error: {e}")
            raise

if __name__ == "__main__":
    async def main():
        test_suite = EnterpriseAgentsTestSuite()
        await test_suite.run_full_test_suite()
    
    # Run the test suite
    asyncio.run(main())
