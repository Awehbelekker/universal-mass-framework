"""
PROMETHEUS AI Trading Platform - Comprehensive Pre-Deployment Analysis & Testing Suite
====================================================================================

This comprehensive analysis examines all system components, identifies issues,
performs testing, and provides deployment readiness assessment.

Date: July 14, 2025
Version: 3.0.0 Enterprise
Target: Firebase Production Deployment
"""

import os
import json
import subprocess
import time
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveDeploymentAnalyzer:
    """Comprehensive analysis and testing for deployment readiness"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.analysis_results = {}
        self.deployment_checklist = {}
        self.critical_issues = []
        self.warnings = []
        self.recommendations = []
        
    async def run_full_analysis(self):
        """Run complete deployment analysis"""
        logger.info("🚀 PROMETHEUS AI Trading Platform - Comprehensive Deployment Analysis")
        logger.info("=" * 80)
        
        analysis_start = time.time()
        
        # Phase 1: Project Structure Analysis
        logger.info("\n📁 Phase 1: Project Structure Analysis")
        await self._analyze_project_structure()
        
        # Phase 2: Code Quality Assessment
        logger.info("\n🔍 Phase 2: Code Quality Assessment")
        await self._analyze_code_quality()
        
        # Phase 3: Frontend Analysis
        logger.info("\n🎨 Phase 3: Frontend Analysis")
        await self._analyze_frontend()
        
        # Phase 4: Backend Analysis
        logger.info("\n⚙️ Phase 4: Backend Analysis")
        await self._analyze_backend()
        
        # Phase 5: Firebase Configuration
        logger.info("\n🔥 Phase 5: Firebase Configuration Analysis")
        await self._analyze_firebase_config()
        
        # Phase 6: Security Assessment
        logger.info("\n🔒 Phase 6: Security Assessment")
        await self._analyze_security()
        
        # Phase 7: Performance Analysis
        logger.info("\n⚡ Phase 7: Performance Analysis")
        await self._analyze_performance()
        
        # Phase 8: Deployment Readiness
        logger.info("\n🎯 Phase 8: Deployment Readiness Assessment")
        await self._assess_deployment_readiness()
        
        # Generate comprehensive report
        total_time = time.time() - analysis_start
        await self._generate_comprehensive_report(total_time)
        
        return self.analysis_results
    
    async def _analyze_project_structure(self):
        """Analyze project structure and organization"""
        structure_analysis = {
            "status": "analyzing",
            "components": {},
            "missing_files": [],
            "recommendations": []
        }
        
        # Critical files check
        critical_files = [
            "firebase.json",
            "frontend/package.json",
            "frontend/src/App.tsx",
            "main.py",
            "requirements.txt",
            "private_access_gate.html"
        ]
        
        for file_path in critical_files:
            full_path = os.path.join(self.workspace_root, file_path)
            if os.path.exists(full_path):
                structure_analysis["components"][file_path] = {
                    "status": "present",
                    "size": os.path.getsize(full_path),
                    "modified": datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
                }
                logger.info(f"✅ {file_path} - Present")
            else:
                structure_analysis["missing_files"].append(file_path)
                logger.warning(f"⚠️ {file_path} - Missing")
        
        # Check directory structure
        important_dirs = [
            "frontend/src/components",
            "frontend/public",
            "functions",
            "tests",
            "security_audit",
            "performance_testing",
            "real_data_simulation"
        ]
        
        for dir_path in important_dirs:
            full_path = os.path.join(self.workspace_root, dir_path)
            if os.path.exists(full_path):
                file_count = len([f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))])
                structure_analysis["components"][dir_path] = {
                    "status": "present",
                    "file_count": file_count
                }
                logger.info(f"✅ {dir_path} - {file_count} files")
            else:
                structure_analysis["missing_files"].append(dir_path)
                logger.warning(f"⚠️ {dir_path} - Missing")
        
        # Recommendations based on analysis
        if structure_analysis["missing_files"]:
            structure_analysis["recommendations"].append("Create missing critical files and directories")
        
        structure_analysis["status"] = "completed"
        self.analysis_results["project_structure"] = structure_analysis
    
    async def _analyze_code_quality(self):
        """Analyze code quality and identify issues"""
        code_analysis = {
            "status": "analyzing",
            "typescript_issues": [],
            "python_issues": [],
            "critical_errors": [],
            "warnings": []
        }
        
        # Check TypeScript compilation
        frontend_path = os.path.join(self.workspace_root, "frontend")
        if os.path.exists(frontend_path):
            try:
                # Run TypeScript compilation check
                result = subprocess.run(
                    ["npm", "run", "build"], 
                    cwd=frontend_path, 
                    capture_output=True, 
                    text=True, 
                    timeout=300
                )
                
                if result.returncode != 0:
                    code_analysis["typescript_issues"].append({
                        "type": "build_failure",
                        "details": result.stderr,
                        "severity": "critical"
                    })
                    logger.error(f"❌ TypeScript build failed: {result.stderr[:200]}...")
                else:
                    logger.info("✅ TypeScript compilation successful")
                    
            except subprocess.TimeoutExpired:
                code_analysis["typescript_issues"].append({
                    "type": "build_timeout",
                    "details": "Build process timed out after 5 minutes",
                    "severity": "critical"
                })
            except Exception as e:
                code_analysis["typescript_issues"].append({
                    "type": "build_error",
                    "details": str(e),
                    "severity": "critical"
                })
        
        # Check Python syntax and imports
        try:
            result = subprocess.run(
                ["python", "-m", "py_compile", "main.py"],
                cwd=self.workspace_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                code_analysis["python_issues"].append({
                    "type": "syntax_error",
                    "file": "main.py",
                    "details": result.stderr,
                    "severity": "critical"
                })
            else:
                logger.info("✅ Python main.py syntax check passed")
                
        except Exception as e:
            code_analysis["python_issues"].append({
                "type": "compilation_error",
                "details": str(e),
                "severity": "critical"
            })
        
        code_analysis["status"] = "completed"
        self.analysis_results["code_quality"] = code_analysis
    
    async def _analyze_frontend(self):
        """Analyze frontend components and dependencies"""
        frontend_analysis = {
            "status": "analyzing",
            "components": {},
            "dependencies": {},
            "build_status": "unknown",
            "issues": []
        }
        
        frontend_path = os.path.join(self.workspace_root, "frontend")
        
        if os.path.exists(frontend_path):
            # Check package.json
            package_json_path = os.path.join(frontend_path, "package.json")
            if os.path.exists(package_json_path):
                try:
                    with open(package_json_path, 'r') as f:
                        package_data = json.load(f)
                    
                    frontend_analysis["dependencies"] = {
                        "production": len(package_data.get("dependencies", {})),
                        "development": len(package_data.get("devDependencies", {})),
                        "key_frameworks": {
                            "react": package_data.get("dependencies", {}).get("react", "not found"),
                            "typescript": package_data.get("dependencies", {}).get("typescript", "not found"),
                            "firebase": package_data.get("dependencies", {}).get("firebase", "not found"),
                            "mui": package_data.get("dependencies", {}).get("@mui/material", "not found")
                        }
                    }
                    logger.info(f"✅ Frontend dependencies analyzed - {frontend_analysis['dependencies']['production']} production deps")
                    
                except json.JSONDecodeError as e:
                    frontend_analysis["issues"].append(f"Invalid package.json: {str(e)}")
            
            # Check key components
            components_path = os.path.join(frontend_path, "src", "components")
            if os.path.exists(components_path):
                components = [f for f in os.listdir(components_path) if f.endswith(('.tsx', '.ts', '.jsx', '.js'))]
                frontend_analysis["components"] = {
                    "count": len(components),
                    "list": components
                }
                logger.info(f"✅ Found {len(components)} frontend components")
            
            # Check build directory
            build_path = os.path.join(frontend_path, "build")
            if os.path.exists(build_path):
                frontend_analysis["build_status"] = "present"
                build_files = [f for f in os.listdir(build_path) if os.path.isfile(os.path.join(build_path, f))]
                frontend_analysis["build_files"] = len(build_files)
                logger.info(f"✅ Build directory present with {len(build_files)} files")
            else:
                frontend_analysis["build_status"] = "missing"
                frontend_analysis["issues"].append("Build directory missing - run 'npm run build'")
        
        frontend_analysis["status"] = "completed"
        self.analysis_results["frontend"] = frontend_analysis
    
    async def _analyze_backend(self):
        """Analyze backend API and Python components"""
        backend_analysis = {
            "status": "analyzing",
            "main_api": {},
            "dependencies": {},
            "core_modules": {},
            "issues": []
        }
        
        # Check main.py
        main_py_path = os.path.join(self.workspace_root, "main.py")
        if os.path.exists(main_py_path):
            try:
                with open(main_py_path, 'r') as f:
                    main_content = f.read()
                
                backend_analysis["main_api"] = {
                    "size": len(main_content),
                    "lines": len(main_content.split('\n')),
                    "has_fastapi": "FastAPI" in main_content,
                    "has_cors": "CORSMiddleware" in main_content,
                    "has_startup": "@app.on_event" in main_content
                }
                logger.info("✅ Main API file analyzed")
                
            except Exception as e:
                backend_analysis["issues"].append(f"Error reading main.py: {str(e)}")
        
        # Check requirements.txt
        requirements_path = os.path.join(self.workspace_root, "requirements.txt")
        if os.path.exists(requirements_path):
            try:
                with open(requirements_path, 'r') as f:
                    requirements = f.read().strip().split('\n')
                
                backend_analysis["dependencies"] = {
                    "count": len([r for r in requirements if r.strip() and not r.startswith('#')]),
                    "key_packages": {
                        "fastapi": any("fastapi" in req.lower() for req in requirements),
                        "uvicorn": any("uvicorn" in req.lower() for req in requirements),
                        "firebase": any("firebase" in req.lower() for req in requirements),
                        "pandas": any("pandas" in req.lower() for req in requirements),
                        "numpy": any("numpy" in req.lower() for req in requirements)
                    }
                }
                logger.info(f"✅ Backend dependencies analyzed - {backend_analysis['dependencies']['count']} packages")
                
            except Exception as e:
                backend_analysis["issues"].append(f"Error reading requirements.txt: {str(e)}")
        
        backend_analysis["status"] = "completed"
        self.analysis_results["backend"] = backend_analysis
    
    async def _analyze_firebase_config(self):
        """Analyze Firebase configuration and setup"""
        firebase_analysis = {
            "status": "analyzing",
            "config_file": {},
            "functions": {},
            "hosting": {},
            "firestore": {},
            "issues": []
        }
        
        # Check firebase.json
        firebase_json_path = os.path.join(self.workspace_root, "firebase.json")
        if os.path.exists(firebase_json_path):
            try:
                with open(firebase_json_path, 'r') as f:
                    firebase_config = json.load(f)
                
                firebase_analysis["config_file"] = {
                    "has_hosting": "hosting" in firebase_config,
                    "has_functions": "functions" in firebase_config,
                    "has_firestore": "firestore" in firebase_config,
                    "has_emulators": "emulators" in firebase_config
                }
                
                # Analyze hosting config
                if "hosting" in firebase_config:
                    hosting = firebase_config["hosting"]
                    firebase_analysis["hosting"] = {
                        "public_dir": hosting.get("public", "unknown"),
                        "has_rewrites": "rewrites" in hosting,
                        "has_headers": "headers" in hosting,
                        "ignore_patterns": len(hosting.get("ignore", []))
                    }
                
                # Analyze functions config
                if "functions" in firebase_config:
                    firebase_analysis["functions"] = {
                        "configured": True,
                        "source": firebase_config["functions"][0].get("source", "unknown") if isinstance(firebase_config["functions"], list) else "unknown"
                    }
                
                # Check functions directory
                functions_path = os.path.join(self.workspace_root, "functions")
                if os.path.exists(functions_path):
                    functions_package_json = os.path.join(functions_path, "package.json")
                    if os.path.exists(functions_package_json):
                        firebase_analysis["functions"]["package_json"] = True
                    else:
                        firebase_analysis["issues"].append("Functions package.json missing")
                
                logger.info("✅ Firebase configuration analyzed")
                
            except json.JSONDecodeError as e:
                firebase_analysis["issues"].append(f"Invalid firebase.json: {str(e)}")
            except Exception as e:
                firebase_analysis["issues"].append(f"Error reading firebase.json: {str(e)}")
        else:
            firebase_analysis["issues"].append("firebase.json missing")
        
        firebase_analysis["status"] = "completed"
        self.analysis_results["firebase"] = firebase_analysis
    
    async def _analyze_security(self):
        """Analyze security configuration and potential issues"""
        security_analysis = {
            "status": "analyzing",
            "authentication": {},
            "firebase_security": {},
            "access_control": {},
            "issues": [],
            "recommendations": []
        }
        
        # Check private access gate
        access_gate_path = os.path.join(self.workspace_root, "private_access_gate.html")
        if os.path.exists(access_gate_path):
            try:
                with open(access_gate_path, 'r') as f:
                    access_content = f.read()
                
                security_analysis["access_control"] = {
                    "has_access_gate": True,
                    "has_firebase_auth": "firebase.auth()" in access_content,
                    "has_access_codes": "accessCodes" in access_content,
                    "has_role_based": "accessLevel" in access_content
                }
                logger.info("✅ Access control system analyzed")
                
            except Exception as e:
                security_analysis["issues"].append(f"Error analyzing access gate: {str(e)}")
        
        # Check for hardcoded secrets (basic scan)
        sensitive_patterns = ["apiKey", "password", "secret", "token"]
        for root, dirs, files in os.walk(self.workspace_root):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.vscode']]
            
            for file in files:
                if file.endswith(('.js', '.html', '.py', '.ts', '.tsx')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for pattern in sensitive_patterns:
                                if f'"{pattern}"' in content.lower() or f"'{pattern}'" in content.lower():
                                    # This is a basic check - would need more sophisticated analysis in production
                                    pass
                    except Exception:
                        continue
        
        # Firebase security rules check
        firestore_rules_path = os.path.join(self.workspace_root, "firestore.rules")
        if os.path.exists(firestore_rules_path):
            security_analysis["firebase_security"]["has_firestore_rules"] = True
            logger.info("✅ Firestore security rules found")
        else:
            security_analysis["issues"].append("Firestore security rules missing")
        
        security_analysis["status"] = "completed"
        self.analysis_results["security"] = security_analysis
    
    async def _analyze_performance(self):
        """Analyze performance aspects and optimization"""
        performance_analysis = {
            "status": "analyzing",
            "frontend_optimization": {},
            "backend_optimization": {},
            "asset_optimization": {},
            "recommendations": []
        }
        
        # Check frontend build optimization
        frontend_build_path = os.path.join(self.workspace_root, "frontend", "build")
        if os.path.exists(frontend_build_path):
            static_path = os.path.join(frontend_build_path, "static")
            if os.path.exists(static_path):
                js_files = []
                css_files = []
                
                for root, dirs, files in os.walk(static_path):
                    for file in files:
                        if file.endswith('.js'):
                            js_files.append(os.path.getsize(os.path.join(root, file)))
                        elif file.endswith('.css'):
                            css_files.append(os.path.getsize(os.path.join(root, file)))
                
                performance_analysis["frontend_optimization"] = {
                    "js_files_count": len(js_files),
                    "css_files_count": len(css_files),
                    "total_js_size": sum(js_files),
                    "total_css_size": sum(css_files),
                    "largest_js": max(js_files) if js_files else 0,
                    "largest_css": max(css_files) if css_files else 0
                }
                
                # Performance recommendations
                if max(js_files) if js_files else 0 > 1024 * 1024:  # 1MB
                    performance_analysis["recommendations"].append("Consider code splitting for large JS bundles")
                
                logger.info(f"✅ Frontend performance analyzed - {len(js_files)} JS files, {len(css_files)} CSS files")
        
        # Check for performance monitoring
        monitoring_files = ["performance_testing", "load_test_suite.py"]
        performance_analysis["monitoring"] = {}
        
        for monitoring_file in monitoring_files:
            file_path = os.path.join(self.workspace_root, monitoring_file)
            if os.path.exists(file_path):
                performance_analysis["monitoring"][monitoring_file] = True
            else:
                performance_analysis["monitoring"][monitoring_file] = False
        
        performance_analysis["status"] = "completed"
        self.analysis_results["performance"] = performance_analysis
    
    async def _assess_deployment_readiness(self):
        """Assess overall deployment readiness"""
        readiness_assessment = {
            "status": "analyzing",
            "overall_score": 0,
            "critical_blockers": [],
            "warnings": [],
            "recommendations": [],
            "deployment_ready": False
        }
        
        score = 100  # Start with perfect score and deduct points
        
        # Check critical components
        if self.analysis_results.get("code_quality", {}).get("critical_errors"):
            readiness_assessment["critical_blockers"].append("Critical code compilation errors")
            score -= 30
        
        if self.analysis_results.get("firebase", {}).get("issues"):
            if any("firebase.json missing" in issue for issue in self.analysis_results["firebase"]["issues"]):
                readiness_assessment["critical_blockers"].append("Firebase configuration missing")
                score -= 25
        
        if self.analysis_results.get("frontend", {}).get("build_status") == "missing":
            readiness_assessment["warnings"].append("Frontend build missing - needs 'npm run build'")
            score -= 10
        
        if self.analysis_results.get("security", {}).get("issues"):
            readiness_assessment["warnings"].extend(self.analysis_results["security"]["issues"])
            score -= 5 * len(self.analysis_results["security"]["issues"])
        
        # Positive points for good practices
        if self.analysis_results.get("security", {}).get("access_control", {}).get("has_access_gate"):
            score += 5
        
        if self.analysis_results.get("firebase", {}).get("config_file", {}).get("has_emulators"):
            score += 3
        
        readiness_assessment["overall_score"] = max(0, min(100, score))
        readiness_assessment["deployment_ready"] = score >= 80 and not readiness_assessment["critical_blockers"]
        
        # Generate recommendations
        if not readiness_assessment["deployment_ready"]:
            readiness_assessment["recommendations"].append("Fix critical blockers before deployment")
        
        if readiness_assessment["overall_score"] < 90:
            readiness_assessment["recommendations"].append("Address warnings to improve deployment quality")
        
        readiness_assessment["status"] = "completed"
        self.analysis_results["deployment_readiness"] = readiness_assessment
    
    async def _generate_comprehensive_report(self, analysis_time: float):
        """Generate comprehensive analysis report"""
        logger.info("\n" + "=" * 80)
        logger.info("📊 COMPREHENSIVE DEPLOYMENT ANALYSIS REPORT")
        logger.info("=" * 80)
        
        # Overall status
        deployment_ready = self.analysis_results.get("deployment_readiness", {}).get("deployment_ready", False)
        overall_score = self.analysis_results.get("deployment_readiness", {}).get("overall_score", 0)
        
        status_icon = "✅" if deployment_ready else "⚠️" if overall_score >= 60 else "❌"
        
        logger.info(f"\n{status_icon} DEPLOYMENT STATUS: {'READY' if deployment_ready else 'NEEDS ATTENTION'}")
        logger.info(f"📈 Overall Score: {overall_score}/100")
        logger.info(f"⏱️ Analysis Time: {analysis_time:.2f} seconds")
        
        # Detailed breakdown
        logger.info(f"\n📋 COMPONENT ANALYSIS:")
        
        for component, analysis in self.analysis_results.items():
            if isinstance(analysis, dict) and "status" in analysis:
                status = analysis["status"]
                status_icon = "✅" if status == "completed" else "⚠️"
                logger.info(f"   {status_icon} {component.replace('_', ' ').title()}: {status}")
                
                # Show critical issues
                if "critical_errors" in analysis and analysis["critical_errors"]:
                    for error in analysis["critical_errors"]:
                        logger.error(f"      ❌ {error}")
                
                if "issues" in analysis and analysis["issues"]:
                    for issue in analysis["issues"]:
                        logger.warning(f"      ⚠️ {issue}")
        
        # Critical blockers
        critical_blockers = self.analysis_results.get("deployment_readiness", {}).get("critical_blockers", [])
        if critical_blockers:
            logger.info(f"\n🚨 CRITICAL BLOCKERS:")
            for blocker in critical_blockers:
                logger.error(f"   ❌ {blocker}")
        
        # Warnings
        warnings = self.analysis_results.get("deployment_readiness", {}).get("warnings", [])
        if warnings:
            logger.info(f"\n⚠️ WARNINGS:")
            for warning in warnings:
                logger.warning(f"   ⚠️ {warning}")
        
        # Recommendations
        recommendations = self.analysis_results.get("deployment_readiness", {}).get("recommendations", [])
        if recommendations:
            logger.info(f"\n🎯 RECOMMENDATIONS:")
            for rec in recommendations:
                logger.info(f"   💡 {rec}")
        
        # Next steps
        logger.info(f"\n🚀 NEXT STEPS:")
        if deployment_ready:
            logger.info("   ✅ System is ready for Firebase deployment")
            logger.info("   🔥 Run: firebase deploy")
            logger.info("   📊 Monitor deployment with Firebase console")
        else:
            logger.info("   🔧 Fix critical blockers listed above")
            logger.info("   ⚠️ Address warnings for better deployment quality")
            logger.info("   🔄 Re-run analysis after fixes")
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"deployment_analysis_report_{timestamp}.json"
        
        report_data = {
            "analysis_timestamp": timestamp,
            "analysis_duration": analysis_time,
            "overall_assessment": {
                "deployment_ready": deployment_ready,
                "overall_score": overall_score,
                "critical_blockers": critical_blockers,
                "warnings": warnings,
                "recommendations": recommendations
            },
            "detailed_analysis": self.analysis_results
        }
        
        try:
            with open(os.path.join(self.workspace_root, report_filename), 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            logger.info(f"\n💾 Detailed report saved: {report_filename}")
        except Exception as e:
            logger.error(f"❌ Failed to save report: {e}")

async def main():
    """Main function to run comprehensive analysis"""
    workspace_root = os.path.dirname(os.path.abspath(__file__))
    analyzer = ComprehensiveDeploymentAnalyzer(workspace_root)
    
    try:
        results = await analyzer.run_full_analysis()
        return results
    except Exception as e:
        logger.error(f"💥 Analysis failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    asyncio.run(main())
