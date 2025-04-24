"""MCP request and response models."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MCPRequest(BaseModel):
    """MCP request model."""

    jsonrpc: str = Field(..., description="JSON-RPC version")
    method: str = Field(..., description="Method to call")
    params: Dict[str, Any] = Field(..., description="Method parameters")
    id: int = Field(..., description="Request ID")


class MCPResponse(BaseModel):
    """MCP response model."""

    jsonrpc: str = Field(..., description="JSON-RPC version")
    id: int = Field(..., description="Request ID")
    result: Optional[Any] = Field(None, description="Result of the request")
    error: Optional[Dict[str, Any]] = Field(None, description="Error information")
