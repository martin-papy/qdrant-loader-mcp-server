"""Main application entry point for RAG MCP Server."""

import asyncio
import logging
from typing import Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .mcp import MCPHandler
from .search import QueryProcessor, SearchEngine
from .utils import Config, setup_logging

logger = logging.getLogger(__name__)

app = FastAPI(title="RAG MCP Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
config = Config()
mcp_handler = MCPHandler()
query_processor = QueryProcessor()
search_engine = SearchEngine()


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    setup_logging(config.server.log_level)
    logger.info("Starting RAG MCP Server")
    await search_engine.initialize(config.qdrant)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down RAG MCP Server")
    await search_engine.cleanup()


@app.post("/mcp")
async def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP protocol requests."""
    try:
        response = await mcp_handler.handle_request(request)
        return response
    except Exception as e:
        logger.error(f"Error handling MCP request: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app", host=config.server.host, port=config.server.port, reload=True
    )
