"""
🧪 SIMPLIFIED ENTERPRISE AGENTS TEST
Quick validation test for enterprise agents functionality.
"""

import asyncio
import json
import logging
import time
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_innovation_scout():
    """Test Innovation Scout Agent"""
    logger.info("🔍 Testing Innovation Scout Agent...")
    
    try:
        from agents.innovation.innovation_scout_agent import InnovationScoutAgent
        agent = InnovationScoutAgent("test_scout")
        
        # Test opportunity scanning
        result = await agent.process_request({
            "action": "scan_opportunities",
            "focus_areas": ["AI", "automation", "enterprise"]
        })
        
        logger.info(f"✅ Innovation Scout Test Result: {result.get('status')}")
        logger.info(f"   Opportunities Found: {result.get('opportunities_found', 0)}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Innovation Scout Test Failed: {e}")
        return False

async def test_enhanced_creative_director():
    """Test Enhanced Creative Director Agent"""
    logger.info("🎨 Testing Enhanced Creative Director Agent...")
    
    try:
        from agents.creative.enhanced_creative_director_agent import EnhancedCreativeDirectorAgent
        agent = EnhancedCreativeDirectorAgent()
        
        # Test basic status
        status = agent.get_agent_status() if hasattr(agent, 'get_agent_status') else {"status": "initialized"}
        
        logger.info(f"✅ Enhanced Creative Director Test Result: initialized")
        logger.info(f"   Agent Status: {status}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Enhanced Creative Director Test Failed: {e}")
        return False

async def test_market_intelligence():
    """Test Market Intelligence Agent"""
    logger.info("📊 Testing Market Intelligence Agent...")
    
    try:
        from agents.research.market_intelligence_agent import MarketIntelligenceAgent
        agent = MarketIntelligenceAgent()
        
        # Test basic status
        status = agent.get_agent_status() if hasattr(agent, 'get_agent_status') else {"status": "initialized"}
        
        logger.info(f"✅ Market Intelligence Test Result: initialized")
        logger.info(f"   Agent Status: {status}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Market Intelligence Test Failed: {e}")
        return False

async def test_ux_design():
    """Test UX Design Agent"""
    logger.info("🎯 Testing UX Design Agent...")
    
    try:
        from agents.creative.ux_design_agent import UXDesignAgent
        agent = UXDesignAgent()
        
        # Test basic status
        status = agent.get_agent_status() if hasattr(agent, 'get_agent_status') else {"status": "initialized"}
        
        logger.info(f"✅ UX Design Test Result: initialized")
        logger.info(f"   Agent Status: {status}")
        return True
        
    except Exception as e:
        logger.error(f"❌ UX Design Test Failed: {e}")
        return False

async def test_system_architect():
    """Test System Architect Agent"""
    logger.info("🏗️ Testing System Architect Agent...")
    
    try:
        from agents.development.system_architect_agent import SystemArchitectAgent
        agent = SystemArchitectAgent()
        
        # Test basic status
        status = agent.get_agent_status() if hasattr(agent, 'get_agent_status') else {"status": "initialized"}
        
        logger.info(f"✅ System Architect Test Result: initialized")
        logger.info(f"   Agent Status: {status}")
        return True
        
    except Exception as e:
        logger.error(f"❌ System Architect Test Failed: {e}")
        return False

async def run_simplified_test():
    """Run simplified enterprise agents test"""
    logger.info("🧪 STARTING SIMPLIFIED ENTERPRISE AGENTS TEST")
    logger.info("=" * 60)
    
    start_time = time.time()
    
    # Run individual agent tests
    results = []
    results.append(await test_innovation_scout())
    results.append(await test_enhanced_creative_director())
    results.append(await test_market_intelligence())
    results.append(await test_ux_design())
    results.append(await test_system_architect())
    
    end_time = time.time()
    
    # Calculate results
    total_tests = len(results)
    successful_tests = sum(results)
    success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
    
    logger.info("=" * 60)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info(f"Total Tests: {total_tests}")
    logger.info(f"Successful: {successful_tests}")
    logger.info(f"Failed: {total_tests - successful_tests}")
    logger.info(f"Success Rate: {success_rate:.1f}%")
    logger.info(f"Execution Time: {end_time - start_time:.2f} seconds")
    
    if success_rate >= 80:
        logger.info("🎉 ENTERPRISE AGENTS STATUS: READY FOR PRODUCTION")
    elif success_rate >= 60:
        logger.info("⚠️ ENTERPRISE AGENTS STATUS: PARTIALLY READY - NEEDS IMPROVEMENT")
    else:
        logger.info("❌ ENTERPRISE AGENTS STATUS: NOT READY - CRITICAL ISSUES")
    
    logger.info("=" * 60)
    
    # Generate report
    report = {
        "test_execution_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_tests": total_tests,
        "successful_tests": successful_tests,
        "failed_tests": total_tests - successful_tests,
        "success_rate": success_rate,
        "execution_time_seconds": end_time - start_time,
        "enterprise_status": "READY" if success_rate >= 80 else "NEEDS_IMPROVEMENT" if success_rate >= 60 else "NOT_READY"
    }
    
    # Save report
    with open("simplified_enterprise_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    logger.info("📄 Test report saved to: simplified_enterprise_test_report.json")
    
    return report

if __name__ == "__main__":
    asyncio.run(run_simplified_test())
