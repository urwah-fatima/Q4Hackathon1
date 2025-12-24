"""
Retriever module for embedding queries and searching Qdrant.
"""

import cohere
from qdrant_client import QdrantClient

from .config import settings


# Initialize clients
cohere_client = cohere.Client(settings.COHERE_API_KEY)
qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)


def embed_query(text: str) -> list[float]:
    """
    Generate embedding for a query using Cohere.

    Uses input_type="search_query" for optimal retrieval performance.

    Args:
        text: Query text to embed

    Returns:
        1024-dimensional embedding vector

    Raises:
        Exception: If Cohere API call fails
    """
    response = cohere_client.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_query",
    )
    return response.embeddings[0]


def search_qdrant(query_vector: list[float], top_k: int = 5) -> list[dict]:
    """
    Search Qdrant for similar vectors.

    Args:
        query_vector: Query embedding vector
        top_k: Number of results to return

    Returns:
        List of results with score and payload

    Raises:
        Exception: If Qdrant search fails
    """
    results = qdrant_client.query_points(
        collection_name=settings.COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    )

    return [
        {
            "score": hit.score,
            "title": hit.payload.get("title", "Unknown"),
            "url": hit.payload.get("url", ""),
            "chunk_index": hit.payload.get("chunk_index", 0),
            "text": hit.payload.get("text", ""),
        }
        for hit in results.points
    ]


def retrieve(question: str, top_k: int = 5) -> list[dict]:
    """
    Full retrieval pipeline: embed query and search Qdrant.

    Args:
        question: User's question
        top_k: Number of results to return

    Returns:
        List of relevant chunks with metadata
    """
    query_vector = embed_query(question)
    results = search_qdrant(query_vector, top_k)
    return results


def check_qdrant_health() -> tuple[bool, str]:
    """
    Check if Qdrant is accessible and collection exists.

    Returns:
        Tuple of (is_healthy, message)
    """
    try:
        collections = qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]

        if settings.COLLECTION_NAME not in collection_names:
            return False, f"Collection '{settings.COLLECTION_NAME}' not found"

        info = qdrant_client.get_collection(settings.COLLECTION_NAME)
        return True, f"Collection has {info.points_count} points"
    except Exception as e:
        return False, str(e)


def check_cohere_health() -> tuple[bool, str]:
    """
    Check if Cohere API is accessible.

    Returns:
        Tuple of (is_healthy, message)
    """
    try:
        # Simple embed test
        response = cohere_client.embed(
            texts=["health check"],
            model="embed-english-v3.0",
            input_type="search_query",
        )
        if response.embeddings and len(response.embeddings[0]) == 1024:
            return True, "Cohere API is responsive"
        return False, "Unexpected embedding response"
    except Exception as e:
        return False, str(e)
