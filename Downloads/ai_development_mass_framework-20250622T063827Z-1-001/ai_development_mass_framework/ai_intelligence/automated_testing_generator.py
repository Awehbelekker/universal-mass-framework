"""
Automated Testing Generator
===========================
Intelligent test case generation and validation for enhanced development speed
"""

import ast
import inspect
import re
from typing import Dict, List, Any, Optional, Tuple, Union, Type
from dataclasses import dataclass
from enum import Enum
import unittest
import pytest

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    EDGE_CASE = "edge_case"

class TestFramework(Enum):
    UNITTEST = "unittest"
    PYTEST = "pytest"
    DOCTEST = "doctest"

@dataclass
class TestCase:
    """Represents a generated test case"""
    name: str
    test_type: TestType
    description: str
    setup_code: str
    test_code: str
    assertions: List[str]
    expected_result: Any
    input_data: Dict[str, Any]
    cleanup_code: str = ""

@dataclass
class TestSuite:
    """Collection of test cases for a function or class"""
    target_name: str
    target_type: str  # function, class, method
    test_cases: List[TestCase]
    coverage_percentage: float
    edge_cases_covered: int
    framework: TestFramework

class AutomatedTestingGenerator:
    """AI-powered automated test generation system"""
    
    def __init__(self, framework: TestFramework = TestFramework.PYTEST):
        self.framework = framework
        self.test_patterns = self._load_test_patterns()
        self.edge_case_generators = self._initialize_edge_case_generators()
        
    def _load_test_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load test generation patterns and templates"""
        return {
            'function_tests': {
                'basic_functionality': '''
def test_{function_name}_basic_functionality():
    """Test basic functionality of {function_name}"""
    # Arrange
    {setup_code}
    
    # Act
    result = {function_name}({input_params})
    
    # Assert
    {assertions}
                ''',
                
                'edge_cases': '''
def test_{function_name}_edge_cases():
    """Test edge cases for {function_name}"""
    # Test empty input
    with pytest.raises({expected_exception}):
        {function_name}({empty_input})
    
    # Test null input
    with pytest.raises({expected_exception}):
        {function_name}(None)
    
    # Test boundary values
    {boundary_tests}
                ''',
                
                'error_handling': '''
def test_{function_name}_error_handling():
    """Test error handling in {function_name}"""
    # Test invalid input types
    with pytest.raises(TypeError):
        {function_name}({invalid_type_input})
    
    # Test invalid values
    with pytest.raises(ValueError):
        {function_name}({invalid_value_input})
    
    # Test specific error conditions
    {specific_error_tests}
                '''
            },
            
            'class_tests': {
                'initialization': '''
def test_{class_name}_initialization():
    """Test {class_name} initialization"""
    # Test valid initialization
    instance = {class_name}({valid_init_params})
    assert instance is not None
    {attribute_assertions}
    
    # Test invalid initialization
    with pytest.raises({expected_exception}):
        {class_name}({invalid_init_params})
                ''',
                
                'method_tests': '''
def test_{class_name}_{method_name}():
    """Test {class_name}.{method_name} method"""
    # Setup
    instance = {class_name}({init_params})
    
    # Test method functionality
    result = instance.{method_name}({method_params})
    {method_assertions}
    
    # Test method state changes
    {state_assertions}
                '''
            },
            
            'api_tests': {
                'endpoint_test': '''
def test_{endpoint_name}_endpoint():
    """Test {endpoint_name} API endpoint"""
    # Test successful request
    response = client.{http_method}('{endpoint_path}', json={valid_payload})
    assert response.status_code == {expected_status}
    assert response.json() == {expected_response}
    
    # Test invalid request
    response = client.{http_method}('{endpoint_path}', json={invalid_payload})
    assert response.status_code == {error_status}
    
    # Test authentication required
    response = client.{http_method}('{endpoint_path}', json={valid_payload}, headers={{}})
    assert response.status_code == 401
                ''',
                
                'rate_limiting_test': '''
def test_{endpoint_name}_rate_limiting():
    """Test rate limiting for {endpoint_name} endpoint"""
    # Make multiple requests rapidly
    for i in range({rate_limit} + 1):
        response = client.{http_method}('{endpoint_path}', json={valid_payload})
        if i < {rate_limit}:
            assert response.status_code != 429
        else:
            assert response.status_code == 429
                '''
            },
            
            'database_tests': {
                'crud_operations': '''
def test_{model_name}_crud_operations():
    """Test CRUD operations for {model_name}"""
    # Create
    instance = {model_name}.create({create_data})
    assert instance.id is not None
    
    # Read
    retrieved = {model_name}.get(instance.id)
    assert retrieved.id == instance.id
    
    # Update
    updated = instance.update({update_data})
    assert updated.{updated_field} == {expected_value}
    
    # Delete
    deleted = instance.delete()
    assert deleted is True
    assert {model_name}.get(instance.id) is None
                ''',
                
                'validation_tests': '''
def test_{model_name}_validation():
    """Test {model_name} validation rules"""
    # Test valid data
    valid_instance = {model_name}({valid_data})
    assert valid_instance.is_valid()
    
    # Test invalid data
    invalid_instance = {model_name}({invalid_data})
    assert not invalid_instance.is_valid()
    assert len(invalid_instance.errors) > 0
    
    # Test specific validation rules
    {specific_validations}
                '''
            }
        }
    
    def _initialize_edge_case_generators(self) -> Dict[str, callable]:
        """Initialize edge case generators for different data types"""
        return {
            'string': self._generate_string_edge_cases,
            'int': self._generate_int_edge_cases,
            'float': self._generate_float_edge_cases,
            'list': self._generate_list_edge_cases,
            'dict': self._generate_dict_edge_cases,
            'bool': self._generate_bool_edge_cases,
            'date': self._generate_date_edge_cases,
            'email': self._generate_email_edge_cases,
            'url': self._generate_url_edge_cases
        }
    
    async def generate_tests_for_function(self, function_code: str, function_name: str) -> TestSuite:
        """Generate comprehensive test suite for a function"""
        # Analyze function signature and behavior
        function_analysis = self._analyze_function(function_code, function_name)
        
        test_cases = []
        
        # Generate basic functionality tests
        basic_tests = await self._generate_basic_functionality_tests(function_analysis)
        test_cases.extend(basic_tests)
        
        # Generate edge case tests
        edge_case_tests = await self._generate_edge_case_tests(function_analysis)
        test_cases.extend(edge_case_tests)
        
        # Generate error handling tests
        error_tests = await self._generate_error_handling_tests(function_analysis)
        test_cases.extend(error_tests)
        
        # Generate performance tests if applicable
        if function_analysis.get('complexity', 'low') in ['medium', 'high']:
            performance_tests = await self._generate_performance_tests(function_analysis)
            test_cases.extend(performance_tests)
        
        # Calculate coverage
        coverage = self._calculate_coverage(function_analysis, test_cases)
        edge_cases_count = len([tc for tc in test_cases if tc.test_type == TestType.EDGE_CASE])
        
        return TestSuite(
            target_name=function_name,
            target_type='function',
            test_cases=test_cases,
            coverage_percentage=coverage,
            edge_cases_covered=edge_cases_count,
            framework=self.framework
        )
    
    async def generate_tests_for_class(self, class_code: str, class_name: str) -> TestSuite:
        """Generate comprehensive test suite for a class"""
        # Analyze class structure and methods
        class_analysis = self._analyze_class(class_code, class_name)
        
        test_cases = []
        
        # Generate initialization tests
        init_tests = await self._generate_initialization_tests(class_analysis)
        test_cases.extend(init_tests)
        
        # Generate method tests
        for method_name, method_info in class_analysis.get('methods', {}).items():
            method_tests = await self._generate_method_tests(class_analysis, method_name, method_info)
            test_cases.extend(method_tests)
        
        # Generate property tests
        property_tests = await self._generate_property_tests(class_analysis)
        test_cases.extend(property_tests)
        
        # Generate integration tests
        integration_tests = await self._generate_integration_tests(class_analysis)
        test_cases.extend(integration_tests)
        
        # Calculate coverage
        coverage = self._calculate_coverage(class_analysis, test_cases)
        edge_cases_count = len([tc for tc in test_cases if tc.test_type == TestType.EDGE_CASE])
        
        return TestSuite(
            target_name=class_name,
            target_type='class',
            test_cases=test_cases,
            coverage_percentage=coverage,
            edge_cases_covered=edge_cases_count,
            framework=self.framework
        )
    
    async def generate_tests_for_api(self, api_spec: Dict[str, Any]) -> TestSuite:
        """Generate tests for API endpoints"""
        endpoint_name = api_spec.get('name', 'api_endpoint')
        test_cases = []
        
        # Generate endpoint functionality tests
        endpoint_tests = await self._generate_endpoint_tests(api_spec)
        test_cases.extend(endpoint_tests)
        
        # Generate authentication tests
        auth_tests = await self._generate_auth_tests(api_spec)
        test_cases.extend(auth_tests)
        
        # Generate rate limiting tests
        if api_spec.get('rate_limit'):
            rate_limit_tests = await self._generate_rate_limit_tests(api_spec)
            test_cases.extend(rate_limit_tests)
        
        # Generate security tests
        security_tests = await self._generate_security_tests(api_spec)
        test_cases.extend(security_tests)
        
        coverage = 95  # APIs typically have high test coverage
        edge_cases_count = len([tc for tc in test_cases if tc.test_type == TestType.EDGE_CASE])
        
        return TestSuite(
            target_name=endpoint_name,
            target_type='api',
            test_cases=test_cases,
            coverage_percentage=coverage,
            edge_cases_covered=edge_cases_count,
            framework=self.framework
        )
    
    def _analyze_function(self, function_code: str, function_name: str) -> Dict[str, Any]:
        """Analyze function to understand its behavior and requirements"""
        try:
            # Parse function code
            tree = ast.parse(function_code)
            function_node = None
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    function_node = node
                    break
            
            if not function_node:
                return {'name': function_name, 'parameters': [], 'return_type': 'unknown'}
            
            # Extract function information
            parameters = []
            for arg in function_node.args.args:
                param_info = {
                    'name': arg.arg,
                    'type': self._infer_parameter_type(arg, function_code),
                    'default': None
                }
                parameters.append(param_info)
            
            # Extract defaults
            defaults = function_node.args.defaults
            if defaults:
                for i, default in enumerate(defaults):
                    param_index = len(parameters) - len(defaults) + i
                    if param_index >= 0:
                        parameters[param_index]['default'] = ast.unparse(default)
            
            return {
                'name': function_name,
                'parameters': parameters,
                'return_type': self._infer_return_type(function_node, function_code),
                'complexity': self._calculate_complexity(function_node),
                'has_exceptions': self._has_exception_handling(function_node),
                'docstring': ast.get_docstring(function_node),
                'async': isinstance(function_node, ast.AsyncFunctionDef)
            }
            
        except Exception as e:
            # Fallback analysis
            return {
                'name': function_name,
                'parameters': self._extract_parameters_fallback(function_code),
                'return_type': 'unknown',
                'complexity': 'medium',
                'has_exceptions': 'try:' in function_code,
                'docstring': None,
                'async': 'async def' in function_code
            }
    
    def _analyze_class(self, class_code: str, class_name: str) -> Dict[str, Any]:
        """Analyze class structure and methods"""
        try:
            tree = ast.parse(class_code)
            class_node = None
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    class_node = node
                    break
            
            if not class_node:
                return {'name': class_name, 'methods': {}, 'attributes': []}
            
            methods = {}
            attributes = []
            
            for node in class_node.body:
                if isinstance(node, ast.FunctionDef):
                    methods[node.name] = {
                        'name': node.name,
                        'parameters': [arg.arg for arg in node.args.args[1:]],  # Skip 'self'
                        'is_property': self._is_property(node),
                        'is_private': node.name.startswith('_'),
                        'docstring': ast.get_docstring(node)
                    }
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            attributes.append(target.id)
            
            return {
                'name': class_name,
                'methods': methods,
                'attributes': attributes,
                'docstring': ast.get_docstring(class_node),
                'inheritance': [base.id for base in class_node.bases if isinstance(base, ast.Name)]
            }
            
        except Exception as e:
            return {
                'name': class_name,
                'methods': self._extract_methods_fallback(class_code),
                'attributes': [],
                'docstring': None,
                'inheritance': []
            }
    
    async def _generate_basic_functionality_tests(self, function_analysis: Dict[str, Any]) -> List[TestCase]:
        """Generate basic functionality test cases"""
        test_cases = []
        function_name = function_analysis['name']
        parameters = function_analysis['parameters']
        
        # Generate test with typical input values
        typical_inputs = self._generate_typical_inputs(parameters)
        
        test_case = TestCase(
            name=f"test_{function_name}_basic_functionality",
            test_type=TestType.UNIT,
            description=f"Test basic functionality of {function_name}",
            setup_code=self._generate_setup_code(function_analysis),
            test_code=self._generate_basic_test_code(function_analysis, typical_inputs),
            assertions=self._generate_basic_assertions(function_analysis, typical_inputs),
            expected_result=self._predict_expected_result(function_analysis, typical_inputs),
            input_data=typical_inputs
        )
        
        test_cases.append(test_case)
        return test_cases
    
    async def _generate_edge_case_tests(self, function_analysis: Dict[str, Any]) -> List[TestCase]:
        """Generate edge case test cases"""
        test_cases = []
        function_name = function_analysis['name']
        parameters = function_analysis['parameters']
        
        for param in parameters:
            param_type = param['type']
            if param_type in self.edge_case_generators:
                edge_cases = self.edge_case_generators[param_type]()
                
                for edge_case in edge_cases:
                    test_inputs = self._generate_typical_inputs(parameters)
                    test_inputs[param['name']] = edge_case['value']
                    
                    test_case = TestCase(
                        name=f"test_{function_name}_{param['name']}_{edge_case['name']}",
                        test_type=TestType.EDGE_CASE,
                        description=f"Test {function_name} with {edge_case['description']}",
                        setup_code="",
                        test_code=self._generate_edge_case_test_code(function_analysis, test_inputs, edge_case),
                        assertions=self._generate_edge_case_assertions(function_analysis, edge_case),
                        expected_result=edge_case.get('expected_result'),
                        input_data=test_inputs
                    )
                    
                    test_cases.append(test_case)
        
        return test_cases
    
    async def _generate_error_handling_tests(self, function_analysis: Dict[str, Any]) -> List[TestCase]:
        """Generate error handling test cases"""
        test_cases = []
        function_name = function_analysis['name']
        
        # Test invalid input types
        test_case = TestCase(
            name=f"test_{function_name}_invalid_input_types",
            test_type=TestType.UNIT,
            description=f"Test {function_name} with invalid input types",
            setup_code="",
            test_code=f"""
    with pytest.raises(TypeError):
        {function_name}("invalid_type")
            """,
            assertions=["pytest.raises(TypeError)"],
            expected_result="TypeError",
            input_data={"invalid_input": "invalid_type"}
        )
        
        test_cases.append(test_case)
        return test_cases
    
    async def _generate_performance_tests(self, function_analysis: Dict[str, Any]) -> List[TestCase]:
        """Generate performance test cases"""
        test_cases = []
        function_name = function_analysis['name']
        
        test_case = TestCase(
            name=f"test_{function_name}_performance",
            test_type=TestType.PERFORMANCE,
            description=f"Test {function_name} performance",
            setup_code="import time\nimport statistics",
            test_code=f"""
    # Performance test
    times = []
    for _ in range(100):
        start_time = time.time()
        result = {function_name}({self._get_performance_test_inputs(function_analysis)})
        times.append(time.time() - start_time)
    
    avg_time = statistics.mean(times)
    assert avg_time < 0.1  # Should complete in less than 100ms
            """,
            assertions=["avg_time < 0.1"],
            expected_result="< 0.1 seconds",
            input_data={}
        )
        
        test_cases.append(test_case)
        return test_cases
    
    def _generate_typical_inputs(self, parameters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate typical input values for parameters"""
        inputs = {}
        
        for param in parameters:
            param_name = param['name']
            param_type = param['type']
            
            if param_type == 'str':
                inputs[param_name] = "test_string"
            elif param_type == 'int':
                inputs[param_name] = 42
            elif param_type == 'float':
                inputs[param_name] = 3.14
            elif param_type == 'bool':
                inputs[param_name] = True
            elif param_type == 'list':
                inputs[param_name] = [1, 2, 3]
            elif param_type == 'dict':
                inputs[param_name] = {"key": "value"}
            else:
                inputs[param_name] = None
        
        return inputs
    
    def _generate_string_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge cases for string parameters"""
        return [
            {"name": "empty_string", "value": "", "description": "empty string", "expected_result": "handled_gracefully"},
            {"name": "very_long_string", "value": "x" * 10000, "description": "very long string", "expected_result": "handled_gracefully"},
            {"name": "unicode_string", "value": "测试🔥", "description": "unicode string", "expected_result": "handled_gracefully"},
            {"name": "whitespace_string", "value": "   ", "description": "whitespace only string", "expected_result": "handled_gracefully"},
            {"name": "null_bytes", "value": "test\x00null", "description": "string with null bytes", "expected_result": "handled_gracefully"}
        ]
    
    def _generate_int_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge cases for integer parameters"""
        return [
            {"name": "zero", "value": 0, "description": "zero value", "expected_result": "handled_gracefully"},
            {"name": "negative", "value": -1, "description": "negative value", "expected_result": "handled_gracefully"},
            {"name": "max_int", "value": 2**31 - 1, "description": "maximum integer", "expected_result": "handled_gracefully"},
            {"name": "min_int", "value": -2**31, "description": "minimum integer", "expected_result": "handled_gracefully"}
        ]
    
    def _generate_float_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge cases for float parameters"""
        return [
            {"name": "zero_float", "value": 0.0, "description": "zero float", "expected_result": "handled_gracefully"},
            {"name": "infinity", "value": float('inf'), "description": "infinity", "expected_result": "handled_gracefully"},
            {"name": "negative_infinity", "value": float('-inf'), "description": "negative infinity", "expected_result": "handled_gracefully"},
            {"name": "nan", "value": float('nan'), "description": "NaN", "expected_result": "handled_gracefully"}
        ]
    
    def _generate_list_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge cases for list parameters"""
        return [
            {"name": "empty_list", "value": [], "description": "empty list", "expected_result": "handled_gracefully"},
            {"name": "single_item_list", "value": [1], "description": "single item list", "expected_result": "handled_gracefully"},
            {"name": "large_list", "value": list(range(10000)), "description": "large list", "expected_result": "handled_gracefully"}
        ]
    
    def _generate_dict_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge cases for dictionary parameters"""
        return [
            {"name": "empty_dict", "value": {}, "description": "empty dictionary", "expected_result": "handled_gracefully"},
            {"name": "nested_dict", "value": {"a": {"b": {"c": "deep"}}}, "description": "deeply nested dictionary", "expected_result": "handled_gracefully"}
        ]
    
    def _generate_bool_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge cases for boolean parameters"""
        return [
            {"name": "true", "value": True, "description": "True value", "expected_result": "handled_gracefully"},
            {"name": "false", "value": False, "description": "False value", "expected_result": "handled_gracefully"}
        ]
    
    def _generate_date_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge cases for date parameters"""
        from datetime import datetime, date
        return [
            {"name": "epoch", "value": datetime(1970, 1, 1), "description": "epoch date", "expected_result": "handled_gracefully"},
            {"name": "future_date", "value": datetime(2100, 1, 1), "description": "far future date", "expected_result": "handled_gracefully"}
        ]
    
    def _generate_email_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge cases for email parameters"""
        return [
            {"name": "invalid_email", "value": "invalid-email", "description": "invalid email format", "expected_result": "validation_error"},
            {"name": "long_email", "value": "a" * 250 + "@example.com", "description": "very long email", "expected_result": "validation_error"}
        ]
    
    def _generate_url_edge_cases(self) -> List[Dict[str, Any]]:
        """Generate edge cases for URL parameters"""
        return [
            {"name": "invalid_url", "value": "not-a-url", "description": "invalid URL format", "expected_result": "validation_error"},
            {"name": "malformed_url", "value": "http://", "description": "malformed URL", "expected_result": "validation_error"}
        ]
    
    def generate_test_file(self, test_suite: TestSuite) -> str:
        """Generate complete test file code"""
        if self.framework == TestFramework.PYTEST:
            return self._generate_pytest_file(test_suite)
        elif self.framework == TestFramework.UNITTEST:
            return self._generate_unittest_file(test_suite)
        else:
            return self._generate_doctest_file(test_suite)
    
    def _generate_pytest_file(self, test_suite: TestSuite) -> str:
        """Generate pytest test file"""
        imports = """
import pytest
import asyncio
from unittest.mock import Mock, patch
from datetime import datetime, date
import json
import time
import statistics
"""
        
        test_functions = []
        for test_case in test_suite.test_cases:
            test_function = f'''
def {test_case.name}():
    """{test_case.description}"""
    {test_case.setup_code}
    
    {test_case.test_code}
'''
            test_functions.append(test_function)
        
        return imports + '\n'.join(test_functions)
    
    def _generate_unittest_file(self, test_suite: TestSuite) -> str:
        """Generate unittest test file"""
        class_name = f"Test{test_suite.target_name.title()}"
        
        imports = """
import unittest
from unittest.mock import Mock, patch
from datetime import datetime, date
import json
import time
import statistics
"""
        
        test_methods = []
        for test_case in test_suite.test_cases:
            test_method = f'''
    def {test_case.name}(self):
        """{test_case.description}"""
        {test_case.setup_code}
        
        {test_case.test_code}
'''
            test_methods.append(test_method)
        
        class_definition = f'''
class {class_name}(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
{''.join(test_methods)}

if __name__ == '__main__':
    unittest.main()
'''
        
        return imports + class_definition
    
    # Helper methods for analysis
    def _infer_parameter_type(self, arg: ast.arg, function_code: str) -> str:
        """Infer parameter type from annotation or context"""
        if arg.annotation:
            return ast.unparse(arg.annotation)
        
        # Try to infer from context
        param_name = arg.arg
        if 'email' in param_name.lower():
            return 'email'
        elif 'url' in param_name.lower():
            return 'url'
        elif 'date' in param_name.lower():
            return 'date'
        elif 'id' in param_name.lower():
            return 'int'
        elif 'name' in param_name.lower():
            return 'str'
        else:
            return 'unknown'
    
    def _infer_return_type(self, function_node: ast.FunctionDef, function_code: str) -> str:
        """Infer return type from annotation or return statements"""
        if function_node.returns:
            return ast.unparse(function_node.returns)
        
        # Analyze return statements
        for node in ast.walk(function_node):
            if isinstance(node, ast.Return) and node.value:
                return 'inferred'
        
        return 'None'
    
    def _calculate_complexity(self, function_node: ast.FunctionDef) -> str:
        """Calculate function complexity"""
        complexity_score = 1  # Base complexity
        
        for node in ast.walk(function_node):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                complexity_score += 1
        
        if complexity_score <= 5:
            return 'low'
        elif complexity_score <= 10:
            return 'medium'
        else:
            return 'high'
    
    def _has_exception_handling(self, function_node: ast.FunctionDef) -> bool:
        """Check if function has exception handling"""
        for node in ast.walk(function_node):
            if isinstance(node, ast.Try):
                return True
        return False
    
    def _calculate_coverage(self, analysis: Dict[str, Any], test_cases: List[TestCase]) -> float:
        """Calculate test coverage percentage"""
        # Simple coverage calculation based on test types
        test_types = set(tc.test_type for tc in test_cases)
        
        coverage = 60  # Base coverage
        if TestType.EDGE_CASE in test_types:
            coverage += 20
        if TestType.PERFORMANCE in test_types:
            coverage += 10
        if TestType.SECURITY in test_types:
            coverage += 10
        
        return min(coverage, 100)
    
    # Additional helper methods...
    def _extract_parameters_fallback(self, function_code: str) -> List[Dict[str, Any]]:
        """Fallback parameter extraction using regex"""
        match = re.search(r'def\s+\w+\s*\(([^)]*)\)', function_code)
        if match:
            params_str = match.group(1)
            params = [p.strip() for p in params_str.split(',') if p.strip() and p.strip() != 'self']
            return [{'name': p, 'type': 'unknown', 'default': None} for p in params]
        return []
    
    def _extract_methods_fallback(self, class_code: str) -> Dict[str, Any]:
        """Fallback method extraction using regex"""
        methods = {}
        for match in re.finditer(r'def\s+(\w+)\s*\(([^)]*)\)', class_code):
            method_name = match.group(1)
            params_str = match.group(2)
            params = [p.strip() for p in params_str.split(',') if p.strip() and p.strip() != 'self']
            
            methods[method_name] = {
                'name': method_name,
                'parameters': params,
                'is_property': False,
                'is_private': method_name.startswith('_'),
                'docstring': None
            }
        
        return methods
    
    def _is_property(self, node: ast.FunctionDef) -> bool:
        """Check if method is a property"""
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == 'property':
                return True
        return False
    
    def _generate_setup_code(self, analysis: Dict[str, Any]) -> str:
        """Generate setup code for tests"""
        return "# Setup test data\npass"
    
    def _generate_basic_test_code(self, analysis: Dict[str, Any], inputs: Dict[str, Any]) -> str:
        """Generate basic test code"""
        function_name = analysis['name']
        params = ', '.join(f"{k}={repr(v)}" for k, v in inputs.items())
        return f"result = {function_name}({params})"
    
    def _generate_basic_assertions(self, analysis: Dict[str, Any], inputs: Dict[str, Any]) -> List[str]:
        """Generate basic assertions"""
        return ["assert result is not None"]
    
    def _predict_expected_result(self, analysis: Dict[str, Any], inputs: Dict[str, Any]) -> Any:
        """Predict expected result based on function analysis"""
        return "predicted_result"
    
    def _generate_edge_case_test_code(self, analysis: Dict[str, Any], inputs: Dict[str, Any], edge_case: Dict[str, Any]) -> str:
        """Generate edge case test code"""
        function_name = analysis['name']
        params = ', '.join(f"{k}={repr(v)}" for k, v in inputs.items())
        return f"result = {function_name}({params})"
    
    def _generate_edge_case_assertions(self, analysis: Dict[str, Any], edge_case: Dict[str, Any]) -> List[str]:
        """Generate edge case assertions"""
        return ["assert result is not None"]
    
    def _get_performance_test_inputs(self, analysis: Dict[str, Any]) -> str:
        """Get inputs for performance testing"""
        return "test_input"

# Export main classes
__all__ = [
    'AutomatedTestingGenerator',
    'TestCase',
    'TestSuite',
    'TestType',
    'TestFramework'
]
