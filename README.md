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

4. Copy and configure the environment:

```bash
cp config/config.template.yaml config/config.yaml
# Edit config.yaml with your settings
```

## Configuration

The server is configured through `config/config.yaml`. You need to set:

- Qdrant connection details
- OpenAI API key
- Server settings
- Search parameters

## Usage

1. Start the server:

```bash
mcp-server
```

2. The server will be available at `http://localhost:8000`

3. Use the MCP protocol to interact with the server:

```python
import jsonrpcclient
from jsonrpcclient.clients.http_client import HTTPClient

client = HTTPClient("http://localhost:8000")
response = client.request(
    "search",
    {
        "query": "How do I configure OAuth?",
        "source_types": ["confluence", "git"],
        "limit": 5
    }
)
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/martin-papy/qdrant-loader-mcp-server.git
cd qdrant-loader-mcp-server

# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
.\venv\Scripts\activate  # On Windows

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src
```

## Documentation

- [Technical Specification](docs/TechnicalSpecification.md)
- [Testing Strategy](docs/TestingStrategy.md)
- [Coding Standards](docs/CodingStandards.md)
- [Client Usage](docs/ClientUsage.md)

## Contributing

We welcome contributions! Please:

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Relevant error messages

For code contributions:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description
4. Ensure all tests pass

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
