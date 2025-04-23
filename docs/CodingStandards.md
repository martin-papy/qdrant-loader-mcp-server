# Coding Standards for RAG MCP Server

## 1. Python Version and Environment

### 1.1 Version Requirements

- Python 3.9+ required
- Use type hints throughout the codebase
- Follow PEP 484 for type annotations

### 1.2 Development Environment

- Use virtual environments (venv)
- Use Poetry for dependency management
- Use pre-commit hooks for code quality

## 2. Code Style

### 2.1 General Guidelines

- Follow PEP 8 style guide
- Use Black for code formatting
- Use isort for import sorting
- Use flake8 for linting
- Maximum line length: 88 characters (Black default)

### 2.2 Naming Conventions

```python
# Variables and functions
variable_name = "snake_case"
function_name() -> None:
    pass

# Classes
class ClassName:
    pass

# Constants
CONSTANT_NAME = "UPPER_CASE"

# Private members
_private_variable = "leading_underscore"
```

### 2.3 Type Hints

```python
from typing import List, Optional, Dict, Any

def process_query(
    query: str,
    source_types: Optional[List[str]] = None
) -> Dict[str, Any]:
    pass
```

## 3. Project Structure

### 3.1 Directory Layout

```text
qdrant-loader-mcp-server/
├── src/
│   ├── mcp/
│   │   ├── protocol.py
│   │   ├── handler.py
│   │   └── models.py
│   ├── search/
│   │   ├── processor.py
│   │   └── engine.py
│   └── utils/
│       ├── config.py
│       └── logging.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── performance/
├── docs/
├── scripts/
└── config/
```

### 3.2 Module Organization

- One class per file
- Related functionality grouped in modules
- Clear separation of concerns
- Minimal circular dependencies

## 4. Documentation

### 4.1 Code Documentation

- Use Google-style docstrings
- Document all public APIs
- Include type information
- Provide usage examples

```python
def search(
    query: str,
    limit: int = 10
) -> List[SearchResult]:
    """Search for relevant content using the query.

    Args:
        query: The search query string.
        limit: Maximum number of results to return.

    Returns:
        List of search results ordered by relevance.

    Raises:
        SearchError: If the search operation fails.
    """
    pass
```

### 4.2 Module Documentation

- Module-level docstrings
- Purpose and usage
- Dependencies
- Examples

## 5. Error Handling

### 5.1 Exception Hierarchy

```python
class MCPError(Exception):
    """Base exception for MCP-related errors."""
    pass

class ProtocolError(MCPError):
    """Protocol-specific errors."""
    pass

class SearchError(MCPError):
    """Search-related errors."""
    pass
```

### 5.2 Error Handling Guidelines

- Use specific exception types
- Include meaningful error messages
- Log errors with context
- Handle errors at appropriate levels

## 6. Testing

### 6.1 Test Organization

- Unit tests for each module
- Integration tests for workflows
- Performance tests for critical paths
- Test fixtures and utilities

### 6.2 Test Naming

```python
def test_search_with_valid_query():
    pass

def test_search_with_invalid_query():
    pass

def test_search_with_empty_results():
    pass
```

## 7. Logging

### 7.1 Logging Configuration

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
```

### 7.2 Logging Guidelines

- Use appropriate log levels
- Include context in log messages
- Avoid sensitive data in logs
- Use structured logging

## 8. Performance

### 8.1 Optimization Guidelines

- Profile before optimizing
- Use async/await appropriately
- Implement caching where beneficial
- Monitor memory usage

### 8.2 Resource Management

- Use context managers
- Proper cleanup of resources
- Connection pooling
- Memory-efficient data structures

## 9. Security

### 9.1 Security Guidelines

- Validate all input
- Sanitize output
- Use secure defaults
- Follow security best practices

### 9.2 API Security

- Rate limiting
- Input validation
- Error message sanitization
- Secure configuration

## 10. Version Control

### 10.1 Git Workflow

- Feature branches
- Pull requests
- Code review
- Semantic versioning

### 10.2 Commit Messages

```text
feat: add new search endpoint
fix: handle empty query results
docs: update API documentation
test: add performance tests
```

## 11. Dependencies

### 11.1 Dependency Management

- Use Poetry for dependency management
- Pin dependency versions
- Regular dependency updates
- Security scanning

### 11.2 Required Dependencies

```toml
[tool.poetry.dependencies]
python = "^3.9"
fastapi = "^0.104.0"
uvicorn = "^0.24.0"
qdrant-client = "^1.6.0"
openai = "^1.3.0"
pydantic = "^2.4.2"
python-dotenv = "^1.0.0"
```

## 12. Code Review

### 12.1 Review Process

- Code review checklist
- Automated checks
- Manual review
- Documentation review

### 12.2 Review Guidelines

- Check for style compliance
- Verify test coverage
- Review error handling
- Check performance impact
