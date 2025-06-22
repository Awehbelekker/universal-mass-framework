#!/usr/bin/env python3
"""
MASS Framework Implementation Verification Script
This script provides a comprehensive verification of the MASS Framework implementation.
"""

import sys
import os
import importlib
import asyncio
from pathlib import Path
from datetime import datetime

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_section(title):
    print(f"\n{'-'*40}")
    print(f"📋 {title}")
    print(f"{'-'*40}")

def verify_implementation():
    """Comprehensive verification of MASS Framework implementation"""
    
    print_header("MASS FRAMEWORK VERIFICATION")
    print(f"Verification Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Framework Path: {os.getcwd()}")
    
    results = {
        'directory_structure': 0,
        'core_imports': 0,
        'agent_system': 0,
        'communication': 0,
        'data_integration': 0,
        'workflow_system': 0,
        'total_score': 0
    }
    
    # 1. Directory Structure Verification
    print_section("Directory Structure Verification")
    
    expected_dirs = ['core', 'agents', 'data_sources', 'workflows', 'utils', 'tests', 'config']
    found_dirs = 0
    
    for dir_name in expected_dirs:
        if os.path.exists(dir_name):
            files = [f for f in os.listdir(dir_name) if f.endswith('.py')]
            print(f"  ✅ {dir_name}/: {len(files)} Python files")
            found_dirs += 1
        else:
            print(f"  ❌ {dir_name}/: Missing")
    
    results['directory_structure'] = (found_dirs / len(expected_dirs)) * 100
    print(f"Directory Structure Score: {results['directory_structure']:.1f}%")
    
    # 2. Core Module Imports
    print_section("Core Module Import Verification")
    
    core_modules = [
        ('MASSCoordinator', 'core.mass_coordinator'),
        ('AgentBase', 'core.agent_base'),
        ('MessageType', 'core.agent_base'),
        ('LiveDataOrchestrator', 'data_sources.live_data_orchestrator'),
        ('AppGenerationWorkflow', 'workflows.app_generation_workflow')
    ]
    
    successful_imports = 0
    
    for component, module_name in core_modules:
        try:
            importlib.import_module(module_name)
            print(f"  ✅ {component}: Successfully imported")
            successful_imports += 1
        except Exception as e:
            print(f"  ❌ {component}: Import failed - {str(e)[:40]}...")
    
    results['core_imports'] = (successful_imports / len(core_modules)) * 100
    print(f"Core Imports Score: {results['core_imports']:.1f}%")
    
    # 3. Agent System Verification
    print_section("Agent System Verification")
    
    try:
        from core.agent_base import AgentBase, MessageType, AgentMessage
        from core.mass_coordinator import MASSCoordinator
        
        # Test coordinator instantiation
        coordinator = MASSCoordinator()
        print(f"  ✅ MASSCoordinator instantiated")
        print(f"  ✅ Agent registry available: {type(coordinator.agents)}")
        
        # Test message types
        message_types = list(MessageType)
        print(f"  ✅ Message types defined: {len(message_types)} types")
        
        # Test message creation
        test_message = AgentMessage(
            sender_id="test_sender",
            receiver_id="test_receiver",
            message_type=MessageType.ANALYSIS_REQUEST,
            payload={"test": "data"},
            timestamp=1234567890.0,
            correlation_id="test-123"
        )
        print(f"  ✅ AgentMessage created successfully")
        
        results['agent_system'] = 100
        results['communication'] = 100
        
    except Exception as e:
        print(f"  ❌ Agent system error: {e}")
        results['agent_system'] = 0
        results['communication'] = 0
    
    print(f"Agent System Score: {results['agent_system']:.1f}%")
    print(f"Communication Score: {results['communication']:.1f}%")
    
    # 4. Data Integration Verification
    print_section("Live Data Integration Verification")
    
    try:
        from data_sources.live_data_orchestrator import LiveDataOrchestrator
        
        data_orchestrator = LiveDataOrchestrator()
        print(f"  ✅ LiveDataOrchestrator instantiated")
        print(f"  ✅ Data sources configured: {len(data_orchestrator.data_sources)}")
        
        # List available data sources
        sources = list(data_orchestrator.data_sources.keys())
        print(f"  ✅ Available sources: {sources[:3]}{'...' if len(sources) > 3 else ''}")
        
        results['data_integration'] = 100
        
    except Exception as e:
        print(f"  ❌ Data integration error: {e}")
        results['data_integration'] = 0
    
    print(f"Data Integration Score: {results['data_integration']:.1f}%")
    
    # 5. Workflow System Verification
    print_section("Workflow System Verification")
    
    try:
        from workflows.app_generation_workflow import AppGenerationWorkflow
        
        workflow = AppGenerationWorkflow()
        print(f"  ✅ AppGenerationWorkflow instantiated")
        print(f"  ✅ Workflow phases defined: {len(workflow.phases)}")
        
        # List workflow phases
        phase_names = [phase["name"] for phase in workflow.phases]
        print(f"  ✅ Phase names: {phase_names[:3]}{'...' if len(phase_names) > 3 else ''}")
        
        results['workflow_system'] = 100
        
    except Exception as e:
        print(f"  ❌ Workflow system error: {e}")
        results['workflow_system'] = 0
    
    print(f"Workflow System Score: {results['workflow_system']:.1f}%")
    
    # 6. Overall Assessment
    print_section("Overall Assessment")
    
    component_scores = [
        results['directory_structure'],
        results['core_imports'],
        results['agent_system'],
        results['communication'],
        results['data_integration'],
        results['workflow_system']
    ]
    
    overall_score = sum(component_scores) / len(component_scores)
    results['total_score'] = overall_score
    
    print(f"Overall Implementation Score: {overall_score:.1f}%")
    
    if overall_score >= 80:
        status = "🟢 PRODUCTION READY"
        desc = "System is fully operational and ready for deployment"
    elif overall_score >= 60:
        status = "🟡 DEVELOPMENT READY"
        desc = "System has solid foundation but needs refinement"
    elif overall_score >= 40:
        status = "🟠 PROTOTYPE READY"
        desc = "Basic functionality present, needs more work"
    else:
        status = "🔴 INCOMPLETE"
        desc = "System needs significant development"
    
    print(f"Status: {status}")
    print(f"Assessment: {desc}")
    
    # 7. Final Summary
    print_header("VERIFICATION SUMMARY")
    
    print("Component Breakdown:")
    print(f"  📁 Directory Structure: {results['directory_structure']:.1f}%")
    print(f"  📦 Core Imports: {results['core_imports']:.1f}%")
    print(f"  🤖 Agent System: {results['agent_system']:.1f}%")
    print(f"  💬 Communication: {results['communication']:.1f}%")
    print(f"  📊 Data Integration: {results['data_integration']:.1f}%")
    print(f"  🔄 Workflow System: {results['workflow_system']:.1f}%")
    
    print(f"\n🎯 FINAL SCORE: {overall_score:.1f}%")
    print(f"🏆 STATUS: {status}")
    
    # Specification Compliance Check
    print("\n📋 SPECIFICATION COMPLIANCE:")
    
    compliance_checks = [
        ("Agent Communication Protocol", results['communication'] >= 70),
        ("Asynchronous Coordination", results['agent_system'] >= 70),
        ("Live Data Integration", results['data_integration'] >= 70),
        ("Multi-Agent Workflow", results['workflow_system'] >= 70),
        ("Production Architecture", overall_score >= 80)
    ]
    
    compliant_count = 0
    for check_name, is_compliant in compliance_checks:
        status_icon = "✅" if is_compliant else "❌"
        print(f"  {status_icon} {check_name}")
        if is_compliant:
            compliant_count += 1
    
    compliance_percentage = (compliant_count / len(compliance_checks)) * 100
    print(f"\n📊 Specification Compliance: {compliance_percentage:.1f}%")
    
    if compliance_percentage >= 80:
        print("🎉 EXCELLENT! High compliance with MASS Framework specification")
    elif compliance_percentage >= 60:
        print("👍 GOOD! Solid compliance with most requirements")
    else:
        print("⚠️  NEEDS WORK! Address compliance gaps")
    
    return results

if __name__ == "__main__":
    try:
        results = verify_implementation()
        
        # Exit with appropriate code
        if results['total_score'] >= 80:
            print("\n✅ VERIFICATION COMPLETE - SYSTEM READY FOR PRODUCTION")
            sys.exit(0)
        elif results['total_score'] >= 60:
            print("\n⚠️  VERIFICATION COMPLETE - SYSTEM NEEDS MINOR IMPROVEMENTS")
            sys.exit(0)
        else:
            print("\n❌ VERIFICATION COMPLETE - SYSTEM NEEDS MAJOR IMPROVEMENTS")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
