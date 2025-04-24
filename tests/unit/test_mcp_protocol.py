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
    assert mcp_handler.protocol is not None


@pytest.mark.asyncio
async def test_handle_valid_request(mcp_handler, valid_request):
    """Test handling valid MCP request."""
    response = await mcp_handler.handle_request(valid_request)
    assert response is not None
    assert "jsonrpc" in response
    assert response["jsonrpc"] == "2.0"
    assert "id" in response
    assert response["id"] == 1


@pytest.mark.asyncio
async def test_handle_invalid_request(mcp_handler):
    """Test handling invalid MCP request."""
    # Not a dict
    response = await mcp_handler.handle_request([])
    assert response is not None
    assert "jsonrpc" in response
    assert response["jsonrpc"] == "2.0"
    assert "error" in response
    assert response["error"]["code"] == -32600
    assert "Invalid Request" in response["error"]["message"]

    # Missing jsonrpc
    response = await mcp_handler.handle_request({"method": "search", "id": 1})
    assert response is not None
    assert "jsonrpc" in response
    assert response["jsonrpc"] == "2.0"
    assert "error" in response
    assert response["error"]["code"] == -32600
    assert "Invalid Request" in response["error"]["message"]

    # Wrong jsonrpc version
    response = await mcp_handler.handle_request({"jsonrpc": "1.0", "method": "search", "id": 1})
    assert response is not None
    assert "jsonrpc" in response
    assert response["jsonrpc"] == "2.0"
    assert "error" in response
    assert response["error"]["code"] == -32600
    assert "Invalid Request" in response["error"]["message"]

    # Missing method
    response = await mcp_handler.handle_request({"jsonrpc": "2.0", "id": 1})
    assert response is not None
    assert "jsonrpc" in response
    assert response["jsonrpc"] == "2.0"
    assert "error" in response
    assert response["error"]["code"] == -32600
    assert "Invalid Request" in response["error"]["message"]


@pytest.mark.asyncio
async def test_handle_initialize(mcp_handler):
    """Test handling initialize request."""
    request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"supportsListOfferings": True},
        },
        "id": 1,
    }
    response = await mcp_handler.handle_request(request)
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 1
    assert "result" in response
    assert response["result"]["protocolVersion"] == "2024-11-05"
    assert response["result"]["serverInfo"]["name"] == "Qdrant Loader MCP Server"
    assert response["result"]["capabilities"]["supportsListOfferings"] is True


@pytest.mark.asyncio
async def test_handle_list_offerings(mcp_handler):
    """Test handling list offerings request."""
    request = {"jsonrpc": "2.0", "method": "ListOfferings", "params": {}, "id": 2}
    response = await mcp_handler.handle_request(request)
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 2
    assert "result" in response
    assert "offerings" in response["result"]
    assert len(response["result"]["offerings"]) == 1
    offering = response["result"]["offerings"][0]
    assert offering["id"] == "qdrant-loader"
    assert offering["name"] == "Qdrant Loader"
    assert offering["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_handle_unknown_method(mcp_handler):
    """Test handling unknown method request."""
    request = {"jsonrpc": "2.0", "method": "UnknownMethod", "params": {}, "id": 3}
    response = await mcp_handler.handle_request(request)
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 3
    assert "error" in response
    assert response["error"]["code"] == -32601
    assert "Method not found" in response["error"]["message"]
    assert "UnknownMethod" in response["error"]["data"]


@pytest.mark.asyncio
async def test_handle_notification(mcp_handler):
    """Test handling notification request."""
    request = {"jsonrpc": "2.0", "method": "notify", "params": {"event": "test"}}
    response = await mcp_handler.handle_request(request)
    assert response == {}


@pytest.mark.asyncio
async def test_handle_request_with_exception(mcp_handler):
    """Test handling request that raises an exception."""

    # Mock a method that raises an exception
    async def _handle_initialize(*args, **kwargs):
        raise Exception("Test error")

    mcp_handler._handle_initialize = _handle_initialize

    request = {"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}
    response = await mcp_handler.handle_request(request)
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 1
    assert "error" in response
    assert response["error"]["code"] == -32603
    assert "Internal error" in response["error"]["message"]
    assert "Test error" in response["error"]["data"]
