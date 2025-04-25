# MCP Server Configuration Guide

## Overview

This document describes the Model Context Protocol (MCP) configuration and implementation details for our RAG MCP Server. It provides a comprehensive guide for setting up and configuring the server to work with Cursor.

## MCP Configuration File

The server is configured through a `mcp.json` file that defines how Cursor should interact with our server. Here's the complete configuration:

```json
        "qdrant-loader-mcp-server": {
            "command": "mcp-qdrant-loader",
            "env": {
                "QDRANT_URL": "http://localhost:6333",
                "QDRANT_API_KEY": "",
                "QDRANT_COLLECTION_NAME": "qdrant-loader-mcp-server",
                "MCP_LOG_LEVEL": "DEBUG",
                "MCP_LOG_FILE": "/path/to/your/mcp-qdrant-loader.log",
                "MCP_DISABLE_CONSOLE_LOGGING": "true"
            }
```

## Configuration Components

### 1. Server Identity

- **name**: Unique identifier for the server
- **version**: Server version
- **description**: Brief description of server capabilities

### 2. Command Configuration

- **command**: How to start the server
- **args**: Command-line arguments
- **env**: Required environment variables
  - `QDRANT_URL`: Qdrant server URL
  - `QDRANT_API_KEY`: Qdrant API key
  - `OPENAI_API_KEY`: OpenAI API key
  - `SERVER_HOST`: (optional) Server host, defaults to "localhost"
  - `SERVER_PORT`: (optional) Server port, defaults to 8000

### 3. Capabilities

#### Tools

- **search**: Main search tool for semantic queries
  - Parameters: query, source_types, limit
  - Returns: Array of search results with metadata

#### Resources

- **search_results**: Streaming resource for search results
  - Content type: NDJSON
  - Schema: Query and results structure

### 4. Server Settings

- **host**: Server hostname
- **port**: Server port
- **protocol**: Communication protocol
- **streaming**: Streaming support flag

### 5. Error Handling

- **retry**: Retry configuration
  - max_attempts: Maximum retry attempts
  - backoff: Retry backoff strategy

## Implementation Details

### 1. Server Startup

The server is started using Python and uvicorn:

```bash
python -m uvicorn src.main:app --host localhost --port 8000
```

### 2. Environment Variables

Required environment variables:

- `QDRANT_URL`: Qdrant server URL
- `QDRANT_API_KEY`: Qdrant API key
- `OPENAI_API_KEY`: OpenAI API key

### 3. Protocol Implementation

- JSON-RPC 2.0 for communication
- NDJSON for streaming responses
- Proper error handling and retries

### 4. Search Capabilities

- Natural language query processing
- Source type filtering
- Configurable result limits
- Rich metadata in results

## Usage with Cursor

1. Place the `mcp.json` file in the appropriate Cursor configuration directory
2. Ensure all required environment variables are set
3. Cursor will automatically start the server when needed
4. The server will be available for semantic search queries

## Error Handling

The server implements comprehensive error handling:

- Protocol errors
- Search errors
- Connection errors
- Retry mechanism with exponential backoff

## Security Considerations

- No authentication required for MCP server
- Environment variables for sensitive data
- Input validation and sanitization
- Proper error message handling

## Performance Considerations

- Streaming responses for efficiency
- Configurable result limits
- Proper resource cleanup
- Connection pooling

## Future Enhancements

1. Additional search capabilities
2. More source types
3. Advanced filtering options
4. Performance optimizations
5. Enhanced error handling

## Related Documentation

- [Technical Specification](TechnicalSpecification.md)
- [Client Usage Guide](ClientUsage.md)
- [Testing Strategy](TestingStrategy.md)
- [Coding Standards](CodingStandards.md)
