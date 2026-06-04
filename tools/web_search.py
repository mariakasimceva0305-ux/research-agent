"""
web_search - DuckDuckGo search tool. No API key required.
"""

from langchain_core.tools import tool
from ddgs import DDGS


@tool
def web_search(query: str) -> str:
    """
    Search the web for information on a given query.
    Args:
        query: search query string
    Returns:
        formatted search results with titles, URLs, and snippets
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return f"No results found for query: {query}"

        output = []
        for i, r in enumerate(results, 1):
            output.append(
                f"[{i}] {r.get('title', 'No title')}\n"
                f"URL: {r.get('href', '')}\n"
                f"{r.get('body', '')}"
            )
        return "\n\n".join(output)

    except Exception as e:
        return f"Search error: {str(e)}"
