#!/usr/bin/env python3
"""
Universal MASS Framework - Implementation Validation Report
==========================================================

Comprehensive validation and cleanup report for the Universal MASS Framework.
This script validates the implementation status and provides recommendations
for cleanup and optimization.

Author: Universal MASS Framework Team
Date: June 22, 2025
Version: 1.0.0
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ValidationResult:
    """Validation result for a component"""
    component: str
    status: str  # "complete", "partial", "missing", "error"
    files_found: List[str]
    files_missing: List[str]
    size_kb: float
    issues: List[str]
    recommendations: List[str]

class MassFrameworkValidator:
    """Comprehensive validation of MASS Framework implementation"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.validation_results = {}
        self.total_files = 0
        self.total_size_mb = 0
        self.issues_found = []
        self.recommendations = []
        
    def validate_core_framework(self) -> ValidationResult:
        """Validate core framework components"""
        core_files = [
            "universal_mass_framework/core/mass_engine.py",
            "universal_mass_framework/core/intelligence_layer.py", 
            "universal_mass_framework/core/agent_coordinator.py",
            "universal_mass_framework/core/config_manager.py"
        ]
        
        found_files = []
        missing_files = []
        total_size = 0
        issues = []
        
        for file_path in core_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                found_files.append(file_path)
                total_size += full_path.stat().st_size / 1024  # KB
            else:
                missing_files.append(file_path)
                issues.append(f"Missing core file: {file_path}")
        
        status = "complete" if len(missing_files) == 0 else "partial"
        
        recommendations = []
        if missing_files:
            recommendations.append("Recreate missing core framework files")
        if total_size < 50:  # KB
            recommendations.append("Core files seem too small - verify implementations")
            
        return ValidationResult(
            component="Core Framework",
            status=status,
            files_found=found_files,
            files_missing=missing_files,
            size_kb=total_size,
            issues=issues,
            recommendations=recommendations
        )
    
    def validate_data_processors(self) -> ValidationResult:
        """Validate data processors implementation"""
        processor_files = [
            "universal_mass_framework/data_orchestration/data_processors/pattern_analyzer.py",
            "universal_mass_framework/data_orchestration/data_processors/predictive_analyzer.py",
            "universal_mass_framework/data_orchestration/data_processors/correlation_engine.py",
            "universal_mass_framework/data_orchestration/data_processors/insight_generator.py",
            "universal_mass_framework/data_orchestration/data_processors/anomaly_detector.py",
            "universal_mass_framework/data_orchestration/data_processors/real_time_processor.py",
            "universal_mass_framework/data_orchestration/data_processors/__init__.py"
        ]
        
        found_files = []
        missing_files = []
        total_size = 0
        issues = []
        
        for file_path in processor_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                found_files.append(file_path)
                size_kb = full_path.stat().st_size / 1024
                total_size += size_kb
                
                # Check if files are substantial (should be large implementations)
                if file_path.endswith("pattern_analyzer.py") and size_kb < 100:
                    issues.append("Pattern analyzer implementation seems too small")
                elif file_path.endswith("predictive_analyzer.py") and size_kb < 100:
                    issues.append("Predictive analyzer implementation seems too small")
            else:
                missing_files.append(file_path)
                issues.append(f"Missing data processor: {file_path}")
        
        status = "complete" if len(missing_files) == 0 else "partial"
        
        recommendations = []
        if missing_files:
            recommendations.append("Recreate missing data processor files")
        if total_size < 500:  # KB - data processors should be substantial
            recommendations.append("Data processors seem too small - verify comprehensive implementations")
            
        return ValidationResult(
            component="Data Processors",
            status=status,
            files_found=found_files,
            files_missing=missing_files,
            size_kb=total_size,
            issues=issues,
            recommendations=recommendations
        )
    
    def validate_intelligence_agents(self) -> ValidationResult:
        """Validate intelligence agents implementation"""
        agent_files = [
            "universal_mass_framework/intelligence_agents/data_analyzer_agent.py",
            "universal_mass_framework/intelligence_agents/predictive_agent.py",
            "universal_mass_framework/intelligence_agents/__init__.py"
        ]
        
        found_files = []
        missing_files = []
        total_size = 0
        issues = []
        
        for file_path in agent_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                found_files.append(file_path)
                total_size += full_path.stat().st_size / 1024  # KB
            else:
                missing_files.append(file_path)
                issues.append(f"Missing intelligence agent: {file_path}")
        
        status = "complete" if len(missing_files) == 0 else "partial"
        
        recommendations = []
        if missing_files:
            recommendations.append("Recreate missing intelligence agent files")
            
        return ValidationResult(
            component="Intelligence Agents",
            status=status,
            files_found=found_files,
            files_missing=missing_files,
            size_kb=total_size,
            issues=issues,
            recommendations=recommendations
        )
    
    def validate_data_orchestration(self) -> ValidationResult:
        """Validate data orchestration components"""
        orchestration_files = [
            "universal_mass_framework/data_orchestration/real_world_data_orchestrator.py",
            "universal_mass_framework/data_orchestration/base_data_source.py",
            "universal_mass_framework/data_orchestration/__init__.py"
        ]
        
        found_files = []
        missing_files = []
        total_size = 0
        issues = []
        
        for file_path in orchestration_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                found_files.append(file_path)
                total_size += full_path.stat().st_size / 1024  # KB
            else:
                missing_files.append(file_path)
                issues.append(f"Missing orchestration file: {file_path}")
        
        # Check for data sources directory
        data_sources_dir = self.base_path / "universal_mass_framework/data_orchestration/data_sources"
        if data_sources_dir.exists():
            source_files = list(data_sources_dir.glob("*.py"))
            found_files.extend([str(f.relative_to(self.base_path)) for f in source_files])
            total_size += sum(f.stat().st_size / 1024 for f in source_files)
        else:
            issues.append("Data sources directory missing")
        
        status = "complete" if len(missing_files) == 0 else "partial"
        
        recommendations = []
        if missing_files:
            recommendations.append("Recreate missing data orchestration files")
        if not data_sources_dir.exists():
            recommendations.append("Create data sources directory and implementations")
            
        return ValidationResult(
            component="Data Orchestration",
            status=status,
            files_found=found_files,
            files_missing=missing_files,
            size_kb=total_size,
            issues=issues,
            recommendations=recommendations
        )
    
    def validate_documentation(self) -> ValidationResult:
        """Validate documentation completeness"""
        doc_files = [
            "UNIVERSAL_MASS_FRAMEWORK_COMPLETE.md",
            "QUICK_START_GUIDE.md",
            "IMPLEMENTATION_COMPLETE_SUMMARY.md",
            "README.md"
        ]
        
        found_files = []
        missing_files = []
        total_size = 0
        issues = []
        
        for file_path in doc_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                found_files.append(file_path)
                total_size += full_path.stat().st_size / 1024  # KB
            else:
                missing_files.append(file_path)
                issues.append(f"Missing documentation: {file_path}")
        
        status = "complete" if len(missing_files) == 0 else "partial"
        
        recommendations = []
        if missing_files:
            recommendations.append("Create missing documentation files")
        if total_size < 50:  # KB
            recommendations.append("Documentation seems too small - add more comprehensive content")
            
        return ValidationResult(
            component="Documentation",
            status=status,
            files_found=found_files,
            files_missing=missing_files,
            size_kb=total_size,
            issues=issues,
            recommendations=recommendations
        )
    
    def validate_testing_infrastructure(self) -> ValidationResult:
        """Validate testing and validation infrastructure"""
        test_files = [
            "test_framework_validation.py",
            "demo_data_processors.py",
            "verify_implementation.py"
        ]
        
        found_files = []
        missing_files = []
        total_size = 0
        issues = []
        
        for file_path in test_files:
            full_path = self.base_path / file_path
            if full_path.exists():
                found_files.append(file_path)
                total_size += full_path.stat().st_size / 1024  # KB
            else:
                missing_files.append(file_path)
                issues.append(f"Missing test file: {file_path}")
        
        # Check for tests directory
        tests_dir = self.base_path / "tests"
        if tests_dir.exists():
            test_files_dir = list(tests_dir.glob("*.py"))
            found_files.extend([str(f.relative_to(self.base_path)) for f in test_files_dir])
            total_size += sum(f.stat().st_size / 1024 for f in test_files_dir)
        
        status = "complete" if len(missing_files) == 0 else "partial"
        
        recommendations = []
        if missing_files:
            recommendations.append("Create missing test files")
        if total_size < 20:  # KB
            recommendations.append("Testing infrastructure seems insufficient")
            
        return ValidationResult(
            component="Testing Infrastructure",
            status=status,
            files_found=found_files,
            files_missing=missing_files,
            size_kb=total_size,
            issues=issues,
            recommendations=recommendations
        )
    
    def check_redundant_files(self) -> List[str]:
        """Check for redundant or unnecessary files"""
        redundant_patterns = [
            "*.log",
            "*.tmp", 
            "*.cache",
            "__pycache__",
            ".pytest_cache",
            "*.pyc",
            ".DS_Store",
            "Thumbs.db",
            "*.bak",
            "*_old.*",
            "*_backup.*"
        ]
        
        redundant_files = []
        for pattern in redundant_patterns:
            redundant_files.extend(self.base_path.glob(f"**/{pattern}"))
        
        return [str(f.relative_to(self.base_path)) for f in redundant_files]
    
    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze dependency requirements"""
        requirements_files = [
            "requirements.txt",
            "requirements-minimal.txt",
            "requirements-functional.txt"
        ]
        
        found_requirements = []
        for req_file in requirements_files:
            if (self.base_path / req_file).exists():
                found_requirements.append(req_file)
        
        return {
            "requirements_files": found_requirements,
            "has_multiple_requirements": len(found_requirements) > 1,
            "needs_consolidation": len(found_requirements) > 2
        }
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run complete validation of MASS Framework"""
        print("🔍 UNIVERSAL MASS FRAMEWORK VALIDATION")
        print("=" * 50)
        print(f"Validation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Framework Path: {self.base_path.absolute()}")
        print()
        
        # Run all validations
        validations = {
            "core_framework": self.validate_core_framework(),
            "data_processors": self.validate_data_processors(),
            "intelligence_agents": self.validate_intelligence_agents(),
            "data_orchestration": self.validate_data_orchestration(),
            "documentation": self.validate_documentation(),
            "testing": self.validate_testing_infrastructure()
        }
        
        # Analyze additional aspects
        redundant_files = self.check_redundant_files()
        dependencies = self.analyze_dependencies()
        
        # Calculate overall metrics
        total_components = len(validations)
        complete_components = sum(1 for v in validations.values() if v.status == "complete")
        total_files = sum(len(v.files_found) for v in validations.values())
        total_size_mb = sum(v.size_kb for v in validations.values()) / 1024
        total_issues = sum(len(v.issues) for v in validations.values())
        
        completion_rate = (complete_components / total_components) * 100
        
        # Generate report
        print("📊 VALIDATION RESULTS")
        print("-" * 30)
        
        for component, result in validations.items():
            status_icon = "✅" if result.status == "complete" else "⚠️" if result.status == "partial" else "❌"
            print(f"{status_icon} {result.component}: {result.status.upper()}")
            print(f"   Files Found: {len(result.files_found)}")
            print(f"   Size: {result.size_kb:.1f} KB")
            if result.issues:
                print(f"   Issues: {len(result.issues)}")
                for issue in result.issues[:3]:  # Show first 3 issues
                    print(f"     - {issue}")
            print()
        
        print("🧹 CLEANUP ANALYSIS")
        print("-" * 30)
        print(f"Redundant Files Found: {len(redundant_files)}")
        if redundant_files:
            print("Files to clean:")
            for f in redundant_files[:10]:  # Show first 10
                print(f"  - {f}")
            if len(redundant_files) > 10:
                print(f"  ... and {len(redundant_files) - 10} more")
        print()
        
        print("📦 DEPENDENCIES ANALYSIS")
        print("-" * 30)
        print(f"Requirements Files: {dependencies['requirements_files']}")
        if dependencies['needs_consolidation']:
            print("⚠️  Recommendation: Consolidate multiple requirements files")
        print()
        
        print("📈 OVERALL METRICS")
        print("-" * 30)
        print(f"Completion Rate: {completion_rate:.1f}%")
        print(f"Total Components: {total_components}")
        print(f"Complete Components: {complete_components}")
        print(f"Total Files: {total_files}")
        print(f"Total Size: {total_size_mb:.1f} MB")
        print(f"Issues Found: {total_issues}")
        print()
        
        # Overall assessment
        if completion_rate >= 90:
            status = "🎉 EXCELLENT - Production Ready"
            grade = "A+"
        elif completion_rate >= 80:
            status = "✅ GOOD - Minor improvements needed"
            grade = "A-"
        elif completion_rate >= 70:
            status = "⚠️  FAIR - Some work required"
            grade = "B"
        else:
            status = "❌ POOR - Major work required"
            grade = "C"
        
        print(f"🏆 FINAL ASSESSMENT: {status}")
        print(f"📊 GRADE: {grade}")
        print()
        
        return {
            "validation_results": validations,
            "completion_rate": completion_rate,
            "total_files": total_files,
            "total_size_mb": total_size_mb,
            "total_issues": total_issues,
            "redundant_files": redundant_files,
            "dependencies": dependencies,
            "overall_status": status,
            "grade": grade,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_cleanup_recommendations(self) -> List[str]:
        """Generate specific cleanup recommendations"""
        recommendations = [
            "🧹 CLEANUP RECOMMENDATIONS",
            "=" * 40,
            "",
            "1. FILE CLEANUP:",
            "   - Remove __pycache__ directories",
            "   - Delete .pyc files",
            "   - Clean up .log files",
            "   - Remove backup files (*_old.*, *_backup.*)",
            "",
            "2. DEPENDENCY MANAGEMENT:",
            "   - Consolidate requirements files",
            "   - Remove unused dependencies",
            "   - Update package versions",
            "",
            "3. DOCUMENTATION ORGANIZATION:",
            "   - Move technical docs to docs/ folder",
            "   - Consolidate deployment guides",
            "   - Update README.md with current status",
            "",
            "4. CODE ORGANIZATION:",
            "   - Remove unused deployment scripts",
            "   - Consolidate testing files",
            "   - Clean up configuration files",
            "",
            "5. DEPLOYMENT PREPARATION:",
            "   - Create single deployment script",
            "   - Prepare production configuration",
            "   - Set up monitoring scripts",
            "",
            "🎯 PRIORITY ACTIONS:",
            "   1. Validate all core components work correctly",
            "   2. Clean up redundant files",
            "   3. Consolidate documentation",
            "   4. Prepare production deployment package",
            "   5. Create comprehensive testing suite"
        ]
        
        return recommendations

def main():
    """Main validation function"""
    validator = MassFrameworkValidator()
    results = validator.run_comprehensive_validation()
    
    # Generate cleanup recommendations
    print("💡 CLEANUP RECOMMENDATIONS")
    print("=" * 50)
    recommendations = validator.generate_cleanup_recommendations()
    for rec in recommendations:
        print(rec)
    
    # Save results to file
    report_file = "mass_framework_validation_report.json"
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    return results

if __name__ == "__main__":
    main()
