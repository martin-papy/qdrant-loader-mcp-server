# Client Usage Guide: RAG MCP Server for Cursor

## 1. Overview

This document describes how to use the RAG MCP Server from Cursor's perspective. The server implements the Model Context Protocol (MCP) to provide contextually relevant information to Cursor.

## 2. Connection Setup

### 2.1 Server Configuration

```yaml
# config.yaml
server:
  host: localhost
  port: 8000
  protocol: json-rpc
  streaming: true
```

### 2.2 Connection Initialization

```python
# Example connection setup
import jsonrpcclient
from jsonrpcclient.clients.http_client import HTTPClient

client = HTTPClient("http://localhost:8000")
```

## 3. MCP Protocol Usage

### 3.1 Basic Search

```python
# Example search request
response = client.request(
    "search",
    {
        "query": "How do I configure OAuth?",
        "source_types": ["confluence", "git"],
        "limit": 5
    }
)
```

### 3.2 Streaming Results

```python
# Example streaming search
async for result in client.stream(
    "search",
    {
        "query": "Authentication setup",
        "source_types": ["confluence"]
    }
):
    print(f"Score: {result['score']}")
    print(f"Text: {result['text']}")
    print(f"Source: {result['source_type']}")
```

## 4. Query Examples

### 4.1 Technical Documentation Search

```python
# Search for technical documentation
response = client.request(
    "search",
    {
        "query": "How to implement rate limiting in FastAPI",
        "source_types": ["confluence", "git"],
        "limit": 3
    }
)
```

### 4.2 Code Search

```python
# Search for code examples
response = client.request(
    "search",
    {
        "query": "FastAPI middleware implementation",
        "source_types": ["git"],
        "limit": 5
    }
)
```

### 4.3 Issue Search

```python
# Search for related issues
response = client.request(
    "search",
    {
        "query": "Authentication bug in login flow",
        "source_types": ["jira"],
        "limit": 3
    }
)
```

## 5. Response Handling

### 5.1 Basic Response

```python
# Handle basic response
response = client.request("search", {"query": "example"})
if response.is_success():
    results = response.result
    for result in results:
        print(f"Score: {result['score']}")
        print(f"Text: {result['text']}")
```

### 5.2 Streaming Response

```python
# Handle streaming response
async for result in client.stream("search", {"query": "example"}):
    if result.is_success():
        print(f"Score: {result['score']}")
        print(f"Text: {result['text']}")
    else:
        print(f"Error: {result.error}")
```

## 6. Error Handling

### 6.1 Protocol Errors

```python
try:
    response = client.request("search", {"query": "example"})
except jsonrpcclient.exceptions.ReceiveError as e:
    print(f"Protocol error: {e}")
```

### 6.2 Application Errors

```python
response = client.request("search", {"query": "example"})
if not response.is_success():
    print(f"Error: {response.error}")
```

## 7. Best Practices

### 7.1 Query Formulation

- Be specific in queries
- Use relevant source types
- Set appropriate limits
- Consider context

### 7.2 Response Processing

- Handle errors gracefully
- Process streaming results efficiently
- Validate response format
- Cache frequently used results

## 8. Performance Considerations

### 8.1 Query Optimization

- Use specific source types
- Set reasonable limits
- Avoid unnecessary queries
- Cache common queries

### 8.2 Resource Management

- Close connections properly
- Handle timeouts
- Implement retry logic
- Monitor resource usage

## 9. Integration Examples

### 9.1 Cursor Integration

```python
# Example Cursor integration
class CursorMCPClient:
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.client = HTTPClient(f"http://{host}:{port}")

    async def get_context(self, query: str) -> List[Dict[str, Any]]:
        results = []
        async for result in self.client.stream(
            "search",
            {"query": query, "limit": 5}
        ):
            results.append(result)
        return results
```

### 9.2 Error Recovery

```python
# Example error recovery
async def get_context_with_retry(
    client: CursorMCPClient,
    query: str,
    max_retries: int = 3
) -> List[Dict[str, Any]]:
    for attempt in range(max_retries):
        try:
            return await client.get_context(query)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(1)
```

## 10. Troubleshooting

### 10.1 Common Issues

- Connection refused
- Protocol errors
- Timeout errors
- Invalid responses

### 10.2 Debugging

- Enable debug logging
- Check server status
- Verify configuration
- Monitor network traffic

## 11. Future Enhancements

### 11.1 Planned Features

- Advanced filtering
- Custom scoring
- Batch processing
- Caching support

### 11.2 Client Improvements

- Better error handling
- Enhanced streaming
- Performance optimization
- Additional examples
