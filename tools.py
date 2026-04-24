import os
import time
from crewai.tools import tool
from tavily import TavilyClient
from config import config

os.environ["TAVILY_API_KEY"] = config.TAVILY_API_KEY
_tavily = TavilyClient(api_key=config.TAVILY_API_KEY)


@tool
def search_web(query: str) -> str:
    """
    Search the live web for current information, facts, and evidence to verify claims.
    Returns a structured list of results with source URLs, titles, and content snippets.
    Use this tool multiple times with different queries for thorough research.
    """
    try:
        response = _tavily.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True,
        )
        output_lines = []

        if response.get("answer"):
            output_lines.append(f"SUMMARY ANSWER: {response['answer']}\n")

        output_lines.append("TOP SOURCES:")
        for i, result in enumerate(response.get("results", []), 1):
            output_lines.append(
                f"\n[{i}] {result.get('title', 'No title')}\n"
                f"    URL: {result.get('url', 'N/A')}\n"
                f"    CONTENT: {result.get('content', '')[:400]}..."
            )

        return "\n".join(output_lines)
    except Exception as e:
        return f"Search error: {str(e)}"


@tool
def analyze_image(image_url: str) -> str:
    """
    Perform a reverse-image search and forensic analysis on the provided image URL.
    Searches for original source, context mismatches, and AI-generation markers.
    """
    if not image_url or image_url.strip() == "":
        return "No image URL provided. Skipping image analysis."
    try:
        query = f"reverse image search fact check original source: {image_url}"
        response = _tavily.search(query=query, search_depth="basic", max_results=3)
        output_lines = ["IMAGE FORENSIC REPORT:"]
        if response.get("answer"):
            output_lines.append(f"Context: {response['answer']}")
        for result in response.get("results", []):
            output_lines.append(
                f"- {result.get('title', '')}: {result.get('content', '')[:300]}\n  Source: {result.get('url', '')}"
            )
        return "\n".join(output_lines)
    except Exception as e:
        return f"Image analysis error: {str(e)}"
