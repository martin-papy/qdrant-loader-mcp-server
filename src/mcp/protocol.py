"""MCP Protocol implementation."""

from typing import Any, Dict, Optional


class MCPProtocol:
    """MCP Protocol implementation for handling RAG requests."""

    def __init__(self):
        """Initialize MCP Protocol."""
        self.version = "2.0"

    def validate_request(self, request: Dict[str, Any]) -> bool:
        """Validate MCP request format.

        Args:
            request: The request to validate

        Returns:
            bool: True if request is valid, False otherwise
        """
        required_fields = ["jsonrpc", "method", "params", "id"]
        return all(field in request for field in required_fields)

    def create_response(
        self, request_id: int, result: Optional[Any] = None, error: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Create MCP response.

        Args:
            request_id: The ID of the request
            result: The result of the request
            error: Any error that occurred

        Returns:
            Dict[str, Any]: The response object
        """
        response = {"jsonrpc": self.version, "id": request_id}

        if error is not None:
            response["error"] = error
        else:
            response["result"] = result

        return response
