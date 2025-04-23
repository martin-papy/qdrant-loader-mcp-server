# RAG MCP Server Implementation Plan for Cursor with Qdrant

## Overview

We are designing a Retrieval-Augmented Generation (RAG) Model Context Protocol (MCP) server that integrates with Cursor. It will use the data ingested by `qdrant-loader` and stored in a Qdrant DB. The primary purpose of this server is to allow Cursor to search and retrieve contextually relevant content to enhance its responses.

## Primary Use Case

- **Search and analyze** technical content stored in Qdrant to return rich context to Cursor.
- Secondary feature (future): **Reindexing** of code repositories upon changes.

## Data Sources

We plan to ingest data from:

- Git repositories
- Confluence spaces
- JIRA issues
- Public documentation

These sources require smart chunking, consistent metadata tagging, and normalization.

## Embedding Strategy

- Using **OpenAI embeddings**, specifically `text-embedding-3-small`.
- Embeddings are used for both ingestion (in a future release) and querying to maintain consistency.
- Future support for additional embedding models.

## Server Architecture

### Tech Stack

- **Python** with **FastAPI**
- **Qdrant** (local or cloud) as the vector DB backend
- **OpenAI** for query and document embeddings
- **JSON-RPC 2.0** for MCP protocol implementation
- **Streaming JSON** (NDJSON) format for search responses

### MCP Implementation

- Strictly follows Model Context Protocol (MCP) specification
- Implements required components:
  - Base Protocol (JSON-RPC 2.0 message format)
  - Lifecycle Management (connection initialization, capability negotiation, session control)
- Implements stateful connections
- Implements server and client capability negotiation
- Implements MCP features:
  - Resources: For providing search results and metadata
  - Tools: For exposing search functionality to the AI model
- Implements proper lifecycle management

### MCP Utilities

- **Error Reporting**: Standard error handling and reporting as per MCP specification
- **Logging**: Basic logging for debugging and monitoring
- **Configuration**: Server configuration management

### Server Design Principles

- **Simplicity**: Focus on core search functionality without unnecessary complexity
- **Composability**: Design to work alongside other MCP servers without conflicts
- **Single Responsibility**: Handle only search and metadata retrieval, leaving other features to specialized servers
- **Clear Boundaries**: Maintain strict separation of concerns with other MCP servers

### Responsibilities

- Accepts raw natural language queries from Cursor through MCP protocol
- Embeds queries using OpenAI
- Performs filtered vector search using Qdrant
- Automatically infers intent and applies source-type filters
- Streams top-K contextually enriched results back to Cursor

### Query Inference

An internal module classifies queries to infer source type (e.g., "JIRA", "Confluence", etc.). Based on this, Qdrant filters are applied:

```json
{
  "must": [
    {"key": "source_type", "match": {"value": "confluence"}}
  ]
}
```

### Sample Streaming Response Format

```json
{
  "query": "How do I configure OAuth in our backend?",
  "results": [
    {
      "score": 0.89,
      "text": "To configure OAuth in the backend...",
      "source_type": "confluence",
      "source_title": "Authentication Architecture",
      "source_url": "https://confluence..."
    },
    {
      "score": 0.87,
      "text": "Our OAuth client is initialized in `auth.py`...",
      "source_type": "git",
      "file_path": "auth/auth.py",
      "repo_name": "backend-services"
    }
  ]
}
```

## Configuration

- **Qdrant Configuration**:
  - Server endpoint (local or cloud)
  - API key (for cloud instances)
- **OpenAI Configuration**:
  - API key
  - Embedding model settings
- **Server Configuration**:
  - Port and host settings
  - Logging preferences
  - Performance tuning parameters

## Authentication & Security

- No authentication for inbound requests to MCP server
- Uses **Qdrant API key** (stored in env vars) for outbound requests
- Optional: run server in a VPC with IP allowlisting
- Custom authentication strategies may be implemented as per MCP specification

## Deployment

- Each user runs their own local instance
- No multi-user scaling required
- Simple installation and configuration process

## Summarization

- **Handled by Cursor**
- MCP server focuses on retrieval only
- Optional future support for summarization via separate service

## Future Enhancements

- **Incremental Reindexing**: Detect changes in Git and reindex only modified files
- **Summarization Endpoint**: Add `/summarize` with OpenAI or local models
- **Query Analytics**: Logging and metrics for insights and debugging
- **Additional Embedding Models**: Support for more embedding models beyond text-embedding-3-small
- **Rate Limiting**: Implementation of request rate limiting
- **Caching**: Local caching for frequently accessed results
- **Server Isolation**: Implement strict conversation and server isolation as per MCP specifications
- **Versioning Strategy**: Develop approach for handling future MCP specification updates
- **Server Composability**: Define and implement patterns for seamless interaction with other MCP servers

## Next Steps

- [ ] Review and finalize architecture
- [ ] Build initial FastAPI skeleton with MCP protocol support
- [ ] Configure Qdrant & OpenAI integration
- [ ] Implement intent inference and search endpoints
- [ ] Add streaming and test with Cursor
- [ ] Implement proper MCP lifecycle management
- [ ] Add configuration management
- [ ] Create installation and setup documentation

---
This document serves as the foundation for implementation and can be iteratively improved as we progress.
