"""Test script for Qdrant hybrid search capabilities."""

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from openai import AsyncOpenAI
import asyncio
import os
import logging
from typing import List, Optional

from src.search.hybrid_search import HybridSearchEngine
from src.search.models import SearchResult

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def test_search_queries(
    hybrid_search: HybridSearchEngine,
    queries: List[str],
    source_types: Optional[List[str]] = None,
    limit: int = 5
) -> None:
    """Test search with multiple queries.
    
    Args:
        hybrid_search: The hybrid search engine instance
        queries: List of search queries to test
        source_types: Optional list of source types to filter by
        limit: Maximum number of results per query
    """
    for query in queries:
        logger.info(f"\nTesting query: {query}")
        try:
            results = await hybrid_search.search(
                query=query,
                limit=limit,
                source_types=source_types
            )
            
            logger.info(f"Found {len(results)} results")
            
            for i, result in enumerate(results, 1):
                print(f"\nResult {i}:")
                print(f"Score (combined): {result.score:.3f}")
                print(f"Source Type: {result.source_type}")
                print(f"Title: {result.source_title}")
                if result.source_url:
                    print(f"URL: {result.source_url}")
                if result.file_path:
                    print(f"File: {result.file_path}")
                print(f"\nContent snippet: {result.text[:200]}...")
                
        except Exception as e:
            logger.error(f"Error searching for query '{query}': {str(e)}")

async def main():
    """Main test function."""
    logger.info("Starting hybrid search test")

    # Load environment variables
    logger.info("Loading environment variables")
    load_dotenv()

    # Validate environment variables
    required_vars = ["QDRANT_URL", "QDRANT_API_KEY", "OPENAI_API_KEY", "QDRANT_COLLECTION_NAME"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return

    try:
        # Initialize clients
        logger.info("Initializing Qdrant client")
        qdrant = QdrantClient(
            url=os.environ["QDRANT_URL"],
            api_key=os.environ["QDRANT_API_KEY"],
        )

        logger.info("Initializing OpenAI client")
        openai = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

        # Initialize hybrid search
        logger.info("Initializing hybrid search engine")
        hybrid_search = HybridSearchEngine(
            qdrant_client=qdrant,
            openai_client=openai,
            collection_name=os.environ["QDRANT_COLLECTION_NAME"]
        )

        # Test queries for different scenarios
        test_scenarios = [
            {
                "name": "Basic Product Requirements Search",
                "queries": [
                    "What are the Product Requirements of our application?",
                    "Show me the main features in our PRD"
                ]
            },
            {
                "name": "Architecture Search",
                "queries": [
                    "How is the system architecture designed?",
                    "What are the main components of our technical design?"
                ]
            },
            {
                "name": "API Documentation Search",
                "queries": [
                    "Show me the API endpoints documentation",
                    "How to use our REST API?"
                ]
            },
            {
                "name": "Source-Specific Search (Git)",
                "queries": [
                    "Show me the implementation of the search functionality"
                ],
                "source_types": ["git"]
            },
            {
                "name": "Source-Specific Search (Confluence)",
                "queries": [
                    "What are our coding standards?"
                ],
                "source_types": ["confluence"]
            }
        ]

        # Run test scenarios
        for scenario in test_scenarios:
            logger.info(f"\n=== Testing Scenario: {scenario['name']} ===")
            await test_search_queries(
                hybrid_search=hybrid_search,
                queries=scenario["queries"],
                source_types=scenario.get("source_types"),
                limit=5
            )

    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
    finally:
        logger.info("Test completed")

if __name__ == "__main__":
    logger.info("Starting script execution")
    asyncio.run(main())
    logger.info("Script execution completed")
