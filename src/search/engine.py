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

# Get logger for this module
logger = LoggingConfig.get_logger("src.search.engine")


class SearchEngine:
    """Search engine implementation using Qdrant."""

    def __init__(self):
        """Initialize the search engine."""
        self.client: Optional[QdrantClient] = None
        self.config: Optional[QdrantConfig] = None
        self.openai_client: Optional[AsyncOpenAI] = None
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

    async def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for text.

        Args:
            text: The text to get embedding for

        Returns:
            List[float]: The embedding vector
        """
        if self.openai_client is None:
            raise RuntimeError("OpenAI client not initialized")

        try:
            # Get embedding from OpenAI
            response = await self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error("Failed to get embedding", exc_info=True)
            raise

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
            if self.client is None or self.config is None:
                raise RuntimeError("Search engine not initialized")

            # Get embedding for query
            logger.debug("Generating embedding for query")
            embedding = await self._get_embedding(query)
            logger.debug("Embedding generated successfully", embedding_size=len(embedding))

            # Prepare search parameters
            search_params = {
                "query_vector": embedding,
                "limit": limit,
                "score_threshold": 0.3,
                "search_params": models.SearchParams(hnsw_ef=128, exact=False),
            }
            logger.debug("Search parameters prepared", search_params=search_params)

            # Execute search
            logger.debug("Executing Qdrant search")
            results = self.client.search(
                collection_name=self.config.collection_name,
                **search_params,
            )
            logger.info(
                "Search completed",
                result_count=len(results),
                first_result_score=results[0].score if results else None,
            )

            # Process results
            logger.debug("Processing search results")
            processed_results = []
            for result in results:
                try:
                    payload = result.payload or {}
                    metadata = payload.get("metadata", {}) or {}
                    processed_result = SearchResult(
                        score=result.score,
                        text=payload.get("content", ""),
                        source_type=payload.get("source_type", "unknown"),
                        source_title=metadata.get("title", ""),
                        source_url=metadata.get("url"),
                        file_path=metadata.get("file_path"),
                        repo_name=metadata.get("repository_name"),
                    )
                    processed_results.append(processed_result)
                    logger.debug(
                        "Result processed",
                        score=processed_result.score,
                        source_type=processed_result.source_type,
                    )
                except Exception as e:
                    logger.error("Error processing result", error=str(e), result=result)

            logger.info(
                "Search results processed successfully", processed_count=len(processed_results)
            )
            return processed_results

        except Exception as e:
            logger.error("Search failed", exc_info=True)
            raise
