# RAG MCP Server for Cursor

A Retrieval-Augmented Generation (RAG) Model Context Protocol (MCP) server that integrates with Cursor. It uses data ingested by `qdrant-loader` and stored in a Qdrant DB to provide contextually relevant information to Cursor.

## Features

- Implements Model Context Protocol (MCP) for Cursor integration
- Provides semantic search across multiple data sources
- Supports streaming responses
- Handles natural language queries
- Integrates with Qdrant vector database
- Uses OpenAI embeddings for semantic search

## Requirements

- Python 3.12+
- Qdrant instance (local or cloud)
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/martin-papy/qdrant-loader-mcp-server.git
cd qdrant-loader-mcp-server
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -e ".[dev]"  # Install with development dependencies
```

4. Set up environment variables:

```bash
export QDRANT_URL="your_qdrant_url"
export QDRANT_API_KEY="your_qdrant_api_key"
export OPENAI_API_KEY="your_openai_api_key"
```

## Configuration

The server is configured through environment variables:

- `QDRANT_URL`: URL of your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant
- `OPENAI_API_KEY`: OpenAI API key
- `SERVER_HOST`: (optional) Server host, defaults to "localhost"
- `SERVER_PORT`: (optional) Server port, defaults to 8000

## Usage

1. Start the server:

```
