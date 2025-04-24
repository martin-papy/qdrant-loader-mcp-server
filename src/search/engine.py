"""Search engine implementation using Qdrant."""

from typing import Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import ResponseHandlingException
import structlog

from ..config import QdrantConfig


class SearchEngine:
    """Search engine implementation using Qdrant."""

    def __init__(self):
        """Initialize the search engine."""
        self.client = None
        self.config = None
        self.logger = structlog.get_logger(__name__)

    async def initialize(self, config: QdrantConfig) -> None:
        """Initialize the search engine with configuration."""
        self.config = config
        try:
            self.client = QdrantClient(url=config.url)

            # Ensure collection exists
            collections = self.client.get_collections().collections
            if not any(c.name == config.collection_name for c in collections):
                self.client.create_collection(
                    collection_name=config.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # Default size for OpenAI embeddings
                        distance=models.Distance.COSINE,
                    ),
                )
            self.logger.info("Successfully connected to Qdrant", url=config.url)
        except Exception as e:
            self.logger.error(
                "Failed to connect to Qdrant server",
                error=str(e),
                url=config.url,
                hint="Make sure Qdrant is running and accessible at the configured URL",
            )
            raise RuntimeError(
                f"Failed to connect to Qdrant server at {config.url}. "
                "Please ensure Qdrant is running and accessible."
            ) from None  # Suppress the original exception

    async def cleanup(self) -> None:
        """Cleanup resources."""
        if self.client:
            self.client.close()
            self.client = None
