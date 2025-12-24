"""
FastAPI application for RAG-powered book Q&A.

Run with: uv run uvicorn app.main:app --reload
"""

import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from .config import settings
from .models import ChatRequest, ChatResponse, Source, HealthResponse, HealthStatus
from .retriever import retrieve, check_qdrant_health, check_cohere_health
from .agent import build_context, generate_answer, stream_answer, check_cohere_chat_health


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def format_sources(chunks: list[dict]) -> list[Source]:
    """
    Convert retrieval results to Source models.

    Args:
        chunks: Retrieved chunks with metadata

    Returns:
        List of Source objects
    """
    return [
        Source(
            title=chunk["title"],
            url=chunk["url"],
            chunk_index=chunk["chunk_index"],
            score=chunk["score"],
            text=chunk["text"][:500] + "..." if len(chunk["text"]) > 500 else chunk["text"],
        )
        for chunk in chunks
    ]


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Answer a question about the book content.

    Retrieves relevant chunks from the vector database,
    builds a context, and generates an answer using OpenAI.
    """
    # Validate question
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Retrieve relevant chunks
        chunks = retrieve(request.question, request.top_k)
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Retrieval service unavailable: {str(e)}"
        )

    if not chunks:
        return ChatResponse(
            answer=(
                "I appreciate your question! However, this doesn't seem to be covered in the "
                "Physical AI & Humanoid Robotics book.\n\n"
                "Aapka sawal shukriya! Lekin yeh topic is kitaab mein nahi hai.\n\n"
                "I'm trained to help with / Main in topics mein madad kar sakta hoon:\n"
                "• ROS 2 architecture\n"
                "• Gazebo simulation\n"
                "• NVIDIA Isaac Sim\n"
                "• Humanoid robots\n"
                "• SLAM & navigation\n\n"
                "Feel free to ask! / Koi bhi sawal poochein!"
            ),
            sources=[],
        )

    # Build context and generate answer
    context = build_context(chunks)

    try:
        answer = generate_answer(context, request.question)
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Generation service unavailable: {str(e)}"
        )

    # Check for low relevance - provide friendly response
    max_score = max(chunk["score"] for chunk in chunks)
    if max_score < settings.RELEVANCE_THRESHOLD:
        answer = (
            "I appreciate your question! However, this doesn't seem to be covered in the "
            "Physical AI & Humanoid Robotics book.\n\n"
            "Aapka sawal shukriya! Lekin yeh topic is kitaab mein nahi hai.\n\n"
            "I'm trained to help with / Main in topics mein madad kar sakta hoon:\n"
            "• ROS 2 architecture\n"
            "• Gazebo simulation\n"
            "• NVIDIA Isaac Sim\n"
            "• Humanoid robots\n"
            "• SLAM & navigation\n\n"
            "Feel free to ask! / Koi bhi sawal poochein!"
        )

    return ChatResponse(
        answer=answer,
        sources=format_sources(chunks),
    )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Stream answer tokens for a question about the book content.

    Uses Server-Sent Events (SSE) to stream the response.
    Final event includes sources.
    """
    # Validate question
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        # Retrieve relevant chunks
        chunks = retrieve(request.question, request.top_k)
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Retrieval service unavailable: {str(e)}"
        )

    if not chunks:
        async def no_results():
            yield f"data: {json.dumps({'event': 'token', 'data': 'I could not find any relevant information in the book for your question.'})}\n\n"
            yield f"data: {json.dumps({'event': 'sources', 'data': []})}\n\n"
            yield f"data: {json.dumps({'event': 'done', 'data': ''})}\n\n"

        return StreamingResponse(
            no_results(),
            media_type="text/event-stream",
        )

    # Build context
    context = build_context(chunks)
    sources = format_sources(chunks)

    async def generate():
        try:
            # Stream tokens
            for token in stream_answer(context, request.question):
                yield f"data: {json.dumps({'event': 'token', 'data': token})}\n\n"

            # Send sources
            sources_data = [s.model_dump() for s in sources]
            yield f"data: {json.dumps({'event': 'sources', 'data': sources_data})}\n\n"

            # Done event
            yield f"data: {json.dumps({'event': 'done', 'data': ''})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'event': 'error', 'data': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    """
    Check health of all dependencies.

    Returns status of Qdrant, Cohere, and OpenAI services.
    """
    dependencies = {}

    # Check Qdrant
    qdrant_healthy, qdrant_msg = check_qdrant_health()
    dependencies["qdrant"] = HealthStatus(
        status="healthy" if qdrant_healthy else "unhealthy",
        message=qdrant_msg if not qdrant_healthy else None,
    )

    # Check Cohere
    cohere_healthy, cohere_msg = check_cohere_health()
    dependencies["cohere"] = HealthStatus(
        status="healthy" if cohere_healthy else "unhealthy",
        message=cohere_msg if not cohere_healthy else None,
    )

    # Check Cohere Chat (for generation)
    cohere_chat_healthy, cohere_chat_msg = check_cohere_chat_health()
    dependencies["cohere_chat"] = HealthStatus(
        status="healthy" if cohere_chat_healthy else "unhealthy",
        message=cohere_chat_msg if not cohere_chat_healthy else None,
    )

    # Overall status
    all_healthy = all([qdrant_healthy, cohere_healthy, cohere_chat_healthy])

    return HealthResponse(
        status="healthy" if all_healthy else "unhealthy",
        version=settings.API_VERSION,
        dependencies=dependencies,
    )


@app.get("/")
async def root():
    """API root - redirect to docs."""
    return {
        "message": "Physical AI Book RAG API",
        "docs": "/docs",
        "health": "/health",
    }
