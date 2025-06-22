"""
Project Analysis Agent for MASS Framework
Analyzes project structure, dependencies, and provides insights
"""

import os
import ast
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from core.agent_base import AgentBase
from core.llm_service import llm_service, AIMessage

logger = logging.getLogger(__name__)

class ProjectAnalysisAgent(AgentBase):
    """AI-powered project analysis agent"""
    
    def __init__(self):
        super().__init__(
            agent_id="ai_project_analyzer",
            specialization="project_analysis"
        )
        self.name = "AI Project Analysis Agent"
        self.description = "Analyzes project structure, dependencies, code quality, and provides architectural insights"
        self.capabilities = [
            "project_structure_analysis",
            "dependency_analysis", 
            "code_quality_assessment",
            "architectural_recommendations",
            "technology_stack_analysis",
            "security_vulnerability_scan",
            "performance_analysis",
            "maintainability_assessment"
        ]
    
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input data for project analysis tasks"""
        try:
            analysis_type = input_data.get("type", "general_analysis")
            project_path = input_data.get("project_path", ".")
            
            if analysis_type == "project_structure":
                return await self._analyze_project_structure_input(input_data)
            elif analysis_type == "dependencies":
                return await self._analyze_dependencies_input(input_data)
            elif analysis_type == "code_quality":
                return await self._analyze_code_quality_input(input_data)
            else:
                return await self._general_project_analysis(input_data)
                
        except Exception as e:
            logger.error(f"Error analyzing input: {str(e)}")
            return {
                "success": False,
                "error": f"Analysis failed: {str(e)}",
                "analysis_type": input_data.get("type", "unknown")
            }
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents for complex project analysis tasks"""
        try:
            coordination_results = {}
            task_type = task_context.get("type", "")
            
            # Coordinate with code generator for architectural recommendations
            if "code_generator" in other_agents and task_type in ["architecture_recommendation", "refactoring_analysis"]:
                coordination_results["code_generator"] = await self._coordinate_with_code_generator(task_context)
            
            # Coordinate with testing agent for quality assessments
            if "testing_agent" in other_agents and task_type in ["code_quality", "test_coverage_analysis"]:
                coordination_results["testing_agent"] = await self._coordinate_with_testing_agent(task_context)
            
            # Coordinate with documentation agent for project documentation analysis
            if "documentation_agent" in other_agents and task_type in ["documentation_analysis", "project_overview"]:
                coordination_results["documentation_agent"] = await self._coordinate_with_documentation_agent(task_context)
            
            return {
                "success": True,
                "coordination_results": coordination_results,
                "coordinated_agents": other_agents,
                "task_context": task_context
            }
            
        except Exception as e:
            logger.error(f"Error coordinating with agents: {str(e)}")
            return {
                "success": False,
                "error": f"Coordination failed: {str(e)}",
                "attempted_agents": other_agents
            }
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process project analysis tasks"""
        try:
            task_type = task.get("type", "")
            
            if task_type == "analyze_project_structure":
                return await self._analyze_project_structure(task)
            elif task_type == "analyze_dependencies":
                return await self._analyze_dependencies(task)
            elif task_type == "assess_code_quality":
                return await self._assess_code_quality(task)
            elif task_type == "recommend_architecture":
                return await self._recommend_architecture(task)
            elif task_type == "analyze_tech_stack":
                return await self._analyze_tech_stack(task)
            elif task_type == "scan_security":
                return await self._scan_security_vulnerabilities(task)
            elif task_type == "analyze_performance":
                return await self._analyze_performance_issues(task)
            elif task_type == "assess_maintainability":
                return await self._assess_maintainability(task)
            elif task_type == "full_project_analysis":
                return await self._full_project_analysis(task)
            else:
                return await self._default_analysis(task)
                
        except Exception as e:
            logger.error(f"Project analysis task failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Project analysis failed"
            }
    
    async def _analyze_project_structure(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze project structure and organization"""
        project_path = task.get("project_path", "")
        
        if not project_path or not os.path.exists(project_path):
            return {
                "success": False,
                "error": "Invalid project path provided"
            }
        
        try:
            # Scan project structure
            structure = self._scan_directory_structure(project_path)
            file_stats = self._analyze_file_statistics(project_path)
            
            # AI analysis of structure
            system_prompt = """You are a senior software architect analyzing project structure. 
            
            Provide insights on:
            1. Project organization and structure quality
            2. Adherence to best practices and conventions
            3. Potential structural improvements
            4. Missing directories or files
            5. Architectural patterns identified
            6. Scalability considerations
            
            Be specific and provide actionable recommendations."""
            
            user_prompt = f"""Analyze this project structure:

Directory Structure:
{json.dumps(structure, indent=2)}

File Statistics:
{json.dumps(file_stats, indent=2)}

Provide a comprehensive analysis with specific recommendations for improvement."""

            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "success": True,
                "analysis_type": "project_structure",
                "structure": structure,
                "file_stats": file_stats,
                "ai_insights": response.content,
                "recommendations": self._extract_recommendations(response.content)
            }
            
        except Exception as e:
            logger.error(f"Project structure analysis failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _analyze_dependencies(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze project dependencies and package management"""
        project_path = task.get("project_path", "")
        
        try:
            dependencies = self._extract_dependencies(project_path)
            dependency_analysis = await self._ai_analyze_dependencies(dependencies)
            
            return {
                "success": True,
                "analysis_type": "dependencies",
                "dependencies": dependencies,
                "analysis": dependency_analysis,
                "security_alerts": self._check_known_vulnerabilities(dependencies),
                "update_recommendations": self._suggest_dependency_updates(dependencies)
            }
            
        except Exception as e:
            logger.error(f"Dependency analysis failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _assess_code_quality(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall code quality of the project"""
        project_path = task.get("project_path", "")
        
        try:
            # Scan code files
            code_metrics = self._calculate_code_metrics(project_path)
            quality_issues = self._identify_quality_issues(project_path)
            
            # AI assessment
            system_prompt = """You are a code quality expert. Analyze the provided code metrics and identify areas for improvement.

            Focus on:
            1. Code complexity and maintainability
            2. Adherence to coding standards
            3. Potential bugs and issues
            4. Performance concerns
            5. Security vulnerabilities
            6. Test coverage and quality
            
            Provide specific, actionable recommendations."""
            
            user_prompt = f"""Assess the code quality based on these metrics:

Code Metrics:
{json.dumps(code_metrics, indent=2)}

Quality Issues Found:
{json.dumps(quality_issues, indent=2)}

Provide a comprehensive code quality assessment with prioritized recommendations."""

            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "success": True,
                "analysis_type": "code_quality",
                "metrics": code_metrics,
                "issues": quality_issues,
                "ai_assessment": response.content,
                "quality_score": self._calculate_quality_score(code_metrics, quality_issues),
                "recommendations": self._extract_recommendations(response.content)
            }
            
        except Exception as e:
            logger.error(f"Code quality assessment failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _full_project_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive project analysis combining all aspects"""
        project_path = task.get("project_path", "")
        
        try:
            # Run all analyses
            structure_analysis = await self._analyze_project_structure(task)
            dependency_analysis = await self._analyze_dependencies(task)
            quality_analysis = await self._assess_code_quality(task)
            tech_analysis = await self._analyze_tech_stack(task)
            
            # Combine results
            comprehensive_analysis = {
                "success": True,
                "analysis_type": "comprehensive",
                "project_path": project_path,
                "analyses": {
                    "structure": structure_analysis,
                    "dependencies": dependency_analysis,
                    "code_quality": quality_analysis,
                    "technology_stack": tech_analysis
                },
                "overall_health_score": self._calculate_overall_health_score([
                    structure_analysis, dependency_analysis, quality_analysis, tech_analysis
                ])
            }
            
            # Generate executive summary
            system_prompt = """You are a technical project manager creating an executive summary of a comprehensive project analysis.
            
            Create a concise, high-level summary that includes:
            1. Overall project health and status
            2. Key strengths and achievements
            3. Critical issues requiring immediate attention
            4. Strategic recommendations for improvement
            5. Risk assessment and mitigation strategies
            6. Next steps and priorities
            
            Keep it business-focused and actionable."""
            
            user_prompt = f"""Create an executive summary for this comprehensive project analysis:

{json.dumps(comprehensive_analysis, indent=2)}

Provide a strategic overview suitable for technical leadership."""

            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            comprehensive_analysis["executive_summary"] = response.content
            
            return comprehensive_analysis
            
        except Exception as e:
            logger.error(f"Comprehensive project analysis failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _scan_directory_structure(self, project_path: str) -> Dict[str, Any]:
        """Scan and analyze directory structure"""
        structure = {}
        
        try:
            for root, dirs, files in os.walk(project_path):
                # Skip hidden directories and common ignore patterns
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
                
                rel_path = os.path.relpath(root, project_path)
                if rel_path == '.':
                    rel_path = 'root'
                
                structure[rel_path] = {
                    "directories": dirs,
                    "files": files,
                    "file_count": len(files),
                    "file_types": self._categorize_file_types(files)
                }
        
        except Exception as e:
            logger.error(f"Directory scanning failed: {str(e)}")
        
        return structure
    
    def _analyze_file_statistics(self, project_path: str) -> Dict[str, Any]:
        """Analyze file statistics and metrics"""
        stats = {
            "total_files": 0,
            "total_lines": 0,
            "file_types": {},
            "languages": {},
            "largest_files": [],
            "avg_file_size": 0
        }
        
        try:
            file_sizes = []
            
            for root, dirs, files in os.walk(project_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
                
                for file in files:
                    if file.startswith('.'):
                        continue
                    
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        file_sizes.append(file_size)
                        
                        # File extension analysis
                        ext = os.path.splitext(file)[1].lower()
                        stats["file_types"][ext] = stats["file_types"].get(ext, 0) + 1
                        
                        # Count lines for text files
                        if ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.html', '.css', '.sql']:
                            try:
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    lines = len(f.readlines())
                                    stats["total_lines"] += lines
                                    
                                    # Track largest files
                                    stats["largest_files"].append({
                                        "file": os.path.relpath(file_path, project_path),
                                        "lines": lines,
                                        "size": file_size
                                    })
                            except:
                                pass
                        
                        stats["total_files"] += 1
                    except:
                        continue
            
            # Sort largest files
            stats["largest_files"].sort(key=lambda x: x["lines"], reverse=True)
            stats["largest_files"] = stats["largest_files"][:10]  # Top 10
            
            # Calculate averages
            if file_sizes:
                stats["avg_file_size"] = sum(file_sizes) / len(file_sizes)
            
        except Exception as e:
            logger.error(f"File statistics analysis failed: {str(e)}")
        
        return stats
    
    def _categorize_file_types(self, files: List[str]) -> Dict[str, int]:
        """Categorize files by type"""
        categories = {
            "source_code": 0,
            "configuration": 0,
            "documentation": 0,
            "data": 0,
            "assets": 0,
            "other": 0
        }
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            
            if ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go']:
                categories["source_code"] += 1
            elif ext in ['.json', '.yaml', '.yml', '.xml', '.ini', '.cfg', '.conf', '.toml']:
                categories["configuration"] += 1
            elif ext in ['.md', '.txt', '.rst', '.doc', '.docx', '.pdf']:
                categories["documentation"] += 1
            elif ext in ['.csv', '.sql', '.db', '.sqlite']:
                categories["data"] += 1
            elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico']:
                categories["assets"] += 1
            else:
                categories["other"] += 1
        
        return categories
    
    def _extract_dependencies(self, project_path: str) -> Dict[str, Any]:
        """Extract dependencies from various package files"""
        dependencies = {
            "python": [],
            "javascript": [],
            "java": [],
            "docker": [],
            "system": []
        }
        
        try:
            # Python dependencies
            requirements_files = ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"]
            for req_file in requirements_files:
                req_path = os.path.join(project_path, req_file)
                if os.path.exists(req_path):
                    dependencies["python"].extend(self._parse_python_requirements(req_path))
            
            # JavaScript dependencies
            package_json = os.path.join(project_path, "package.json")
            if os.path.exists(package_json):
                dependencies["javascript"] = self._parse_package_json(package_json)
            
            # Java dependencies
            pom_xml = os.path.join(project_path, "pom.xml")
            if os.path.exists(pom_xml):
                dependencies["java"] = self._parse_pom_xml(pom_xml)
            
            # Docker dependencies
            dockerfile = os.path.join(project_path, "Dockerfile")
            if os.path.exists(dockerfile):
                dependencies["docker"] = self._parse_dockerfile(dockerfile)
        
        except Exception as e:
            logger.error(f"Dependency extraction failed: {str(e)}")
        
        return dependencies
    
    def _parse_python_requirements(self, file_path: str) -> List[Dict[str, str]]:
        """Parse Python requirements file"""
        deps = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Basic parsing - can be enhanced
                        parts = line.split('==')
                        if len(parts) == 2:
                            deps.append({"name": parts[0], "version": parts[1]})
                        else:
                            deps.append({"name": line, "version": "unknown"})
        except Exception as e:
            logger.error(f"Failed to parse requirements: {str(e)}")
        
        return deps
    
    def _parse_package_json(self, file_path: str) -> List[Dict[str, str]]:
        """Parse package.json dependencies"""
        deps = []
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                for dep_type in ["dependencies", "devDependencies"]:
                    if dep_type in data:
                        for name, version in data[dep_type].items():
                            deps.append({
                                "name": name,
                                "version": version,
                                "type": dep_type
                            })
        except Exception as e:
            logger.error(f"Failed to parse package.json: {str(e)}")
        
        return deps
    
    def _parse_pom_xml(self, file_path: str) -> List[Dict[str, str]]:
        """Parse Maven pom.xml dependencies"""
        # Simplified XML parsing - would need proper XML parser for production
        deps = []
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Basic regex extraction - enhance for production
                deps.append({"name": "maven_project", "version": "extracted_from_pom"})
        except Exception as e:
            logger.error(f"Failed to parse pom.xml: {str(e)}")
        
        return deps
    
    def _parse_dockerfile(self, file_path: str) -> List[Dict[str, str]]:
        """Parse Dockerfile for system dependencies"""
        deps = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('FROM'):
                        base_image = line.split()[1]
                        deps.append({"name": "base_image", "version": base_image})
        except Exception as e:
            logger.error(f"Failed to parse Dockerfile: {str(e)}")
        
        return deps
    
    async def _ai_analyze_dependencies(self, dependencies: Dict[str, Any]) -> str:
        """AI analysis of project dependencies"""
        system_prompt = """You are a dependency security and architecture expert. Analyze the project dependencies and provide insights on:

        1. Security vulnerabilities and outdated packages
        2. Dependency conflicts and compatibility issues
        3. Licensing concerns
        4. Performance impact of dependencies
        5. Recommendations for optimization
        6. Alternative packages to consider
        
        Be specific about security risks and provide actionable recommendations."""
        
        user_prompt = f"""Analyze these project dependencies:

        {json.dumps(dependencies, indent=2)}
        
        Provide a comprehensive dependency analysis with security and optimization recommendations."""
        
        try:
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            return response.content
        except Exception as e:
            logger.error(f"AI dependency analysis failed: {str(e)}")
            return f"Dependency analysis failed: {str(e)}"
    
    def _calculate_code_metrics(self, project_path: str) -> Dict[str, Any]:
        """Calculate basic code metrics"""
        metrics = {
            "total_functions": 0,
            "total_classes": 0,
            "avg_function_length": 0,
            "max_function_length": 0,
            "complex_functions": [],
            "code_duplication": 0
        }
        
        function_lengths = []
        
        try:
            for root, dirs, files in os.walk(project_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
                
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        file_metrics = self._analyze_python_file(file_path)
                        
                        metrics["total_functions"] += file_metrics.get("functions", 0)
                        metrics["total_classes"] += file_metrics.get("classes", 0)
                        function_lengths.extend(file_metrics.get("function_lengths", []))
            
            if function_lengths:
                metrics["avg_function_length"] = sum(function_lengths) / len(function_lengths)
                metrics["max_function_length"] = max(function_lengths)
                metrics["complex_functions"] = len([l for l in function_lengths if l > 50])
        
        except Exception as e:
            logger.error(f"Code metrics calculation failed: {str(e)}")
        
        return metrics
    
    def _analyze_python_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single Python file"""
        metrics = {
            "functions": 0,
            "classes": 0,
            "function_lengths": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        metrics["functions"] += 1
                        # Calculate function length
                        func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 10
                        metrics["function_lengths"].append(func_lines)
                    elif isinstance(node, ast.ClassDef):
                        metrics["classes"] += 1
        
        except Exception as e:
            logger.error(f"Python file analysis failed for {file_path}: {str(e)}")
        
        return metrics
    
    def _identify_quality_issues(self, project_path: str) -> List[Dict[str, Any]]:
        """Identify code quality issues"""
        issues = []
        
        # This is a simplified implementation
        # In production, integrate with tools like pylint, flake8, sonarqube
        
        try:
            for root, dirs, files in os.walk(project_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
                
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        file_issues = self._check_python_file_issues(file_path)
                        issues.extend(file_issues)
        
        except Exception as e:
            logger.error(f"Quality issue identification failed: {str(e)}")
        
        return issues
    
    def _check_python_file_issues(self, file_path: str) -> List[Dict[str, Any]]:
        """Check for basic Python code issues"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
                for i, line in enumerate(lines):
                    # Basic checks
                    if len(line.strip()) > 120:
                        issues.append({
                            "file": file_path,
                            "line": i + 1,
                            "type": "line_too_long",
                            "severity": "low",
                            "message": "Line exceeds 120 characters"
                        })
                    
                    if line.strip().startswith('print(') and not line.strip().startswith('# '):
                        issues.append({
                            "file": file_path,
                            "line": i + 1,
                            "type": "debug_statement",
                            "severity": "medium",
                            "message": "Potential debug print statement"
                        })
        
        except Exception as e:
            logger.error(f"Python file issue checking failed for {file_path}: {str(e)}")
        
        return issues
    
    def _calculate_quality_score(self, metrics: Dict[str, Any], issues: List[Dict[str, Any]]) -> int:
        """Calculate overall code quality score (0-100)"""
        score = 100
        
        # Deduct points for issues
        high_severity_issues = len([i for i in issues if i.get("severity") == "high"])
        medium_severity_issues = len([i for i in issues if i.get("severity") == "medium"])
        low_severity_issues = len([i for i in issues if i.get("severity") == "low"])
        
        score -= high_severity_issues * 10
        score -= medium_severity_issues * 5
        score -= low_severity_issues * 2
        
        # Deduct points for complex functions
        complex_functions = metrics.get("complex_functions", 0)
        score -= complex_functions * 3
        
        return max(0, min(100, score))
    
    def _calculate_overall_health_score(self, analyses: List[Dict[str, Any]]) -> int:
        """Calculate overall project health score"""
        scores = []
        
        for analysis in analyses:
            if analysis.get("success") and "quality_score" in analysis:
                scores.append(analysis["quality_score"])
            elif analysis.get("success"):
                scores.append(75)  # Default score for successful analysis
            else:
                scores.append(50)  # Lower score for failed analysis
        
        return int(sum(scores) / len(scores)) if scores else 50
    
    def _extract_recommendations(self, ai_content: str) -> List[str]:
        """Extract actionable recommendations from AI analysis"""
        # Simple extraction - can be enhanced with NLP
        recommendations = []
        
        lines = ai_content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('- ') or line.startswith('• ') or 'recommend' in line.lower():
                recommendations.append(line)
        
        return recommendations[:10]  # Top 10 recommendations
    
    def _check_known_vulnerabilities(self, dependencies: Dict[str, Any]) -> List[Dict[str, str]]:
        """Check for known vulnerabilities (placeholder implementation)"""
        # In production, integrate with vulnerability databases
        return []
    
    def _suggest_dependency_updates(self, dependencies: Dict[str, Any]) -> List[Dict[str, str]]:
        """Suggest dependency updates (placeholder implementation)"""
        # In production, check latest versions and compatibility
        return []
    
    async def _analyze_tech_stack(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technology stack and architecture"""
        project_path = task.get("project_path", "")
        
        try:
            # Identify technologies used
            tech_stack = self._identify_technologies(project_path)
            
            system_prompt = """You are a technology stack analyst. Analyze the identified technologies and provide insights on:

            1. Technology choices and their appropriateness
            2. Architecture patterns and design decisions
            3. Scalability and performance implications
            4. Security considerations
            5. Maintenance and long-term viability
            6. Integration and compatibility issues
            7. Recommendations for improvements or migrations
            
            Provide strategic technical guidance."""
            
            user_prompt = f"""Analyze this technology stack:

            {json.dumps(tech_stack, indent=2)}
            
            Provide comprehensive technology stack analysis with strategic recommendations."""
            
            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            return {
                "success": True,
                "analysis_type": "technology_stack",
                "tech_stack": tech_stack,
                "ai_analysis": response.content,
                "recommendations": self._extract_recommendations(response.content)
            }
            
        except Exception as e:
            logger.error(f"Tech stack analysis failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _identify_technologies(self, project_path: str) -> Dict[str, Any]:
        """Identify technologies used in the project"""
        technologies = {
            "languages": [],
            "frameworks": [],
            "databases": [],
            "tools": [],
            "platforms": []
        }
        
        try:
            # Check for specific files that indicate technologies
            file_indicators = {
                "package.json": ["Node.js", "JavaScript"],
                "requirements.txt": ["Python"],
                "pom.xml": ["Java", "Maven"],
                "build.gradle": ["Java", "Gradle"],
                "Dockerfile": ["Docker"],
                "docker-compose.yml": ["Docker Compose"],
                "Makefile": ["Make"],
                "CMakeLists.txt": ["CMake", "C++"]
            }
            
            for indicator_file, techs in file_indicators.items():
                if os.path.exists(os.path.join(project_path, indicator_file)):
                    technologies["tools"].extend(techs)
            
            # Check file extensions for languages
            for root, dirs, files in os.walk(project_path):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
                
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    
                    if ext == '.py' and 'Python' not in technologies["languages"]:
                        technologies["languages"].append('Python')
                    elif ext in ['.js', '.jsx'] and 'JavaScript' not in technologies["languages"]:
                        technologies["languages"].append('JavaScript')
                    elif ext in ['.ts', '.tsx'] and 'TypeScript' not in technologies["languages"]:
                        technologies["languages"].append('TypeScript')
                    elif ext == '.java' and 'Java' not in technologies["languages"]:
                        technologies["languages"].append('Java')
                    elif ext in ['.cpp', '.c'] and 'C++' not in technologies["languages"]:
                        technologies["languages"].append('C++')
        
        except Exception as e:
            logger.error(f"Technology identification failed: {str(e)}")
        
        return technologies
    
    async def _scan_security_vulnerabilities(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Placeholder for security vulnerability scanning"""
        return {
            "success": True,
            "analysis_type": "security_scan",
            "vulnerabilities": [],
            "recommendations": ["Implement proper security scanning tools"]
        }
    
    async def _analyze_performance_issues(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Placeholder for performance analysis"""
        return {
            "success": True,
            "analysis_type": "performance_analysis",
            "issues": [],
            "recommendations": ["Implement performance profiling tools"]
        }
    
    # Helper methods for abstract method implementations
    
    async def _analyze_project_structure_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze project structure from input data"""
        project_path = input_data.get("project_path", ".")
        try:
            structure = self._scan_directory_structure(project_path)
            return {
                "success": True,
                "analysis_type": "project_structure",
                "structure": structure,
                "summary": f"Found {len(structure.get('files', []))} files in project"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Structure analysis failed: {str(e)}"
            }
    
    async def _analyze_dependencies_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze dependencies from input data"""
        project_path = input_data.get("project_path", ".")
        try:
            deps = self._scan_dependencies(project_path)
            return {
                "success": True,
                "analysis_type": "dependencies",
                "dependencies": deps,
                "summary": f"Found {len(deps)} dependencies"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Dependency analysis failed: {str(e)}"
            }
    
    async def _analyze_code_quality_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code quality from input data"""
        project_path = input_data.get("project_path", ".")
        try:
            quality_metrics = await self._calculate_code_quality_metrics(project_path)
            return {
                "success": True,
                "analysis_type": "code_quality",
                "metrics": quality_metrics,
                "summary": f"Code quality score: {quality_metrics.get('overall_score', 'N/A')}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Code quality analysis failed: {str(e)}"
            }
    
    async def _general_project_analysis(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform general project analysis"""
        project_path = input_data.get("project_path", ".")
        try:
            analysis_results = {
                "structure": self._scan_directory_structure(project_path),
                "dependencies": self._scan_dependencies(project_path),
                "quality_metrics": await self._calculate_code_quality_metrics(project_path)
            }
            return {
                "success": True,
                "analysis_type": "general_analysis",
                "results": analysis_results,
                "summary": "Comprehensive project analysis completed"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"General analysis failed: {str(e)}"
            }
    
    async def _coordinate_with_code_generator(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with code generator agent"""
        return {
            "coordination_type": "code_generator",
            "task_context": task_context,
            "recommendations": ["Consider architectural patterns", "Implement design patterns"],
            "status": "coordinated"
        }
    
    async def _coordinate_with_testing_agent(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with testing agent"""
        return {
            "coordination_type": "testing_agent",
            "task_context": task_context,
            "recommendations": ["Increase test coverage", "Add integration tests"],
            "status": "coordinated"
        }
    
    async def _coordinate_with_documentation_agent(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with documentation agent"""
        return {
            "coordination_type": "documentation_agent",
            "task_context": task_context,
            "recommendations": ["Update project documentation", "Add API documentation"],
            "status": "coordinated"
        }
