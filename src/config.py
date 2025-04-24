"""Configuration settings for the RAG MCP Server."""

from pydantic import BaseModel
from typing import Optional


class ServerConfig(BaseModel):
    """Server configuration settings."""

    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"


class QdrantConfig(BaseModel):
    """Qdrant configuration settings."""

    url: str = "http://localhost:6333"
    collection_name: str = "documents"


class Config(BaseModel):
    """Main configuration class."""

    server: ServerConfig = ServerConfig()
    qdrant: QdrantConfig = QdrantConfig()
