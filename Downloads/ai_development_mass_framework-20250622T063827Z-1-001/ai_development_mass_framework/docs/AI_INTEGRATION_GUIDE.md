# AI Integration Documentation - MASS Framework Phase 1.1

## Overview

The MASS Framework Phase 1.1 introduces comprehensive AI integration capabilities, transforming the framework into an AI-powered development platform. This documentation covers all AI features, agents, and capabilities.

## Table of Contents

1. [AI Architecture Overview](#ai-architecture-overview)
2. [AI Agents](#ai-agents)
3. [LLM Service](#llm-service)
4. [AI Coordinator](#ai-coordinator)
5. [API Endpoints](#api-endpoints)
6. [Frontend Components](#frontend-components)
7. [Configuration](#configuration)
8. [Usage Examples](#usage-examples)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

## AI Architecture Overview

The AI integration follows a modular, extensible architecture:

```
┌─────────────────────────────────────────┐
│              Frontend Layer             │
│  ┌─────────────┐  ┌─────────────────┐   │
│  │   AIChat    │  │ AIWorkflowBuilder│   │
│  └─────────────┘  └─────────────────┘   │
└─────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────┐
│               API Layer                 │
│  AI Endpoints (/api/ai/*)               │
└─────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────┐
│            AI Coordinator               │
│  Task Analysis │ Agent Recommendation   │
│  Workflow Creation │ Natural Language   │
└─────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────┐
│              AI Agents                  │
│ ┌─────────────┐ ┌─────────────────────┐ │
│ │CodeGenerator│ │Documentation Agent  │ │
│ └─────────────┘ └─────────────────────┘ │
│ ┌─────────────┐ ┌─────────────────────┐ │
│ │Testing Agent│ │Debugging Agent      │ │
│ └─────────────┘ └─────────────────────┘ │
└─────────────────────────────────────────┘
                     │
┌─────────────────────────────────────────┐
│            LLM Service                  │
│  OpenAI │ Anthropic │ Future Providers │
└─────────────────────────────────────────┘
```

## AI Agents

### 1. AI Code Generator Agent (`ai_code_generator`)

**Purpose**: Generate, refactor, and improve code using AI.

**Capabilities**:
- Code generation from natural language descriptions
- Code refactoring and optimization
- Code review and analysis
- Test generation
- Bug fixing
- Code explanation

**Supported Languages**:
- Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, SQL

**Usage Example**:
```python
agent = CodeGeneratorAgent()
result = await agent.process_task({
    "type": "generate_code",
    "description": "Create a function to calculate fibonacci numbers",
    "language": "python",
    "template": "function"
})
```

### 2. AI Documentation Agent (`ai_documentation_agent`)

**Purpose**: Generate comprehensive documentation using AI.

**Capabilities**:
- API documentation generation
- User guide creation
- Technical specification writing
- README generation
- Code documentation
- Architecture documentation

**Document Types**:
- `api_documentation`
- `user_guide`
- `technical_specification`
- `readme`
- `changelog`
- `installation_guide`
- `troubleshooting_guide`
- `architecture_overview`

**Usage Example**:
```python
agent = AIDocumentationAgent()
result = await agent.process_task({
    "type": "generate_documentation",
    "doc_type": "api_documentation",
    "content": "REST API endpoints",
    "project_info": {"name": "My API", "version": "1.0.0"}
})
```

### 3. AI Testing Agent (`ai_testing_agent`)

**Purpose**: Generate comprehensive test suites using AI.

**Capabilities**:
- Unit test generation
- Integration test creation
- End-to-end test development
- Performance test generation
- Security test creation
- Test coverage analysis
- Test optimization

**Test Types**:
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests
- Security tests
- API tests
- UI tests
- Load tests

**Supported Frameworks**:
- Python: pytest, unittest, nose2
- JavaScript: jest, mocha, cypress
- Java: junit, testng
- C#: nunit, xunit, mstest

**Usage Example**:
```python
agent = AITestingAgent()
result = await agent.process_task({
    "type": "generate_tests",
    "code": "def fibonacci(n): ...",
    "language": "python",
    "test_type": "unit_tests",
    "framework": "pytest"
})
```

### 4. AI Debugging Agent (`ai_debugging_agent`)

**Purpose**: Debug and fix code issues using AI.

**Capabilities**:
- Error diagnosis and analysis
- Bug fixing
- Performance analysis
- Memory leak detection
- Security vulnerability assessment
- Code optimization
- Debugging guidance

**Bug Types**:
- Syntax errors
- Runtime errors
- Logic errors
- Performance issues
- Memory leaks
- Security vulnerabilities
- Concurrency issues

**Usage Example**:
```python
agent = AIDebuggingAgent()
result = await agent.process_task({
    "type": "debug_error",
    "code": "problematic_code_here",
    "error_message": "NameError: name 'x' is not defined",
    "language": "python"
})
```

## LLM Service

The LLM Service provides a unified interface for multiple AI providers.

### Supported Providers

1. **OpenAI**
   - Models: GPT-4, GPT-3.5-turbo
   - Features: Chat completion, function calling
   - Configuration: API key required

2. **Anthropic**
   - Models: Claude-3 Opus, Claude-3 Sonnet
   - Features: Chat completion, long context
   - Configuration: API key required

### Configuration

```yaml
# config/ai_config.yaml
llm_providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    default_model: "gpt-4"
    max_tokens: 4096
  
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    default_model: "claude-3-opus-20240229"
    max_tokens: 4096

default_provider: "openai"
```

### Usage

```python
from core.llm_service import llm_service, AIMessage

response = await llm_service.chat_completion([
    AIMessage(role="system", content="You are a helpful assistant"),
    AIMessage(role="user", content="Help me write a function")
])
```

## AI Coordinator

The AI Coordinator manages AI operations and provides intelligent task routing.

### Capabilities

- **Task Analysis**: Analyze natural language requests and determine requirements
- **Agent Recommendation**: Recommend appropriate agents for specific tasks
- **Workflow Creation**: Generate complete workflows from descriptions
- **Natural Language Interface**: Process natural language commands
- **Usage Monitoring**: Track AI usage and performance metrics

### Key Methods

```python
# Analyze a task
analysis = await ai_coordinator.analyze_task(
    "Create a Python web scraper with tests"
)

# Recommend agents
agents = await ai_coordinator.recommend_agents(
    "Build a REST API with documentation"
)

# Create workflow
workflow = await ai_coordinator.create_workflow(
    "Develop a data processing pipeline",
    requirements={"language": "python"},
    preferences={"style": "functional"}
)

# Chat interface
response = await ai_coordinator.chat(
    "How do I optimize this SQL query?",
    context={"database": "postgresql"},
    conversation_history=[]
)
```

## API Endpoints

### Chat Endpoints

#### POST /api/ai/chat
Natural language chat interface with AI assistant.

**Request**:
```json
{
  "message": "Help me create a REST API",
  "context": {"language": "python", "framework": "fastapi"},
  "conversation_history": []
}
```

**Response**:
```json
{
  "status": "success",
  "response": "I can help you create a REST API using FastAPI...",
  "suggestions": ["Generate API endpoints", "Create data models"],
  "usage": {"total_tokens": 150, "cost": 0.003}
}
```

### Code Generation Endpoints

#### POST /api/ai/generate-code
Generate code from natural language description.

**Request**:
```json
{
  "description": "Create a function to validate email addresses",
  "language": "python",
  "template": "function",
  "requirements": ["use regex", "handle edge cases"]
}
```

#### POST /api/ai/review-code
Review code quality and provide suggestions.

**Request**:
```json
{
  "code": "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
  "language": "python",
  "review_criteria": ["performance", "style", "security"]
}
```

### Documentation Endpoints

#### POST /api/ai/generate-documentation
Generate documentation from code or specifications.

**Request**:
```json
{
  "doc_type": "api_documentation",
  "content": "FastAPI application with user management",
  "project_info": {"name": "User API", "version": "1.0.0"}
}
```

#### POST /api/ai/analyze-code-for-docs
Analyze code to generate documentation.

**Request**:
```json
{
  "code": "class User: ...",
  "language": "python"
}
```

### Testing Endpoints

#### POST /api/ai/generate-tests
Generate test suites for code.

**Request**:
```json
{
  "code": "def calculate_tax(income, rate): ...",
  "language": "python",
  "test_type": "unit_tests",
  "framework": "pytest"
}
```

#### POST /api/ai/analyze-coverage
Analyze test coverage and suggest improvements.

**Request**:
```json
{
  "code": "source_code_here",
  "existing_tests": "existing_test_code",
  "language": "python"
}
```

### Debugging Endpoints

#### POST /api/ai/debug-error
Debug errors and provide solutions.

**Request**:
```json
{
  "code": "problematic_code",
  "error_message": "IndexError: list index out of range",
  "language": "python",
  "stack_trace": "Traceback (most recent call last): ..."
}
```

#### POST /api/ai/fix-bug
Fix identified bugs in code.

**Request**:
```json
{
  "code": "buggy_code_here",
  "bug_description": "Function doesn't handle empty input",
  "language": "python"
}
```

### Coordinator Endpoints

#### POST /api/ai/analyze-task
Analyze task requirements and complexity.

#### POST /api/ai/create-workflow
Create workflow from natural language description.

#### POST /api/ai/recommend-agents
Recommend appropriate agents for a task.

#### GET /api/ai/usage-stats
Get AI usage statistics and metrics.

#### GET /api/ai/models
Get available AI models and their capabilities.

## Frontend Components

### AIChat Component

Interactive chat interface for AI assistance.

**Features**:
- Real-time messaging
- Conversation history
- Code syntax highlighting
- File upload support
- Quick actions

**Usage**:
```tsx
import AIChat from './components/AIChat';

<AIChat />
```

### AIWorkflowBuilder Component

Visual workflow builder with AI assistance.

**Features**:
- Natural language workflow creation
- Visual workflow editor
- Agent recommendation
- Real-time preview
- Workflow execution

**Usage**:
```tsx
import AIWorkflowBuilder from './components/AIWorkflowBuilder';

<AIWorkflowBuilder />
```

## Configuration

### Environment Variables

```bash
# Required API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional Configuration
AI_DEFAULT_PROVIDER=openai
AI_MAX_TOKENS=4096
AI_TEMPERATURE=0.7
AI_DEBUG_MODE=false
```

### Configuration Files

**config/ai_config.yaml**:
```yaml
llm_providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    default_model: "gpt-4"
    max_tokens: 4096
    temperature: 0.7
  
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    default_model: "claude-3-opus-20240229"
    max_tokens: 4096
    temperature: 0.7

default_provider: "openai"
fallback_provider: "anthropic"

# Cost tracking
track_usage: true
cost_alerts:
  daily_limit: 10.00
  monthly_limit: 100.00

# Performance settings
timeout: 30
max_retries: 3
concurrent_requests: 5
```

## Usage Examples

### Complete Development Workflow

```python
# 1. Generate code
code_result = await ai_code_generator.process_task({
    "type": "generate_code",
    "description": "Create a user authentication system",
    "language": "python",
    "framework": "fastapi"
})

# 2. Generate tests
test_result = await ai_testing_agent.process_task({
    "type": "generate_tests",
    "code": code_result["generated_code"],
    "language": "python",
    "test_type": "unit_tests"
})

# 3. Generate documentation
doc_result = await ai_documentation_agent.process_task({
    "type": "generate_documentation",
    "content": code_result["generated_code"],
    "doc_type": "api_documentation"
})

# 4. Review and optimize
review_result = await ai_code_generator.process_task({
    "type": "review_code",
    "code": code_result["generated_code"],
    "review_criteria": ["security", "performance"]
})
```

### Natural Language Workflow Creation

```python
# Create workflow from description
workflow = await ai_coordinator.create_workflow(
    "Build a machine learning model to predict house prices with data preprocessing, model training, evaluation, and deployment",
    requirements={
        "language": "python",
        "ml_framework": "scikit-learn",
        "deployment": "docker"
    },
    preferences={
        "style": "object_oriented",
        "documentation": "comprehensive"
    }
)
```

### Interactive Debugging Session

```python
# Debug an error
debug_result = await ai_debugging_agent.process_task({
    "type": "debug_error",
    "code": """
def process_data(data):
    result = []
    for item in data:
        if item['value'] > 0:
            result.append(item['value'] * 2)
    return result
    """,
    "error_message": "KeyError: 'value'",
    "language": "python"
})

# Get fix suggestion
fix_result = await ai_debugging_agent.process_task({
    "type": "fix_bug",
    "code": debug_result["problematic_code"],
    "bug_description": debug_result["root_cause"],
    "language": "python"
})
```

## Testing

### Running AI Tests

```bash
# Run all AI tests
python -m pytest tests/test_ai_integration.py -v

# Run specific test categories
python -m pytest tests/test_ai_integration.py::TestCodeGeneratorAgent -v
python -m pytest tests/test_ai_api_integration.py::TestAIChatEndpoint -v

# Run with coverage
python -m pytest tests/ --cov=agents.ai_agents --cov=core.ai_coordinator --cov-report=html
```

### Mock Testing

For testing without API costs:

```python
# Mock LLM responses
@patch('core.llm_service.llm_service.chat_completion')
def test_code_generation(mock_chat):
    mock_chat.return_value = Mock(
        content="def test_function(): return 42",
        usage={"total_tokens": 20}
    )
    # Test code here
```

## Troubleshooting

### Common Issues

1. **API Key Issues**
   ```
   Error: Invalid API key
   Solution: Check environment variables and API key validity
   ```

2. **Rate Limiting**
   ```
   Error: Rate limit exceeded
   Solution: Implement backoff strategy or upgrade API plan
   ```

3. **Context Length Errors**
   ```
   Error: Context length exceeded
   Solution: Reduce input size or use models with larger context
   ```

4. **Import Errors**
   ```
   Error: Cannot import AI agents
   Solution: Ensure all dependencies are installed (pip install -r requirements.txt)
   ```

### Performance Optimization

1. **Concurrent Requests**: Use async/await for multiple AI operations
2. **Caching**: Cache frequent AI responses
3. **Model Selection**: Use appropriate models for different tasks
4. **Token Management**: Monitor and optimize token usage

### Monitoring and Logging

```python
# Enable debug logging
import logging
logging.getLogger('ai_agents').setLevel(logging.DEBUG)

# Monitor usage
usage_stats = await ai_coordinator.get_usage_stats()
print(f"Total tokens used: {usage_stats['total_tokens']}")
print(f"Total cost: ${usage_stats['total_cost']}")
```

## Next Steps

### Phase 1.2 - Advanced AI Features
- Multi-agent collaboration
- Custom model fine-tuning
- AI-powered project analysis
- Intelligent code suggestions

### Phase 2 - Enterprise Features
- Team collaboration
- Advanced security
- Audit logging
- Custom AI models

### Phase 3 - Cloud Deployment
- Scalable infrastructure
- Multi-tenant support
- Global deployment
- Enterprise integrations

## Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation
- Submit issues on GitHub
- Contact support team

---

*This documentation covers MASS Framework Phase 1.1 AI Integration. For the latest updates, check the official repository.*
