"""Search engine implementation using Qdrant."""

from typing import Dict, Any, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import ResponseHandlingException
import structlog
from openai import AsyncOpenAI

from ..config import QdrantConfig, OpenAIConfig
from ..utils import LoggingConfig
from .models import SearchResult
from .hybrid_search import HybridSearchEngine

# Get logger for this module
logger = LoggingConfig.get_logger("src.search.engine")


class SearchEngine:
    """Search engine implementation using Qdrant."""

    def __init__(self):
        """Initialize the search engine."""
        self.client: Optional[QdrantClient] = None
        self.config: Optional[QdrantConfig] = None
        self.openai_client: Optional[AsyncOpenAI] = None
        self.hybrid_search: Optional[HybridSearchEngine] = None
        self.logger = structlog.get_logger(__name__)

    async def initialize(self, config: QdrantConfig, openai_config: OpenAIConfig) -> None:
        """Initialize the search engine with configuration."""
        self.config = config
        try:
            self.client = QdrantClient(url=config.url, api_key=config.api_key)
            self.openai_client = AsyncOpenAI(api_key=openai_config.api_key)

            # Ensure collection exists
            if self.client is None:
                raise RuntimeError("Failed to initialize Qdrant client")

            collections = self.client.get_collections().collections
            if not any(c.name == config.collection_name for c in collections):
                self.client.create_collection(
                    collection_name=config.collection_name,
                    vectors_config=models.VectorParams(
                        size=1536,  # Default size for OpenAI embeddings
                        distance=models.Distance.COSINE,
                    ),
                )
                
            # Initialize hybrid search
            if self.client and self.openai_client:
                self.hybrid_search = HybridSearchEngine(
                    qdrant_client=self.client,
                    openai_client=self.openai_client,
                    collection_name=config.collection_name
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

    async def search(
        self,
        query: str,
        source_types: Optional[List[str]] = None,
        limit: int = 10,
    ) -> List[SearchResult]:
        """Search for relevant documents.

        Args:
            query: The search query
            source_types: Optional list of source types to filter by
            limit: Maximum number of results to return

        Returns:
            List[SearchResult]: List of search results
        """
        logger.debug("Starting search", query=query, source_types=source_types, limit=limit)

        try:
            if not self.hybrid_search:
                raise RuntimeError("Search engine not initialized")

            # Use hybrid search
            results = await self.hybrid_search.search(
                query=query,
                limit=limit,
                source_types=source_types
            )
            
            logger.info(
                "Search completed",
                result_count=len(results),
                first_result_score=results[0].score if results else None,
            )

            return results

        except Exception as e:
            logger.error("Search failed", exc_info=True)
            raise
