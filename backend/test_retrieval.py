"""
Retrieval Testing CLI for Physical AI & Humanoid Robotics Book

This script provides a CLI for testing retrieval quality from the Qdrant vector database.

Usage:
    uv run test_retrieval.py test              # Run predefined test queries
    uv run test_retrieval.py query "question"  # Run a single query
    uv run test_retrieval.py interactive       # Interactive REPL mode
"""

import os
from typing import Optional

import cohere
import typer
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Load environment variables
load_dotenv()

# Configuration constants
COLLECTION_NAME = "book_chatbot_embedding"
DEFAULT_TOP_K = 5
RELEVANCE_THRESHOLD = 0.5  # Below this score, warn about low relevance

# Initialize clients
cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# Initialize Typer app and Rich console
app = typer.Typer(
    name="test_retrieval",
    help="RAG Retrieval Testing CLI for the Physical AI & Humanoid Robotics Book",
    add_completion=False,
)
console = Console()

# Predefined test queries covering book topics
TEST_QUERIES = [
    "What is ROS 2 and how does it work?",
    "How do humanoid robots maintain balance?",
    "What is URDF and how is it used for robot modeling?",
    "Explain reinforcement learning for robotics",
    "How does NVIDIA Isaac Sim work for robot simulation?",
    "What is visual SLAM and how do robots use it for navigation?",
    "How do you deploy AI models on edge devices for robotics?",
    "What are the key differences between Gazebo and Unity for simulation?",
]


def check_collection_exists() -> bool:
    """
    Check if the book collection exists in Qdrant.

    Returns:
        True if collection exists, False otherwise
    """
    try:
        collections = qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]
        return COLLECTION_NAME in collection_names
    except Exception as e:
        console.print(f"[red]Error connecting to Qdrant: {e}[/red]")
        return False


def embed_query(text: str) -> Optional[list[float]]:
    """
    Generate embedding for a query using Cohere.

    Uses input_type="search_query" for optimal retrieval.

    Args:
        text: Query text to embed

    Returns:
        Embedding vector or None on error
    """
    try:
        response = cohere_client.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_query",
        )
        return response.embeddings[0]
    except cohere.errors.TooManyRequestsError:
        console.print("[yellow]Rate limited by Cohere. Please wait and try again.[/yellow]")
        return None
    except Exception as e:
        console.print(f"[red]Cohere API error: {e}[/red]")
        return None


def search_qdrant(query_vector: list[float], top_k: int = DEFAULT_TOP_K) -> list:
    """
    Search Qdrant for similar vectors.

    Args:
        query_vector: Query embedding vector
        top_k: Number of results to return

    Returns:
        List of search results with payloads
    """
    try:
        results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k,
        )
        return results
    except Exception as e:
        console.print(f"[red]Qdrant search error: {e}[/red]")
        return []


def format_result(result, rank: int, threshold: float = RELEVANCE_THRESHOLD) -> Panel:
    """
    Format a search result for pretty terminal output.

    Args:
        result: Qdrant search result
        rank: Result ranking (1-based)
        threshold: Score threshold for relevance warning

    Returns:
        Rich Panel with formatted result
    """
    score = result.score
    title = result.payload.get("title", "Unknown")
    url = result.payload.get("url", "N/A")
    text = result.payload.get("text", "")
    chunk_index = result.payload.get("chunk_index", 0)

    # Truncate text if too long
    if len(text) > 300:
        text = text[:300] + "..."

    # Color based on score
    if score >= 0.7:
        score_color = "green"
    elif score >= threshold:
        score_color = "yellow"
    else:
        score_color = "red"

    # Build content
    content = f"[bold]Score:[/bold] [{score_color}]{score:.4f}[/{score_color}]"
    if score < threshold:
        content += " [red]⚠️ Low relevance[/red]"
    content += f"\n[bold]Title:[/bold] {title}"
    content += f"\n[bold]URL:[/bold] {url}"
    content += f"\n[bold]Chunk:[/bold] {chunk_index}"
    content += f"\n\n[dim]{text}[/dim]"

    return Panel(content, title=f"Result #{rank}", border_style="blue")


def run_single_query(
    query_text: str,
    top_k: int = DEFAULT_TOP_K,
    threshold: float = RELEVANCE_THRESHOLD,
) -> bool:
    """
    Run a single query and display results.

    Args:
        query_text: The query to search for
        top_k: Number of results to return
        threshold: Score threshold for relevance warning

    Returns:
        True if results found, False otherwise
    """
    console.print(f"\n[bold cyan]Query:[/bold cyan] {query_text}")
    console.print("-" * 60)

    # Embed query
    query_vector = embed_query(query_text)
    if query_vector is None:
        return False

    # Search Qdrant
    results = search_qdrant(query_vector, top_k)

    if not results:
        console.print("[yellow]No results found for this query.[/yellow]")
        return False

    # Display results
    for i, result in enumerate(results, 1):
        console.print(format_result(result, i, threshold))

    return True


@app.command()
def test(
    top_k: int = typer.Option(DEFAULT_TOP_K, "--top-k", "-k", help="Number of results per query"),
    threshold: float = typer.Option(RELEVANCE_THRESHOLD, "--threshold", "-t", help="Relevance score threshold"),
):
    """
    Run predefined test queries to evaluate retrieval quality.
    """
    console.print(Panel.fit(
        "[bold]RAG Retrieval Test Suite[/bold]\n"
        f"Collection: {COLLECTION_NAME}\n"
        f"Test queries: {len(TEST_QUERIES)}\n"
        f"Top-K: {top_k}",
        border_style="green",
    ))

    # Check collection exists
    if not check_collection_exists():
        console.print(f"[red]Collection '{COLLECTION_NAME}' not found. Run ingestion first.[/red]")
        raise typer.Exit(1)

    # Run all test queries
    success_count = 0
    for query in TEST_QUERIES:
        if run_single_query(query, top_k, threshold):
            success_count += 1
        console.print()

    # Summary
    console.print(Panel.fit(
        f"[bold]Test Summary[/bold]\n"
        f"Queries run: {len(TEST_QUERIES)}\n"
        f"Successful: {success_count}\n"
        f"Failed: {len(TEST_QUERIES) - success_count}",
        border_style="green" if success_count == len(TEST_QUERIES) else "yellow",
    ))


@app.command()
def query(
    text: str = typer.Argument(..., help="Query text to search for"),
    top_k: int = typer.Option(DEFAULT_TOP_K, "--top-k", "-k", help="Number of results to return"),
    threshold: float = typer.Option(RELEVANCE_THRESHOLD, "--threshold", "-t", help="Relevance score threshold"),
):
    """
    Run a single query and display results.
    """
    # Check collection exists
    if not check_collection_exists():
        console.print(f"[red]Collection '{COLLECTION_NAME}' not found. Run ingestion first.[/red]")
        raise typer.Exit(1)

    run_single_query(text, top_k, threshold)


@app.command()
def interactive(
    top_k: int = typer.Option(DEFAULT_TOP_K, "--top-k", "-k", help="Number of results per query"),
    threshold: float = typer.Option(RELEVANCE_THRESHOLD, "--threshold", "-t", help="Relevance score threshold"),
):
    """
    Interactive REPL mode for testing queries.
    """
    console.print(Panel.fit(
        "[bold]Interactive Query Mode[/bold]\n"
        f"Collection: {COLLECTION_NAME}\n"
        f"Top-K: {top_k}\n"
        "Type 'quit' or 'exit' to stop",
        border_style="cyan",
    ))

    # Check collection exists
    if not check_collection_exists():
        console.print(f"[red]Collection '{COLLECTION_NAME}' not found. Run ingestion first.[/red]")
        raise typer.Exit(1)

    while True:
        try:
            query_text = console.input("\n[bold green]Enter query (or 'quit' to exit):[/bold green] ")
            query_text = query_text.strip()

            if query_text.lower() in ("quit", "exit", "q"):
                console.print("[cyan]Goodbye![/cyan]")
                break

            if not query_text:
                console.print("[yellow]Please enter a query.[/yellow]")
                continue

            run_single_query(query_text, top_k, threshold)

        except KeyboardInterrupt:
            console.print("\n[cyan]Goodbye![/cyan]")
            break


@app.command()
def stats():
    """
    Display collection statistics.
    """
    # Check collection exists
    if not check_collection_exists():
        console.print(f"[red]Collection '{COLLECTION_NAME}' not found. Run ingestion first.[/red]")
        raise typer.Exit(1)

    try:
        info = qdrant_client.get_collection(COLLECTION_NAME)

        table = Table(title=f"Collection: {COLLECTION_NAME}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Points Count", str(info.points_count))
        table.add_row("Vectors Count", str(info.vectors_count))
        table.add_row("Status", str(info.status))

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error getting collection stats: {e}[/red]")


if __name__ == "__main__":
    app()
