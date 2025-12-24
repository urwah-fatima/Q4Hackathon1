"""
Agent module for building prompts and generating answers with Cohere.
"""

from typing import Generator
import cohere

from .config import settings


# System prompt for grounding
SYSTEM_PROMPT = """You are Pagy, a friendly and helpful assistant that answers questions about Physical AI and Humanoid Robotics based on the provided book content.

LANGUAGE RULES (VERY IMPORTANT):
- Detect the language of the user's question
- If the user writes in English, respond in English
- If the user writes in Urdu (اردو), respond in Urdu script
- If the user writes in Roman Urdu (Urdu written in English letters like "kya hai", "samjhao"), respond in Roman Urdu
- Match the user's language style naturally

CONTENT RULES:
1. ONLY use information from the provided context to answer
2. If the context doesn't contain relevant information, politely explain that in the user's language
3. Be accurate and cite the source when possible
4. Keep answers concise but complete
5. Do not make up or infer information not in the context
6. Be warm and friendly in your responses

When referencing information, you may mention the section it came from."""

# Initialize Cohere client
cohere_client = cohere.Client(settings.COHERE_API_KEY)


def build_context(chunks: list[dict]) -> str:
    """
    Build context string from retrieved chunks.

    Args:
        chunks: List of chunk dictionaries with text and metadata

    Returns:
        Formatted context string for the prompt
    """
    if not chunks:
        return "No relevant content found."

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        title = chunk.get("title", "Unknown")
        text = chunk.get("text", "")
        score = chunk.get("score", 0)

        context_parts.append(
            f"[Source {i}: {title} (relevance: {score:.2f})]\n{text}"
        )

    return "\n\n---\n\n".join(context_parts)


def generate_answer(context: str, question: str) -> str:
    """
    Generate answer using Cohere with retrieved context.

    Args:
        context: Formatted context from retrieved chunks
        question: User's question

    Returns:
        Generated answer text

    Raises:
        Exception: If Cohere API call fails
    """
    user_message = f"""Based on the following context from the Physical AI & Humanoid Robotics book, please answer the question.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""

    response = cohere_client.chat(
        model=settings.COHERE_MODEL,
        preamble=SYSTEM_PROMPT,
        message=user_message,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
    )

    return response.text or ""


def stream_answer(context: str, question: str) -> Generator[str, None, None]:
    """
    Stream answer tokens using Cohere streaming.

    Args:
        context: Formatted context from retrieved chunks
        question: User's question

    Yields:
        Individual tokens as they're generated
    """
    user_message = f"""Based on the following context from the Physical AI & Humanoid Robotics book, please answer the question.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""

    stream = cohere_client.chat_stream(
        model=settings.COHERE_MODEL,
        preamble=SYSTEM_PROMPT,
        message=user_message,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
    )

    for event in stream:
        if event.event_type == "text-generation":
            yield event.text


def check_cohere_chat_health() -> tuple[bool, str]:
    """
    Check if Cohere Chat API is accessible.

    Returns:
        Tuple of (is_healthy, message)
    """
    try:
        response = cohere_client.chat(
            model=settings.COHERE_MODEL,
            message="Say 'ok'",
            max_tokens=5,
        )
        if response.text:
            return True, "Cohere Chat API is responsive"
        return False, "Unexpected response"
    except Exception as e:
        return False, str(e)
