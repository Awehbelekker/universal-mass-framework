"""
Smart Refactoring Assistant
===========================
Automated code optimization and refactoring suggestions for enhanced development speed
"""

import ast
import re
import subprocess
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import complexity_analysis
import performance_analyzer

class RefactoringType(Enum):
    CODE_DUPLICATION = "code_duplication"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    STRUCTURE_IMPROVEMENT = "structure_improvement"
    SECURITY_ENHANCEMENT = "security_enhancement"
    MAINTAINABILITY = "maintainability"
    COMPLEXITY_REDUCTION = "complexity_reduction"

class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class RefactoringIssue:
    """Represents a refactoring issue found in code"""
    issue_type: RefactoringType
    severity: Severity
    description: str
    file_path: str
    line_number: int
    affected_lines: List[int]
    suggested_fix: str
    estimated_impact: int  # Performance improvement percentage
    effort_required: str  # Time estimate

@dataclass
class RefactoringResult:
    """Result of a refactoring operation"""
    original_code: str
    refactored_code: str
    improvements: List[str]
    performance_gain: int
    maintainability_score: int
    before_metrics: Dict[str, Any]
    after_metrics: Dict[str, Any]

class SmartRefactoringAssistant:
    """AI-powered code refactoring and optimization assistant"""
    
    def __init__(self):
        self.code_analyzers = {
            'complexity': ComplexityAnalyzer(),
            'performance': PerformanceAnalyzer(),
            'duplication': DuplicationDetector(),
            'security': SecurityAnalyzer(),
            'structure': StructureAnalyzer()
        }
        self.refactoring_patterns = self._load_refactoring_patterns()
    
    def _load_refactoring_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load refactoring patterns and templates"""
        return {
            'extract_method': {
                'description': 'Extract complex logic into separate methods',
                'pattern': r'def\s+\w+\([^)]*\):[^}]{200,}',  # Functions longer than 200 chars
                'template': '''
def {original_method}({params}):
    """
    {original_docstring}
    """
    {extracted_calls}
    return {return_value}

def {extracted_method}({extracted_params}):
    """
    {extracted_docstring}
    """
    {extracted_logic}
    return {extracted_return}
                '''
            },
            
            'eliminate_duplication': {
                'description': 'Remove duplicated code by extracting common functionality',
                'pattern': r'(.{20,})\s*\n.*\1',  # Repeated code blocks
                'template': '''
def {common_method}({params}):
    """
    {description}
    """
    {common_logic}
    return {return_value}

# Replace duplicated code with calls to {common_method}
                '''
            },
            
            'optimize_loops': {
                'description': 'Optimize loop performance and readability',
                'patterns': {
                    'list_comprehension': {
                        'from': r'for\s+(\w+)\s+in\s+([^:]+):\s*(\w+)\.append\(([^)]+)\)',
                        'to': '{list_name} = [{expression} for {var} in {iterable}]'
                    },
                    'generator_expression': {
                        'from': r'sum\(\[([^]]+)\s+for\s+([^]]+)\s+in\s+([^]]+)\]\)',
                        'to': 'sum({expression} for {var} in {iterable})'
                    }
                }
            },
            
            'improve_error_handling': {
                'description': 'Enhance error handling and logging',
                'template': '''
try:
    {original_code}
except {specific_exception} as e:
    logger.error(f"Specific error in {function_name}: {{str(e)}}")
    {specific_handling}
except Exception as e:
    logger.error(f"Unexpected error in {function_name}: {{str(e)}}")
    {generic_handling}
finally:
    {cleanup_code}
                '''
            },
            
            'database_optimization': {
                'description': 'Optimize database queries and operations',
                'patterns': {
                    'n_plus_one': {
                        'issue': 'N+1 query problem detected',
                        'solution': 'Use eager loading or join queries'
                    },
                    'missing_indexes': {
                        'issue': 'Queries without proper indexing',
                        'solution': 'Add database indexes for frequently queried columns'
                    },
                    'connection_management': {
                        'issue': 'Inefficient connection handling',
                        'solution': 'Use connection pooling and proper connection cleanup'
                    }
                }
            }
        }
    
    async def analyze_code(self, code: str, file_path: str = "") -> List[RefactoringIssue]:
        """Analyze code and identify refactoring opportunities"""
        issues = []
        
        # Run different analyzers
        complexity_issues = await self.code_analyzers['complexity'].analyze(code, file_path)
        performance_issues = await self.code_analyzers['performance'].analyze(code, file_path)
        duplication_issues = await self.code_analyzers['duplication'].analyze(code, file_path)
        security_issues = await self.code_analyzers['security'].analyze(code, file_path)
        structure_issues = await self.code_analyzers['structure'].analyze(code, file_path)
        
        # Combine all issues
        issues.extend(complexity_issues)
        issues.extend(performance_issues)
        issues.extend(duplication_issues)
        issues.extend(security_issues)
        issues.extend(structure_issues)
        
        # Sort by severity and impact
        issues.sort(key=lambda x: (x.severity.value, -x.estimated_impact))
        
        return issues
    
    async def suggest_refactoring(self, issue: RefactoringIssue, code: str) -> str:
        """Generate refactoring suggestion for a specific issue"""
        if issue.issue_type == RefactoringType.CODE_DUPLICATION:
            return await self._suggest_duplication_fix(issue, code)
        elif issue.issue_type == RefactoringType.PERFORMANCE_OPTIMIZATION:
            return await self._suggest_performance_fix(issue, code)
        elif issue.issue_type == RefactoringType.COMPLEXITY_REDUCTION:
            return await self._suggest_complexity_fix(issue, code)
        elif issue.issue_type == RefactoringType.SECURITY_ENHANCEMENT:
            return await self._suggest_security_fix(issue, code)
        elif issue.issue_type == RefactoringType.STRUCTURE_IMPROVEMENT:
            return await self._suggest_structure_fix(issue, code)
        else:
            return await self._suggest_generic_fix(issue, code)
    
    async def _suggest_duplication_fix(self, issue: RefactoringIssue, code: str) -> str:
        """Suggest fixes for code duplication"""
        pattern = self.refactoring_patterns['eliminate_duplication']
        
        # Extract duplicated code
        lines = code.split('\n')
        duplicated_section = '\n'.join(lines[issue.line_number:issue.line_number + len(issue.affected_lines)])
        
        # Generate common method
        common_method_name = self._generate_method_name(duplicated_section)
        parameters = self._extract_parameters(duplicated_section)
        
        refactored = pattern['template'].format(
            common_method=common_method_name,
            params=', '.join(parameters),
            description=f"Common functionality extracted from lines {issue.line_number}-{max(issue.affected_lines)}",
            common_logic=duplicated_section.strip(),
            return_value=self._extract_return_value(duplicated_section)
        )
        
        return refactored
    
    async def _suggest_performance_fix(self, issue: RefactoringIssue, code: str) -> str:
        """Suggest performance optimizations"""
        lines = code.split('\n')
        problematic_code = '\n'.join(lines[issue.line_number-1:issue.line_number + len(issue.affected_lines)])
        
        # Check for common performance issues
        if 'for ' in problematic_code and '.append(' in problematic_code:
            # Suggest list comprehension
            return self._convert_to_list_comprehension(problematic_code)
        elif 'SELECT' in problematic_code.upper() and 'WHERE' not in problematic_code.upper():
            # Suggest adding WHERE clause or indexing
            return f"# Add WHERE clause to limit results\n{problematic_code.replace('SELECT', 'SELECT # TODO: Add WHERE clause\\n')}"
        elif 'for ' in problematic_code and 'if ' in problematic_code:
            # Suggest filter or generator expression
            return self._optimize_filtering_loop(problematic_code)
        else:
            return f"# Performance optimization needed\n{problematic_code}\n# TODO: Consider caching, memoization, or algorithm optimization"
    
    async def _suggest_complexity_fix(self, issue: RefactoringIssue, code: str) -> str:
        """Suggest complexity reduction strategies"""
        lines = code.split('\n')
        complex_section = '\n'.join(lines[issue.line_number-1:issue.line_number + len(issue.affected_lines)])
        
        # Extract method refactoring for complex functions
        if 'def ' in complex_section:
            method_parts = self._split_complex_method(complex_section)
            refactored_methods = []
            
            for i, part in enumerate(method_parts):
                if i == 0:
                    # Main method
                    refactored_methods.append(part)
                else:
                    # Extracted methods
                    method_name = f"_extracted_logic_{i}"
                    refactored_methods.append(f"def {method_name}(self, {self._extract_parameters(part)}):\n    {part}")
            
            return '\n\n'.join(refactored_methods)
        
        return f"# Complexity reduction needed\n{complex_section}\n# TODO: Break down into smaller, focused methods"
    
    async def _suggest_security_fix(self, issue: RefactoringIssue, code: str) -> str:
        """Suggest security enhancements"""
        lines = code.split('\n')
        vulnerable_code = '\n'.join(lines[issue.line_number-1:issue.line_number + len(issue.affected_lines)])
        
        # Common security fixes
        if 'execute(' in vulnerable_code and '%' in vulnerable_code:
            # SQL injection prevention
            return vulnerable_code.replace(
                'execute(',
                '# Use parameterized queries to prevent SQL injection\nexecute('
            ).replace('%', '?')
        elif 'eval(' in vulnerable_code:
            # Dangerous eval usage
            return f"# SECURITY WARNING: eval() is dangerous\n# {vulnerable_code}\n# TODO: Replace eval() with safer alternatives like ast.literal_eval()"
        elif 'open(' in vulnerable_code and 'w' in vulnerable_code:
            # File operation security
            return vulnerable_code.replace('open(', '# Validate file path before opening\nopen(')
        
        return f"# Security enhancement needed\n{vulnerable_code}\n# TODO: Review for security vulnerabilities"
    
    async def _suggest_structure_fix(self, issue: RefactoringIssue, code: str) -> str:
        """Suggest structural improvements"""
        lines = code.split('\n')
        structural_section = '\n'.join(lines[issue.line_number-1:issue.line_number + len(issue.affected_lines)])
        
        # Add type hints if missing
        if 'def ' in structural_section and '->' not in structural_section:
            return self._add_type_hints(structural_section)
        
        # Add docstrings if missing
        if '"""' not in structural_section and 'def ' in structural_section:
            return self._add_docstring(structural_section)
        
        return f"# Structural improvement needed\n{structural_section}\n# TODO: Add type hints, docstrings, and proper error handling"
    
    async def _suggest_generic_fix(self, issue: RefactoringIssue, code: str) -> str:
        """Generic refactoring suggestions"""
        return f"# {issue.description}\n# TODO: {issue.suggested_fix}"
    
    def _generate_method_name(self, code: str) -> str:
        """Generate appropriate method name from code"""
        # Extract key words from code and create method name
        words = re.findall(r'\b[a-zA-Z]+\b', code)
        meaningful_words = [word.lower() for word in words if len(word) > 2 and word.lower() not in ['the', 'and', 'for', 'with']]
        return '_'.join(meaningful_words[:3]) if meaningful_words else 'extracted_method'
    
    def _extract_parameters(self, code: str) -> List[str]:
        """Extract potential parameters from code"""
        # Simple parameter extraction (would be more sophisticated in production)
        variables = re.findall(r'\b[a-zA-Z_]\w*\b', code)
        return list(set(variables))[:5]  # Limit to 5 parameters
    
    def _extract_return_value(self, code: str) -> str:
        """Extract return value from code"""
        if 'return ' in code:
            return_match = re.search(r'return\s+(.+)', code)
            return return_match.group(1) if return_match else 'None'
        return 'None'
    
    def _convert_to_list_comprehension(self, code: str) -> str:
        """Convert loop with append to list comprehension"""
        # Simple conversion (would be more sophisticated in production)
        match = re.search(r'for\s+(\w+)\s+in\s+([^:]+):\s*(\w+)\.append\(([^)]+)\)', code)
        if match:
            var, iterable, list_name, expression = match.groups()
            return f"{list_name} = [{expression} for {var} in {iterable}]"
        return code
    
    def _optimize_filtering_loop(self, code: str) -> str:
        """Optimize filtering loops"""
        # Convert to filter or generator expression
        if 'if ' in code and 'for ' in code:
            return f"# Consider using filter() or generator expression\n{code}\n# Example: filtered_items = [item for item in items if condition]"
        return code
    
    def _split_complex_method(self, method_code: str) -> List[str]:
        """Split complex method into smaller parts"""
        # Simple splitting by logical blocks (would be more sophisticated in production)
        lines = method_code.split('\n')
        parts = []
        current_part = []
        
        for line in lines:
            current_part.append(line)
            if len(current_part) > 10 and (line.strip().startswith('if') or line.strip().startswith('for')):
                parts.append('\n'.join(current_part))
                current_part = []
        
        if current_part:
            parts.append('\n'.join(current_part))
        
        return parts if len(parts) > 1 else [method_code]
    
    def _add_type_hints(self, code: str) -> str:
        """Add type hints to function definitions"""
        # Simple type hint addition (would use AST analysis in production)
        if 'def ' in code and '->' not in code:
            return code.replace('def ', 'def ').replace('):', ') -> Any:')
        return code
    
    def _add_docstring(self, code: str) -> str:
        """Add docstring to functions"""
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('def '):
                # Insert docstring after function definition
                lines.insert(i + 1, '    """TODO: Add function description"""')
                break
        return '\n'.join(lines)

    async def perform_refactoring(self, code: str, issues: List[RefactoringIssue]) -> RefactoringResult:
        """Perform automatic refactoring based on identified issues"""
        original_code = code
        refactored_code = code
        improvements = []
        
        # Calculate before metrics
        before_metrics = await self._calculate_metrics(original_code)
        
        # Apply refactoring for each issue
        for issue in issues:
            if issue.severity in [Severity.HIGH, Severity.CRITICAL]:
                suggested_fix = await self.suggest_refactoring(issue, refactored_code)
                refactored_code = self._apply_refactoring(refactored_code, issue, suggested_fix)
                improvements.append(f"Fixed {issue.issue_type.value}: {issue.description}")
        
        # Calculate after metrics
        after_metrics = await self._calculate_metrics(refactored_code)
        
        # Calculate performance gain
        performance_gain = self._calculate_performance_gain(before_metrics, after_metrics)
        
        return RefactoringResult(
            original_code=original_code,
            refactored_code=refactored_code,
            improvements=improvements,
            performance_gain=performance_gain,
            maintainability_score=after_metrics.get('maintainability', 0),
            before_metrics=before_metrics,
            after_metrics=after_metrics
        )
    
    def _apply_refactoring(self, code: str, issue: RefactoringIssue, suggested_fix: str) -> str:
        """Apply refactoring suggestion to code"""
        lines = code.split('\n')
        
        # Replace affected lines with suggested fix
        start_line = max(0, issue.line_number - 1)
        end_line = min(len(lines), start_line + len(issue.affected_lines))
        
        # Replace the affected section
        new_lines = lines[:start_line] + suggested_fix.split('\n') + lines[end_line:]
        
        return '\n'.join(new_lines)
    
    async def _calculate_metrics(self, code: str) -> Dict[str, Any]:
        """Calculate code quality metrics"""
        # This would use actual static analysis tools in production
        return {
            'complexity': self._calculate_complexity(code),
            'maintainability': self._calculate_maintainability(code),
            'performance_score': self._estimate_performance(code),
            'security_score': self._assess_security(code),
            'lines_of_code': len(code.split('\n'))
        }
    
    def _calculate_complexity(self, code: str) -> int:
        """Calculate cyclomatic complexity"""
        # Simple complexity calculation (would use proper tools in production)
        complexity_indicators = ['if ', 'for ', 'while ', 'except ', 'elif ', 'and ', 'or ']
        return sum(code.count(indicator) for indicator in complexity_indicators)
    
    def _calculate_maintainability(self, code: str) -> int:
        """Calculate maintainability score"""
        score = 100
        
        # Deduct points for various maintainability issues
        if '"""' not in code:  # No docstrings
            score -= 20
        if '->' not in code and 'def ' in code:  # No type hints
            score -= 15
        if 'TODO' in code or 'FIXME' in code:  # Has TODO items
            score -= 10
        if len(code.split('\n')) > 100:  # Very long files
            score -= 15
        
        return max(0, score)
    
    def _estimate_performance(self, code: str) -> int:
        """Estimate performance score"""
        score = 100
        
        # Deduct points for performance issues
        if 'for ' in code and '.append(' in code:  # Inefficient list building
            score -= 20
        if code.count('for ') > 3:  # Multiple nested loops
            score -= 15
        if 'SELECT *' in code.upper():  # Inefficient database queries
            score -= 25
        
        return max(0, score)
    
    def _assess_security(self, code: str) -> int:
        """Assess security score"""
        score = 100
        
        # Deduct points for security issues
        if 'eval(' in code:  # Dangerous eval usage
            score -= 30
        if 'execute(' in code and '%' in code:  # Potential SQL injection
            score -= 25
        if 'pickle.loads(' in code:  # Dangerous deserialization
            score -= 20
        
        return max(0, score)
    
    def _calculate_performance_gain(self, before: Dict[str, Any], after: Dict[str, Any]) -> int:
        """Calculate performance improvement percentage"""
        before_score = before.get('performance_score', 0)
        after_score = after.get('performance_score', 0)
        
        if before_score == 0:
            return 0
        
        return max(0, int(((after_score - before_score) / before_score) * 100))

# Analyzer classes for different aspects of code quality
class ComplexityAnalyzer:
    """Analyzes code complexity and suggests simplifications"""
    
    async def analyze(self, code: str, file_path: str) -> List[RefactoringIssue]:
        """Analyze code complexity"""
        issues = []
        lines = code.split('\n')
        
        # Analyze each function for complexity
        for i, line in enumerate(lines):
            if line.strip().startswith('def '):
                function_complexity = self._analyze_function_complexity(lines, i)
                if function_complexity > 10:  # High complexity threshold
                    issues.append(RefactoringIssue(
                        issue_type=RefactoringType.COMPLEXITY_REDUCTION,
                        severity=Severity.HIGH if function_complexity > 15 else Severity.MEDIUM,
                        description=f"Function has high cyclomatic complexity ({function_complexity})",
                        file_path=file_path,
                        line_number=i + 1,
                        affected_lines=list(range(i, i + self._get_function_length(lines, i))),
                        suggested_fix="Break down into smaller, focused methods",
                        estimated_impact=25,
                        effort_required="30-60 minutes"
                    ))
        
        return issues
    
    def _analyze_function_complexity(self, lines: List[str], start_line: int) -> int:
        """Calculate cyclomatic complexity for a function"""
        complexity = 1  # Base complexity
        function_lines = self._get_function_lines(lines, start_line)
        
        for line in function_lines:
            # Count complexity-adding constructs
            complexity += line.count('if ') + line.count('elif ') + line.count('for ') + \
                         line.count('while ') + line.count('except ') + line.count('and ') + \
                         line.count('or ')
        
        return complexity
    
    def _get_function_lines(self, lines: List[str], start_line: int) -> List[str]:
        """Get all lines belonging to a function"""
        function_lines = []
        indent_level = len(lines[start_line]) - len(lines[start_line].lstrip())
        
        for i in range(start_line, len(lines)):
            line = lines[i]
            if line.strip() == '':
                continue
            
            current_indent = len(line) - len(line.lstrip())
            if i > start_line and current_indent <= indent_level and line.strip():
                break
            
            function_lines.append(line)
        
        return function_lines
    
    def _get_function_length(self, lines: List[str], start_line: int) -> int:
        """Get the length of a function in lines"""
        return len(self._get_function_lines(lines, start_line))

class PerformanceAnalyzer:
    """Analyzes code for performance issues"""
    
    async def analyze(self, code: str, file_path: str) -> List[RefactoringIssue]:
        """Analyze code for performance issues"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Check for common performance issues
            if 'for ' in line and any(lines[j].strip().endswith('.append(') for j in range(i+1, min(i+5, len(lines)))):
                issues.append(RefactoringIssue(
                    issue_type=RefactoringType.PERFORMANCE_OPTIMIZATION,
                    severity=Severity.MEDIUM,
                    description="Inefficient list building with append in loop",
                    file_path=file_path,
                    line_number=i + 1,
                    affected_lines=[i + 1, i + 2],
                    suggested_fix="Use list comprehension instead of append in loop",
                    estimated_impact=30,
                    effort_required="5-10 minutes"
                ))
            
            if 'SELECT *' in line.upper():
                issues.append(RefactoringIssue(
                    issue_type=RefactoringType.PERFORMANCE_OPTIMIZATION,
                    severity=Severity.HIGH,
                    description="Inefficient SELECT * query",
                    file_path=file_path,
                    line_number=i + 1,
                    affected_lines=[i + 1],
                    suggested_fix="Select only needed columns",
                    estimated_impact=50,
                    effort_required="5-15 minutes"
                ))
        
        return issues

class DuplicationDetector:
    """Detects code duplication"""
    
    async def analyze(self, code: str, file_path: str) -> List[RefactoringIssue]:
        """Detect code duplication"""
        issues = []
        lines = code.split('\n')
        
        # Simple duplication detection (would be more sophisticated in production)
        for i in range(len(lines) - 5):
            for j in range(i + 5, len(lines) - 5):
                similarity = self._calculate_similarity(lines[i:i+5], lines[j:j+5])
                if similarity > 0.8:  # 80% similarity threshold
                    issues.append(RefactoringIssue(
                        issue_type=RefactoringType.CODE_DUPLICATION,
                        severity=Severity.MEDIUM,
                        description=f"Code duplication detected (similarity: {similarity:.0%})",
                        file_path=file_path,
                        line_number=i + 1,
                        affected_lines=list(range(i + 1, i + 6)) + list(range(j + 1, j + 6)),
                        suggested_fix="Extract common functionality into a separate method",
                        estimated_impact=20,
                        effort_required="15-30 minutes"
                    ))
        
        return issues
    
    def _calculate_similarity(self, block1: List[str], block2: List[str]) -> float:
        """Calculate similarity between two code blocks"""
        if len(block1) != len(block2):
            return 0.0
        
        similar_lines = sum(1 for line1, line2 in zip(block1, block2) if line1.strip() == line2.strip())
        return similar_lines / len(block1)

class SecurityAnalyzer:
    """Analyzes code for security issues"""
    
    async def analyze(self, code: str, file_path: str) -> List[RefactoringIssue]:
        """Analyze code for security vulnerabilities"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Check for common security issues
            if 'eval(' in line:
                issues.append(RefactoringIssue(
                    issue_type=RefactoringType.SECURITY_ENHANCEMENT,
                    severity=Severity.CRITICAL,
                    description="Dangerous use of eval() function",
                    file_path=file_path,
                    line_number=i + 1,
                    affected_lines=[i + 1],
                    suggested_fix="Replace eval() with safer alternatives like ast.literal_eval()",
                    estimated_impact=0,  # Security fix, not performance
                    effort_required="10-20 minutes"
                ))
            
            if 'execute(' in line and '%' in line:
                issues.append(RefactoringIssue(
                    issue_type=RefactoringType.SECURITY_ENHANCEMENT,
                    severity=Severity.HIGH,
                    description="Potential SQL injection vulnerability",
                    file_path=file_path,
                    line_number=i + 1,
                    affected_lines=[i + 1],
                    suggested_fix="Use parameterized queries instead of string formatting",
                    estimated_impact=0,  # Security fix, not performance
                    effort_required="15-30 minutes"
                ))
        
        return issues

class StructureAnalyzer:
    """Analyzes code structure and organization"""
    
    async def analyze(self, code: str, file_path: str) -> List[RefactoringIssue]:
        """Analyze code structure"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            # Check for missing type hints
            if line.strip().startswith('def ') and '->' not in line:
                issues.append(RefactoringIssue(
                    issue_type=RefactoringType.STRUCTURE_IMPROVEMENT,
                    severity=Severity.LOW,
                    description="Function missing return type hint",
                    file_path=file_path,
                    line_number=i + 1,
                    affected_lines=[i + 1],
                    suggested_fix="Add return type hint to function signature",
                    estimated_impact=0,  # Maintainability improvement
                    effort_required="2-5 minutes"
                ))
            
            # Check for missing docstrings
            if line.strip().startswith('def ') or line.strip().startswith('class '):
                next_line = lines[i+1] if i+1 < len(lines) else ""
                if '"""' not in next_line:
                    issues.append(RefactoringIssue(
                        issue_type=RefactoringType.STRUCTURE_IMPROVEMENT,
                        severity=Severity.LOW,
                        description="Missing docstring",
                        file_path=file_path,
                        line_number=i + 1,
                        affected_lines=[i + 1],
                        suggested_fix="Add comprehensive docstring",
                        estimated_impact=0,  # Maintainability improvement
                        effort_required="5-10 minutes"
                    ))
        
        return issues

# Export main classes
__all__ = [
    'SmartRefactoringAssistant',
    'RefactoringIssue',
    'RefactoringResult',
    'RefactoringType',
    'Severity'
]
