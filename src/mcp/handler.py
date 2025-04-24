"""MCP Handler implementation."""

from typing import Any, Dict, Optional, Union

from .protocol import MCPProtocol


class MCPHandler:
    """MCP Handler for processing RAG requests."""

    def __init__(self):
        """Initialize MCP Handler."""
        self.protocol = MCPProtocol()

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP request.

        Args:
            request: The request to handle

        Returns:
            Dict[str, Any]: The response
        """
        # Handle non-dict requests
        if not isinstance(request, dict):
            return {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32600,
                    "message": "Invalid Request",
                    "data": "The request is not a valid JSON-RPC 2.0 request",
                },
            }

        # Validate request format
        if not self.protocol.validate_request(request):
            # For invalid requests, we need to determine if we can extract an ID
            request_id = request.get("id")
            if request_id is None or not isinstance(request_id, (str, int)):
                request_id = None
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32600,
                    "message": "Invalid Request",
                    "data": "The request is not a valid JSON-RPC 2.0 request",
                },
            }

        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "ListOfferings":
                return await self._handle_list_offerings(request_id, params)
            elif method == "initialize":
                return await self._handle_initialize(request_id, params)
            else:
                return self.protocol.create_response(
                    request_id,
                    error={
                        "code": -32601,
                        "message": "Method not found",
                        "data": f"Method '{method}' not found",
                    },
                )
        except Exception as e:
            return self.protocol.create_response(
                request_id, error={"code": -32603, "message": "Internal error", "data": str(e)}
            )

    async def _handle_initialize(
        self, request_id: Optional[Union[str, int]], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle initialize request.

        Args:
            request_id: The ID of the request
            params: The parameters of the request

        Returns:
            Dict[str, Any]: The response
        """
        return self.protocol.create_response(
            request_id,
            result={
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "Qdrant Loader MCP Server", "version": "1.0.0"},
                "capabilities": {"supportsListOfferings": True},
            },
        )

    async def _handle_list_offerings(
        self, request_id: Optional[Union[str, int]], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle list offerings request.

        Args:
            request_id: The ID of the request
            params: The parameters of the request

        Returns:
            Dict[str, Any]: The response
        """
        return self.protocol.create_response(
            request_id,
            result={
                "offerings": [
                    {
                        "id": "qdrant-loader",
                        "name": "Qdrant Loader",
                        "description": "Load data into Qdrant vector database",
                        "version": "1.0.0",
                    }
                ]
            },
        )
