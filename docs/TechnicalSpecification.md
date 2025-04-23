# Technical Specification: RAG MCP Server for Cursor

## 1. System Architecture

### 1.1 High-Level Overview

The RAG MCP Server is designed as a standalone service that implements the Model Context Protocol (MCP) to provide Cursor with contextually relevant information from various data sources. The system architecture follows a modular design pattern with clear separation of concerns.

### 1.2 Core Components

- **MCP Protocol Handler**: Manages JSON-RPC 2.0 communication and protocol lifecycle
- **Query Processor**: Handles natural language query processing and intent inference
- **Vector Search Engine**: Interfaces with Qdrant for semantic search
- **Embedding Service**: Manages document and query embeddings using OpenAI
- **Streaming Response Handler**: Manages NDJSON streaming of search results

### 1.3 Data Flow

1. Cursor sends query via MCP protocol
2. Query Processor analyzes intent and source type
3. Embedding Service generates query embedding
4. Vector Search Engine performs filtered search
5. Results are streamed back to Cursor in NDJSON format

## 2. Technical Stack

### 2.1 Core Technologies

- **Language**: Python 3.9+
- **Web Framework**: FastAPI
- **Vector Database**: Qdrant
- **Embedding Model**: OpenAI text-embedding-3-small
- **Protocol**: JSON-RPC 2.0 with NDJSON streaming

### 2.2 Dependencies

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

## 3. API Specification

### 3.1 MCP Protocol Implementation

The server implements the following MCP protocol features:

#### 3.1.1 Base Protocol

- JSON-RPC 2.0 message format
- Request/Response/Notification message types
- Error handling as per MCP specification

#### 3.1.2 Lifecycle Management

- Connection initialization
- Capability negotiation
- Session control
- Graceful shutdown

#### 3.1.3 Resources

- Search results streaming
- Metadata retrieval
- Source type filtering

### 3.2 Endpoints

#### 3.2.1 Search Endpoint

```python
async def search(
    query: str,
    source_types: Optional[List[str]] = None,
    limit: int = 10
) -> AsyncGenerator[Dict[str, Any], None]
```

#### 3.2.2 Metadata Endpoint

```python
async def get_metadata(
    source_id: str
) -> Dict[str, Any]
```

## 4. Data Models

### 4.1 Search Request

```python
class SearchRequest(BaseModel):
    query: str
    source_types: Optional[List[str]] = None
    limit: int = 10
```

### 4.2 Search Result

```python
class SearchResult(BaseModel):
    score: float
    text: str
    source_type: str
    source_title: str
    source_url: Optional[str] = None
    file_path: Optional[str] = None
    repo_name: Optional[str] = None
```

## 5. Configuration

### 5.1 Environment Variables

```yaml
QDRANT_URL: str
QDRANT_API_KEY: str
OPENAI_API_KEY: str
SERVER_HOST: str = "localhost"
SERVER_PORT: int = 8000
```

### 5.2 Configuration File

```yaml
server:
  host: localhost
  port: 8000
  log_level: INFO

qdrant:
  url: http://localhost:6333
  collection_name: cursor_context

openai:
  model: text-embedding-3-small
  max_tokens: 8191
```

## 6. Error Handling

### 6.1 MCP Protocol Errors

- Invalid JSON-RPC message format
- Method not found
- Invalid parameters
- Internal server error

### 6.2 Application Errors

- Qdrant connection errors
- OpenAI API errors
- Invalid query format
- Source type validation errors

## 7. Performance Considerations

### 7.1 Optimization Strategies

- Connection pooling for Qdrant
- Caching of frequently accessed results
- Batch processing for multiple queries
- Efficient streaming of large result sets

### 7.2 Resource Requirements

- CPU: 2+ cores
- RAM: 4GB minimum
- Storage: 1GB minimum
- Network: 100Mbps minimum

## 8. Security

### 8.1 Authentication

- No authentication required for MCP server
- Qdrant API key authentication
- OpenAI API key authentication

### 8.2 Data Protection

- Environment variable management
- Secure configuration handling
- Input validation and sanitization

## 9. Monitoring and Logging

### 9.1 Logging Strategy

- Request/Response logging
- Error tracking
- Performance metrics
- Query analytics

### 9.2 Metrics

- Query latency
- Search result quality
- Error rates
- Resource utilization

## 10. Deployment

### 10.1 Local Deployment

```bash
# Installation
pip install -r requirements.txt

# Configuration
cp config.template.yaml config.yaml
# Edit config.yaml with your settings

# Running
python -m uvicorn main:app --host localhost --port 8000
```

### 10.2 Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 11. Testing Strategy

### 11.1 Unit Tests

- MCP protocol implementation
- Query processing
- Vector search
- Error handling

### 11.2 Integration Tests

- End-to-end search flow
- Streaming response handling
- Configuration management
- Error recovery

### 11.3 Performance Tests

- Load testing
- Latency measurement
- Resource utilization
- Streaming efficiency

## 12. Future Enhancements

### 12.1 Planned Features

- Incremental reindexing
- Additional embedding models
- Advanced filtering options
- Query analytics dashboard

### 12.2 Technical Debt

- Code documentation
- Test coverage
- Performance optimization
- Security hardening

## 13. Appendix

### 13.1 MCP Protocol Reference

- JSON-RPC 2.0 specification
- MCP protocol documentation
- Error codes and handling

### 13.2 API Examples

- Search request/response examples
- Error handling examples
- Streaming response examples
