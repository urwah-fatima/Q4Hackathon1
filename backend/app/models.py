"""
Pydantic models for request/response schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    question: str = Field(..., min_length=1, description="The question to ask about the book content")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of relevant chunks to retrieve")


class Source(BaseModel):
    """A source reference from the book."""

    title: str = Field(..., description="Page/section title")
    url: str = Field(..., description="URL to the source page")
    chunk_index: int = Field(..., description="Chunk position within the page")
    score: float = Field(..., description="Relevance score (0-1)")
    text: str = Field(..., description="The chunk text content")


class ChatResponse(BaseModel):
    """Response from chat endpoint."""

    answer: str = Field(..., description="The generated answer")
    sources: list[Source] = Field(default_factory=list, description="Sources used to generate the answer")


class StreamEvent(BaseModel):
    """Server-Sent Event for streaming responses."""

    event: str = Field(..., description="Event type: 'token', 'sources', 'done', or 'error'")
    data: str = Field(..., description="Event data (token text, JSON sources, or error message)")


class HealthStatus(BaseModel):
    """Health check response for a single dependency."""

    status: str = Field(..., description="'healthy' or 'unhealthy'")
    message: Optional[str] = Field(default=None, description="Error message if unhealthy")


class HealthResponse(BaseModel):
    """Response from health endpoint."""

    status: str = Field(..., description="Overall status: 'healthy' or 'unhealthy'")
    version: str = Field(..., description="API version")
    dependencies: dict[str, HealthStatus] = Field(
        default_factory=dict,
        description="Health status of each dependency"
    )
