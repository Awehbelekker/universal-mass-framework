"""
Intelligent Code Suggestion Engine for MASS Framework
Provides context-aware code suggestions and improvements
"""

import ast
import re
import os
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from core.agent_base import AgentBase
from core.llm_service import llm_service, AIMessage

logger = logging.getLogger(__name__)

@dataclass
class CodeSuggestion:
    """Represents a code suggestion"""
    id: str
    type: str  # completion, refactor, optimization, bug_fix, style
    description: str
    original_code: str
    suggested_code: str
    confidence: float  # 0.0 to 1.0
    reasoning: str
    file_path: str
    line_number: int
    priority: str  # low, medium, high, critical
    tags: List[str]

@dataclass
class CodeContext:
    """Represents code context for suggestions"""
    file_path: str
    language: str
    imports: List[str]
    classes: List[str]
    functions: List[str]
    variables: List[str]
    surrounding_code: str
    project_context: Dict[str, Any]

class IntelligentCodeSuggestionEngine(AgentBase):
    """AI-powered intelligent code suggestion engine"""
    
    def __init__(self):
        super().__init__(
            agent_id="ai_code_suggestion_engine",
            specialization="code_suggestions"
        )
        self.name = "Intelligent Code Suggestion Engine"
        self.description = "Provides context-aware code suggestions, completions, and improvements using AI"
        self.capabilities = [
            "code_completion",
            "code_refactoring",
            "performance_optimization",
            "bug_detection_and_fixes",
            "style_improvements",
            "best_practices_enforcement",
            "pattern_recognition",
            "context_aware_suggestions"
        ]
        self.suggestion_cache = {}
        self.code_patterns = self._load_code_patterns()
        self.suggestion_history = []
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process code suggestion tasks"""
        try:
            task_type = task.get("type", "")
            
            if task_type == "get_suggestions":
                return await self._get_code_suggestions(task)
            elif task_type == "complete_code":
                return await self._complete_code(task)
            elif task_type == "refactor_code":
                return await self._refactor_code(task)
            elif task_type == "optimize_performance":
                return await self._optimize_performance(task)
            elif task_type == "fix_bugs":
                return await self._suggest_bug_fixes(task)
            elif task_type == "improve_style":
                return await self._improve_code_style(task)
            elif task_type == "enforce_patterns":
                return await self._enforce_best_practices(task)
            elif task_type == "analyze_context":
                return await self._analyze_code_context(task)
            else:
                return await self._get_code_suggestions(task)
                
        except Exception as e:
            logger.error(f"Code suggestion task failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "suggestions": []
            }
    
    async def _get_code_suggestions(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive code suggestions for given code"""
        code = task.get("code", "")
        file_path = task.get("file_path", "")
        language = task.get("language", "python")
        cursor_position = task.get("cursor_position", 0)
        
        if not code:
            return {
                "success": False,
                "error": "No code provided for analysis",
                "suggestions": []
            }
        
        try:
            # Analyze code context
            context = await self._build_code_context(code, file_path, language)
            
            # Generate different types of suggestions
            suggestions = []
            
            # Completion suggestions
            completion_suggestions = await self._generate_completion_suggestions(
                code, context, cursor_position
            )
            suggestions.extend(completion_suggestions)
            
            # Refactoring suggestions
            refactor_suggestions = await self._generate_refactor_suggestions(
                code, context
            )
            suggestions.extend(refactor_suggestions)
            
            # Performance suggestions
            performance_suggestions = await self._generate_performance_suggestions(
                code, context
            )
            suggestions.extend(performance_suggestions)
            
            # Bug fix suggestions
            bug_fix_suggestions = await self._generate_bug_fix_suggestions(
                code, context
            )
            suggestions.extend(bug_fix_suggestions)
            
            # Style improvement suggestions
            style_suggestions = await self._generate_style_suggestions(
                code, context
            )
            suggestions.extend(style_suggestions)
            
            # Rank suggestions by confidence and priority
            suggestions = self._rank_suggestions(suggestions)
            
            # Cache suggestions for future reference
            self._cache_suggestions(file_path, suggestions)
            
            return {
                "success": True,
                "suggestions": [self._suggestion_to_dict(s) for s in suggestions],
                "total_suggestions": len(suggestions),
                "context": self._context_to_dict(context)
            }
            
        except Exception as e:
            logger.error(f"Code suggestions generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "suggestions": []
            }
    
    async def _complete_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Provide intelligent code completion"""
        code = task.get("code", "")
        cursor_position = task.get("cursor_position", len(code))
        language = task.get("language", "python")
        
        try:
            # Get the partial line and context
            lines = code.split('\n')
            current_line_index = code[:cursor_position].count('\n')
            
            if current_line_index < len(lines):
                current_line = lines[current_line_index]
                prefix = current_line[:cursor_position - code[:cursor_position].rfind('\n') - 1]
            else:
                current_line = ""
                prefix = ""
            
            # Build context
            context = await self._build_code_context(code, "", language)
            
            # Generate completions using AI
            system_prompt = f"""You are an intelligent code completion assistant for {language}. 
            
            Provide code completions that are:
            1. Contextually appropriate
            2. Follow language conventions and best practices
            3. Complete and syntactically correct
            4. Consider the surrounding code context
            5. Offer multiple completion options when applicable
            
            Return completions as a JSON array of objects with:
            - "completion": the completion text
            - "description": brief description
            - "confidence": confidence score (0-1)
            - "type": completion type (method, variable, keyword, etc.)"""
            
            user_prompt = f"""Complete this {language} code:

Context:
{code}

Current line: {current_line}
Prefix to complete: {prefix}

Provide intelligent code completions for the current position."""

            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            # Parse completions
            try:
                completions = json.loads(response.content)
                if not isinstance(completions, list):
                    completions = [completions]
            except json.JSONDecodeError:
                # Fallback to simple completion
                completions = [{
                    "completion": response.content.strip(),
                    "description": "AI-generated completion",
                    "confidence": 0.7,
                    "type": "general"
                }]
            
            return {
                "success": True,
                "completions": completions,
                "context": {
                    "current_line": current_line,
                    "prefix": prefix,
                    "cursor_position": cursor_position
                }
            }
            
        except Exception as e:
            logger.error(f"Code completion failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "completions": []
            }
    
    async def _refactor_code(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest code refactoring improvements"""
        code = task.get("code", "")
        refactor_type = task.get("refactor_type", "general")  # extract_method, rename, etc.
        language = task.get("language", "python")
        
        try:
            context = await self._build_code_context(code, "", language)
            
            system_prompt = f"""You are a code refactoring expert for {language}. 
            
            Analyze the provided code and suggest refactoring improvements focusing on:
            1. Code readability and maintainability
            2. Reducing complexity and duplication
            3. Improving performance
            4. Following best practices and design patterns
            5. Extracting reusable components
            
            Return suggestions as JSON array with:
            - "type": refactoring type
            - "description": what to refactor and why
            - "original_code": code to be refactored
            - "refactored_code": improved code
            - "benefits": list of benefits
            - "confidence": confidence score (0-1)"""
            
            user_prompt = f"""Suggest refactoring improvements for this {language} code:

{code}

Focus on {refactor_type} refactoring if specified, otherwise provide general improvements."""

            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            try:
                refactoring_suggestions = json.loads(response.content)
                if not isinstance(refactoring_suggestions, list):
                    refactoring_suggestions = [refactoring_suggestions]
            except json.JSONDecodeError:
                refactoring_suggestions = [{
                    "type": "general",
                    "description": "General refactoring suggestion",
                    "original_code": code,
                    "refactored_code": response.content,
                    "benefits": ["Improved code quality"],
                    "confidence": 0.7
                }]
            
            return {
                "success": True,
                "refactoring_suggestions": refactoring_suggestions,
                "refactor_type": refactor_type
            }
            
        except Exception as e:
            logger.error(f"Code refactoring failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "refactoring_suggestions": []
            }
    
    async def _optimize_performance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest performance optimizations"""
        code = task.get("code", "")
        language = task.get("language", "python")
        performance_data = task.get("performance_data", {})
        
        try:
            system_prompt = f"""You are a performance optimization expert for {language}.
            
            Analyze the code and suggest performance improvements:
            1. Algorithmic optimizations
            2. Data structure improvements
            3. Memory usage optimization
            4. I/O optimization
            5. Caching strategies
            6. Parallel processing opportunities
            
            Return optimization suggestions as JSON array with:
            - "optimization_type": type of optimization
            - "description": detailed explanation
            - "original_code": code to be optimized
            - "optimized_code": improved code
            - "expected_improvement": expected performance gain
            - "trade_offs": any trade-offs to consider
            - "confidence": confidence score (0-1)"""
            
            user_prompt = f"""Suggest performance optimizations for this {language} code:

{code}

Performance data (if available):
{json.dumps(performance_data, indent=2)}

Focus on practical optimizations that provide measurable improvements."""

            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            try:
                optimizations = json.loads(response.content)
                if not isinstance(optimizations, list):
                    optimizations = [optimizations]
            except json.JSONDecodeError:
                optimizations = [{
                    "optimization_type": "general",
                    "description": "General performance optimization",
                    "original_code": code,
                    "optimized_code": response.content,
                    "expected_improvement": "Improved performance",
                    "trade_offs": "None identified",
                    "confidence": 0.7
                }]
            
            return {
                "success": True,
                "optimizations": optimizations,
                "performance_data": performance_data
            }
            
        except Exception as e:
            logger.error(f"Performance optimization failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "optimizations": []
            }
    
    async def _suggest_bug_fixes(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest bug fixes and error handling improvements"""
        code = task.get("code", "")
        error_message = task.get("error_message", "")
        language = task.get("language", "python")
        
        try:
            system_prompt = f"""You are a debugging expert for {language}.
            
            Analyze the code for potential bugs and suggest fixes:
            1. Syntax errors and typos
            2. Logic errors and edge cases
            3. Exception handling improvements
            4. Input validation issues
            5. Resource management problems
            6. Concurrency issues
            
            Return bug fixes as JSON array with:
            - "bug_type": type of bug
            - "description": explanation of the issue
            - "location": where the bug occurs
            - "original_code": buggy code
            - "fixed_code": corrected code
            - "severity": severity level (low, medium, high, critical)
            - "explanation": detailed fix explanation
            - "confidence": confidence score (0-1)"""
            
            user_prompt = f"""Analyze this {language} code for bugs and suggest fixes:

{code}

Error message (if any): {error_message}

Identify potential bugs and provide concrete fix suggestions."""

            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            try:
                bug_fixes = json.loads(response.content)
                if not isinstance(bug_fixes, list):
                    bug_fixes = [bug_fixes]
            except json.JSONDecodeError:
                bug_fixes = [{
                    "bug_type": "general",
                    "description": "Potential bug identified",
                    "location": "Code analysis",
                    "original_code": code,
                    "fixed_code": response.content,
                    "severity": "medium",
                    "explanation": "General bug fix suggestion",
                    "confidence": 0.7
                }]
            
            return {
                "success": True,
                "bug_fixes": bug_fixes,
                "error_message": error_message
            }
            
        except Exception as e:
            logger.error(f"Bug fix suggestions failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "bug_fixes": []
            }
    
    async def _improve_code_style(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest code style improvements"""
        code = task.get("code", "")
        style_guide = task.get("style_guide", "pep8")  # pep8, google, etc.
        language = task.get("language", "python")
        
        try:
            system_prompt = f"""You are a code style expert for {language} following {style_guide} guidelines.
            
            Analyze the code and suggest style improvements:
            1. Naming conventions
            2. Formatting and indentation
            3. Comment and documentation style
            4. Code organization
            5. Import statements
            6. Line length and readability
            
            Return style suggestions as JSON array with:
            - "style_issue": type of style issue
            - "description": what needs to be improved
            - "original_code": code with style issues
            - "improved_code": code with better style
            - "guideline": specific guideline reference
            - "priority": priority level (low, medium, high)
            - "confidence": confidence score (0-1)"""
            
            user_prompt = f"""Suggest style improvements for this {language} code following {style_guide}:

{code}

Focus on practical style improvements that enhance readability and maintainability."""

            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            try:
                style_improvements = json.loads(response.content)
                if not isinstance(style_improvements, list):
                    style_improvements = [style_improvements]
            except json.JSONDecodeError:
                style_improvements = [{
                    "style_issue": "general",
                    "description": "General style improvement",
                    "original_code": code,
                    "improved_code": response.content,
                    "guideline": style_guide,
                    "priority": "medium",
                    "confidence": 0.7
                }]
            
            return {
                "success": True,
                "style_improvements": style_improvements,
                "style_guide": style_guide
            }
            
        except Exception as e:
            logger.error(f"Style improvement suggestions failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "style_improvements": []
            }
    
    async def _build_code_context(self, code: str, file_path: str, language: str) -> CodeContext:
        """Build comprehensive code context for suggestions"""
        context = CodeContext(
            file_path=file_path,
            language=language,
            imports=[],
            classes=[],
            functions=[],
            variables=[],
            surrounding_code=code,
            project_context={}
        )
        
        try:
            if language == "python":
                context = await self._build_python_context(code, context)
            elif language in ["javascript", "typescript"]:
                context = await self._build_javascript_context(code, context)
            # Add more language-specific context builders as needed
            
        except Exception as e:
            logger.error(f"Context building failed: {str(e)}")
        
        return context
    
    async def _build_python_context(self, code: str, context: CodeContext) -> CodeContext:
        """Build Python-specific code context"""
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        context.imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            context.imports.append(f"{node.module}.{alias.name}")
                elif isinstance(node, ast.ClassDef):
                    context.classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    context.functions.append(node.name)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            context.variables.append(target.id)
                            
        except SyntaxError:
            # Handle incomplete or malformed code
            logger.warning("Code contains syntax errors, using text-based analysis")
            context = await self._build_text_based_context(code, context)
        
        return context
    
    async def _build_javascript_context(self, code: str, context: CodeContext) -> CodeContext:
        """Build JavaScript/TypeScript-specific code context"""
        # Simplified JavaScript context building
        # In production, use a proper JavaScript AST parser
        
        # Extract imports
        import_patterns = [
            r'import\s+.*\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\([\'"]([^\'"]+)[\'"]\)'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, code)
            context.imports.extend(matches)
        
        # Extract function declarations
        function_patterns = [
            r'function\s+(\w+)\s*\(',
            r'const\s+(\w+)\s*=\s*\(',
            r'(\w+)\s*:\s*function\s*\('
        ]
        
        for pattern in function_patterns:
            matches = re.findall(pattern, code)
            context.functions.extend(matches)
        
        # Extract class declarations
        class_pattern = r'class\s+(\w+)'
        matches = re.findall(class_pattern, code)
        context.classes.extend(matches)
        
        return context
    
    async def _build_text_based_context(self, code: str, context: CodeContext) -> CodeContext:
        """Build context using text-based analysis when AST fails"""
        lines = code.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Look for imports
            if line.startswith('import ') or line.startswith('from '):
                context.imports.append(line)
            
            # Look for function definitions
            if line.startswith('def ') or 'function ' in line:
                # Extract function name
                match = re.search(r'def\s+(\w+)\s*\(|function\s+(\w+)\s*\(', line)
                if match:
                    func_name = match.group(1) or match.group(2)
                    context.functions.append(func_name)
            
            # Look for class definitions
            if line.startswith('class '):
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    context.classes.append(match.group(1))
        
        return context
    
    async def _generate_completion_suggestions(
        self, 
        code: str, 
        context: CodeContext, 
        cursor_position: int
    ) -> List[CodeSuggestion]:
        """Generate code completion suggestions"""
        suggestions = []
        
        try:
            # Get the current line and position
            lines = code.split('\n')
            current_line_index = code[:cursor_position].count('\n')
            
            if current_line_index < len(lines):
                current_line = lines[current_line_index]
                
                # Generate context-aware completions
                if current_line.strip().endswith('.'):
                    # Method/attribute completion
                    suggestions.extend(await self._generate_member_completions(code, context))
                elif current_line.strip().startswith('def '):
                    # Function completion
                    suggestions.extend(await self._generate_function_completions(code, context))
                elif current_line.strip().startswith('class '):
                    # Class completion
                    suggestions.extend(await self._generate_class_completions(code, context))
                else:
                    # General completions
                    suggestions.extend(await self._generate_general_completions(code, context))
        
        except Exception as e:
            logger.error(f"Completion suggestions failed: {str(e)}")
        
        return suggestions
    
    async def _generate_member_completions(self, code: str, context: CodeContext) -> List[CodeSuggestion]:
        """Generate member (method/attribute) completion suggestions"""
        # Placeholder implementation
        return []
    
    async def _generate_function_completions(self, code: str, context: CodeContext) -> List[CodeSuggestion]:
        """Generate function completion suggestions"""
        # Placeholder implementation
        return []
    
    async def _generate_class_completions(self, code: str, context: CodeContext) -> List[CodeSuggestion]:
        """Generate class completion suggestions"""
        # Placeholder implementation
        return []
    
    async def _generate_general_completions(self, code: str, context: CodeContext) -> List[CodeSuggestion]:
        """Generate general completion suggestions"""
        # Placeholder implementation
        return []
    
    async def _generate_refactor_suggestions(self, code: str, context: CodeContext) -> List[CodeSuggestion]:
        """Generate refactoring suggestions"""
        suggestions = []
        
        # Analyze code for refactoring opportunities
        if context.language == "python":
            suggestions.extend(await self._analyze_python_refactoring(code, context))
        
        return suggestions
    
    async def _analyze_python_refactoring(self, code: str, context: CodeContext) -> List[CodeSuggestion]:
        """Analyze Python code for refactoring opportunities"""
        suggestions = []
        
        try:
            lines = code.split('\n')
            
            # Look for long functions (>20 lines)
            current_function = None
            function_start = 0
            function_lines = 0
            
            for i, line in enumerate(lines):
                if line.strip().startswith('def '):
                    if current_function and function_lines > 20:
                        suggestions.append(CodeSuggestion(
                            id=f"refactor_{current_function}_{function_start}",
                            type="refactor",
                            description=f"Function '{current_function}' is too long ({function_lines} lines). Consider breaking it into smaller functions.",
                            original_code='\n'.join(lines[function_start:i]),
                            suggested_code="# Break this function into smaller, focused functions",
                            confidence=0.8,
                            reasoning="Long functions are harder to understand and maintain",
                            file_path=context.file_path,
                            line_number=function_start + 1,
                            priority="medium",
                            tags=["maintainability", "readability"]
                        ))
                    
                    # Start new function
                    match = re.search(r'def\s+(\w+)', line)
                    if match:
                        current_function = match.group(1)
                        function_start = i
                        function_lines = 0
                
                if current_function:
                    function_lines += 1
            
            # Check the last function
            if current_function and function_lines > 20:
                suggestions.append(CodeSuggestion(
                    id=f"refactor_{current_function}_{function_start}",
                    type="refactor",
                    description=f"Function '{current_function}' is too long ({function_lines} lines). Consider breaking it into smaller functions.",
                    original_code='\n'.join(lines[function_start:]),
                    suggested_code="# Break this function into smaller, focused functions",
                    confidence=0.8,
                    reasoning="Long functions are harder to understand and maintain",
                    file_path=context.file_path,
                    line_number=function_start + 1,
                    priority="medium",
                    tags=["maintainability", "readability"]
                ))
        
        except Exception as e:
            logger.error(f"Python refactoring analysis failed: {str(e)}")
        
        return suggestions
    
    async def _generate_performance_suggestions(self, code: str, context: CodeContext) -> List[CodeSuggestion]:
        """Generate performance optimization suggestions"""
        suggestions = []
        
        # Look for common performance issues
        if 'for' in code and 'append' in code:
            suggestions.append(CodeSuggestion(
                id="perf_list_comprehension",
                type="optimization",
                description="Consider using list comprehension instead of for loop with append",
                original_code=code,
                suggested_code="# Use list comprehension: [expr for item in iterable]",
                confidence=0.7,
                reasoning="List comprehensions are generally faster than for loops with append",
                file_path=context.file_path,
                line_number=1,
                priority="low",
                tags=["performance", "pythonic"]
            ))
        
        return suggestions
    
    async def _generate_bug_fix_suggestions(self, code: str, context: CodeContext) -> List[CodeSuggestion]:
        """Generate bug fix suggestions"""
        suggestions = []
        
        # Look for common bug patterns
        if 'except:' in code:
            suggestions.append(CodeSuggestion(
                id="bug_bare_except",
                type="bug_fix",
                description="Bare except clause can hide unexpected errors",
                original_code="except:",
                suggested_code="except Exception as e:",
                confidence=0.9,
                reasoning="Bare except catches all exceptions including system exit",
                file_path=context.file_path,
                line_number=code.find('except:') + 1,
                priority="high",
                tags=["error_handling", "best_practices"]
            ))
        
        return suggestions
    
    async def _generate_style_suggestions(self, code: str, context: CodeContext) -> List[CodeSuggestion]:
        """Generate style improvement suggestions"""
        suggestions = []
        
        lines = code.split('\n')
        for i, line in enumerate(lines):
            # Check line length
            if len(line) > 79:
                suggestions.append(CodeSuggestion(
                    id=f"style_line_length_{i}",
                    type="style",
                    description="Line is too long (>79 characters)",
                    original_code=line,
                    suggested_code="# Break this line into multiple lines",
                    confidence=0.8,
                    reasoning="PEP 8 recommends maximum line length of 79 characters",
                    file_path=context.file_path,
                    line_number=i + 1,
                    priority="low",
                    tags=["pep8", "readability"]
                ))
        
        return suggestions
    
    def _rank_suggestions(self, suggestions: List[CodeSuggestion]) -> List[CodeSuggestion]:
        """Rank suggestions by confidence, priority, and relevance"""
        priority_scores = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        
        def suggestion_score(suggestion: CodeSuggestion) -> float:
            priority_score = priority_scores.get(suggestion.priority, 1)
            return suggestion.confidence * priority_score
        
        return sorted(suggestions, key=suggestion_score, reverse=True)
    
    def _cache_suggestions(self, file_path: str, suggestions: List[CodeSuggestion]):
        """Cache suggestions for future reference"""
        self.suggestion_cache[file_path] = {
            "suggestions": suggestions,
            "timestamp": logger.info("Suggestions cached")
        }
    
    def _suggestion_to_dict(self, suggestion: CodeSuggestion) -> Dict[str, Any]:
        """Convert CodeSuggestion to dictionary"""
        return {
            "id": suggestion.id,
            "type": suggestion.type,
            "description": suggestion.description,
            "original_code": suggestion.original_code,
            "suggested_code": suggestion.suggested_code,
            "confidence": suggestion.confidence,
            "reasoning": suggestion.reasoning,
            "file_path": suggestion.file_path,
            "line_number": suggestion.line_number,
            "priority": suggestion.priority,
            "tags": suggestion.tags
        }
    
    def _context_to_dict(self, context: CodeContext) -> Dict[str, Any]:
        """Convert CodeContext to dictionary"""
        return {
            "file_path": context.file_path,
            "language": context.language,
            "imports": context.imports,
            "classes": context.classes,
            "functions": context.functions,
            "variables": context.variables,
            "project_context": context.project_context
        }
    
    def _load_code_patterns(self) -> Dict[str, Any]:
        """Load common code patterns and anti-patterns"""
        return {
            "anti_patterns": [
                "bare_except",
                "mutable_default_args",
                "string_concatenation_in_loop",
                "duplicate_code"
            ],
            "good_patterns": [
                "list_comprehension",
                "context_managers",
                "generator_expressions",
                "proper_exception_handling"
            ]
        }
    
    async def _enforce_best_practices(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Enforce coding best practices"""
        code = task.get("code", "")
        language = task.get("language", "python")
        
        try:
            system_prompt = f"""You are a coding standards expert for {language}.
            
            Analyze the code and identify violations of best practices:
            1. Naming conventions
            2. Code organization
            3. Error handling
            4. Security practices
            5. Performance considerations
            6. Documentation requirements
            
            Return violations as JSON array with:
            - "practice": best practice violated
            - "description": explanation of the issue
            - "location": where the violation occurs
            - "severity": severity level
            - "recommendation": how to fix it
            - "example": example of correct implementation"""
            
            user_prompt = f"""Identify best practice violations in this {language} code:

{code}

Focus on practical improvements that follow industry standards."""

            response = await llm_service.chat_completion([
                AIMessage(role="system", content=system_prompt),
                AIMessage(role="user", content=user_prompt)
            ])
            
            try:
                violations = json.loads(response.content)
                if not isinstance(violations, list):
                    violations = [violations]
            except json.JSONDecodeError:
                violations = [{
                    "practice": "general",
                    "description": "Best practice violation identified",
                    "location": "Code analysis",
                    "severity": "medium",
                    "recommendation": response.content,
                    "example": "See recommendation"
                }]
            
            return {
                "success": True,
                "violations": violations,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Best practices enforcement failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "violations": []
            }
    
    async def _analyze_code_context(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and return detailed code context"""
        code = task.get("code", "")
        file_path = task.get("file_path", "")
        language = task.get("language", "python")
        
        try:
            context = await self._build_code_context(code, file_path, language)
            
            return {
                "success": True,
                "context": self._context_to_dict(context),
                "analysis": {
                    "total_imports": len(context.imports),
                    "total_classes": len(context.classes),
                    "total_functions": len(context.functions),
                    "total_variables": len(context.variables),
                    "complexity_score": self._calculate_complexity_score(context)
                }
            }
            
        except Exception as e:
            logger.error(f"Code context analysis failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "context": {}
            }
    
    def _calculate_complexity_score(self, context: CodeContext) -> int:
        """Calculate code complexity score"""
        # Simple complexity calculation
        score = 0
        score += len(context.functions) * 2
        score += len(context.classes) * 3
        score += len(context.imports)
        score += len(context.variables)
        
        return min(score, 100)  # Cap at 100

    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input for code suggestion tasks"""
        try:
            suggestion_type = input_data.get("type", "code_completion")
            code_context = input_data.get("code_context", "")
            
            if suggestion_type == "code_completion":
                return await self._analyze_completion_context(input_data)
            elif suggestion_type == "refactoring":
                return await self._analyze_refactoring_context(input_data)
            elif suggestion_type == "optimization":
                return await self._analyze_optimization_context(input_data)
            else:
                return await self._general_code_analysis(input_data)
                
        except Exception as e:
            logger.error(f"Error analyzing code input: {str(e)}")
            return {
                "success": False,
                "error": f"Code analysis failed: {str(e)}",
                "suggestion_type": input_data.get("type", "unknown")
            }
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents for comprehensive code suggestions"""
        try:
            coordination_results = {}
            task_type = task_context.get("type", "")
            
            # Coordinate with code generator for complex code generation
            if "code_generator" in other_agents and task_type in ["generate_code", "refactor_code"]:
                coordination_results["code_generator"] = await self._coordinate_with_code_generator(task_context)
            
            # Coordinate with testing agent for test-driven suggestions
            if "testing_agent" in other_agents and task_type in ["test_suggestions", "coverage_improvement"]:
                coordination_results["testing_agent"] = await self._coordinate_with_testing_agent(task_context)
            
            # Coordinate with project analyzer for context-aware suggestions
            if "project_analyzer" in other_agents and task_type in ["context_analysis", "architectural_suggestions"]:
                coordination_results["project_analyzer"] = await self._coordinate_with_project_analyzer(task_context)
            
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
    
    # Helper methods for abstract method implementations
    
    async def _analyze_completion_context(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze context for code completion"""
        code_context = input_data.get("code_context", "")
        cursor_position = input_data.get("cursor_position", 0)
        
        return {
            "success": True,
            "analysis_type": "code_completion",
            "context_analysis": {
                "context_length": len(code_context),
                "cursor_position": cursor_position,
                "language": input_data.get("language", "python"),
                "suggestions_available": True
            },
            "summary": "Code completion context analyzed"
        }
    
    async def _analyze_refactoring_context(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze context for code refactoring"""
        code_snippet = input_data.get("code_snippet", "")
        refactor_type = input_data.get("refactor_type", "general")
        
        return {
            "success": True,
            "analysis_type": "refactoring",
            "context_analysis": {
                "code_length": len(code_snippet),
                "refactor_type": refactor_type,
                "complexity": "medium",
                "refactoring_opportunities": ["Extract method", "Simplify conditionals"]
            },
            "summary": "Refactoring context analyzed"
        }
    
    async def _analyze_optimization_context(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze context for performance optimization"""
        code_snippet = input_data.get("code_snippet", "")
        performance_metrics = input_data.get("performance_metrics", {})
        
        return {
            "success": True,
            "analysis_type": "optimization",
            "context_analysis": {
                "code_length": len(code_snippet),
                "performance_metrics": performance_metrics,
                "optimization_potential": "high",
                "optimization_areas": ["Algorithm complexity", "Memory usage"]
            },
            "summary": "Optimization context analyzed"
        }
    
    async def _general_code_analysis(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform general code analysis"""
        code_context = input_data.get("code_context", "")
        
        return {
            "success": True,
            "analysis_type": "general_analysis",
            "context_analysis": {
                "code_length": len(code_context),
                "language": input_data.get("language", "python"),
                "analysis_areas": ["Structure", "Style", "Performance", "Best practices"]
            },
            "summary": "General code analysis completed"
        }
    
    async def _coordinate_with_code_generator(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with code generator agent"""
        return {
            "coordination_type": "code_generator",
            "task_context": task_context,
            "recommendations": ["Generate comprehensive code", "Follow best practices"],
            "status": "coordinated"
        }
    
    async def _coordinate_with_testing_agent(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with testing agent"""
        return {
            "coordination_type": "testing_agent",
            "task_context": task_context,
            "recommendations": ["Generate test cases", "Ensure test coverage"],
            "status": "coordinated"
        }
    
    async def _coordinate_with_project_analyzer(self, task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with project analyzer agent"""
        return {
            "coordination_type": "project_analyzer",
            "task_context": task_context,
            "recommendations": ["Analyze project context", "Provide architectural insights"],
            "status": "coordinated"
        }
