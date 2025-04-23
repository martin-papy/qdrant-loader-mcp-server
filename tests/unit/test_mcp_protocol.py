"""Unit tests for MCP protocol implementation."""

import pytest
from src.mcp import MCPHandler, MCPRequest, MCPResponse


@pytest.fixture
def mcp_handler():
    """Create MCP handler fixture."""
    return MCPHandler()


@pytest.fixture
def valid_request():
    """Create valid MCP request fixture."""
    return {
        "jsonrpc": "2.0",
        "method": "search",
        "params": {"query": "test query", "source_types": ["git"], "limit": 5},
        "id": 1,
    }


def test_mcp_handler_initialization(mcp_handler):
    """Test MCP handler initialization."""
    assert mcp_handler is not None


@pytest.mark.asyncio
async def test_handle_valid_request(mcp_handler, valid_request):
    """Test handling valid MCP request."""
    response = await mcp_handler.handle_request(valid_request)
    assert response is not None
    assert "jsonrpc" in response
    assert response["jsonrpc"] == "2.0"
    assert "id" in response
    assert response["id"] == 1
