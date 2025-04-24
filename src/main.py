"""Main application entry point for RAG MCP Server."""

import os
import sys
import signal
import asyncio
import json
import logging
from typing import Dict, Any, NoReturn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from uvicorn.config import Config as UvicornConfig
from uvicorn.server import Server, ServerState

from .mcp import MCPHandler
from .utils import LoggingConfig
from .config import Config
from .search.engine import SearchEngine
from .search.processor import QueryProcessor

# Initialize logging first
LoggingConfig.setup(level="DEBUG")
logger = LoggingConfig.get_logger("src.main")  # Use proper module name
logger.info("Initializing MCP Qdrant Loader")

# Initialize components
config = Config()
mcp_handler = MCPHandler()
query_processor = QueryProcessor()
search_engine = SearchEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    logger.info("Starting MCP Qdrant Loader")
    try:
        await search_engine.initialize(config.qdrant)
    except RuntimeError as e:
        logger.error("Failed to initialize search engine", error=str(e))
        logger.error(
            "Server cannot start without Qdrant connection. "
            "Please ensure Qdrant is running and try again."
        )
        # Exit immediately without traceback
        os._exit(1)

    yield

    # Shutdown
    logger.info("Shutting down MCP Qdrant Loader")
    await search_engine.cleanup()


app = FastAPI(title="MCP Qdrant Loader", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def read_stdin():
    """Read from stdin non-blockingly."""
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return reader


async def shutdown(loop: asyncio.AbstractEventLoop):
    """Handle graceful shutdown."""
    logger.info("Shutting down...")

    # Get all tasks except the current one
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    # Cancel all tasks
    for task in tasks:
        task.cancel()

    # Wait for all tasks to complete
    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

    # Stop the event loop
    loop.stop()


def main():
    """Main entry point for the application."""
    # Suppress asyncio debug messages
    logging.getLogger("asyncio").setLevel(logging.WARNING)

    logger.debug("Starting main function...")
    try:
        # Create and set the event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Set up signal handlers
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(loop)))

        # Run the stdio handler
        logger.debug("Running stdio handler...")
        loop.run_until_complete(handle_stdio())
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise
    finally:
        logger.debug("Cleaning up...")
        try:
            # Cancel all remaining tasks
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()

            # Run the loop until all tasks are done
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        except Exception as e:
            logger.error(f"Error during final cleanup: {e}")
        finally:
            loop.close()


async def handle_stdio():
    """Handle stdio communication with Cursor."""
    reader = await read_stdin()
    logger.info("Server ready to handle requests")

    while True:
        try:
            # Read a line from stdin
            logger.debug("Waiting for input...")
            line = await reader.readline()
            if not line:
                logger.info("No input received, breaking")
                break

            # Parse the request
            try:
                request = json.loads(line.decode())
            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
                # Send error response for invalid JSON
                response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error",
                        "data": "Invalid JSON received",
                    },
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                continue

            # Validate request format
            if not isinstance(request, dict):
                logger.error("Request must be a JSON object")
                response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request",
                        "data": "Request must be a JSON object",
                    },
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                continue

            if "jsonrpc" not in request or request["jsonrpc"] != "2.0":
                logger.error("Invalid JSON-RPC version")
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request",
                        "data": "Invalid JSON-RPC version",
                    },
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                continue

            if "method" not in request:
                logger.error("Missing method in request")
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request",
                        "data": "Missing method in request",
                    },
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
                continue

            # Handle the request
            response = await mcp_handler.handle_request(request)

            # Write the response to stdout
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except asyncio.CancelledError:
            logger.info("Received shutdown signal")
            break
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            continue


if __name__ == "__main__":
    main()
