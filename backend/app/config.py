"""
Configuration settings loaded from environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings from environment."""

    # API Keys
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # Qdrant Collection
    COLLECTION_NAME: str = "book_chatbot_embedding"

    # Retrieval settings
    DEFAULT_TOP_K: int = 5
    RELEVANCE_THRESHOLD: float = 0.5

    # Cohere Chat settings
    COHERE_MODEL: str = "command-r-plus-08-2024"
    MAX_TOKENS: int = 1024
    TEMPERATURE: float = 0.3

    # API settings
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "Physical AI Book RAG API"
    API_DESCRIPTION: str = "RAG API for querying Physical AI & Humanoid Robotics book content"


settings = Settings()
