from typing import Any, Dict, List
import requests
from mcp.server.fastmcp import FastMCP
import os
import logging
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("search_server")

# Initialize FastMCP server
mcp = FastMCP("search_server")

# Get current directory
current_dir = Path(__file__).parent
results_dir = current_dir / "search_results"
os.makedirs(results_dir, exist_ok=True)

# Validate API key
api_key = os.getenv("BRAVE_API_KEY")
if not api_key:
    logger.warning("BRAVE_API_KEY environment variable is not set!")
    logger.warning("Search functionality will be limited or unavailable")

# Brave Search API endpoint
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

@mcp.tool(name="brave_search", description="Search the web using Brave Search API")
def brave_search(query: str, count: int = 10) -> Dict[str, Any]:
    """
    Search the web using Brave Search API
    
    Args:
        query: Search query string
        count: Number of results to return (max 20)
    
    Returns:
        Dictionary containing search results
    """
    try:
        logger.info(f"Searching for: {query}")
        
        if not api_key:
            return {
                "success": False, 
                "error": "BRAVE_API_KEY not configured",
                "results": []
            }
        
        # Limit count to reasonable range
        count = max(1, min(count, 20))
        
        # Request headers
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key
        }
        
        # Request parameters
        params = {
            "q": query,
            "count": count,
            "search_lang": "en",
            "country": "US",
            "safesearch": "moderate",
            "freshness": "pw",  # Past week for more recent results
            "text_decorations": False,
            "spellcheck": True
        }
        
        # Make API request
        try:
            response = requests.get(
                BRAVE_SEARCH_URL,
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Search API request failed: {e}")
            return {
                "success": False,
                "error": f"Search API request failed: {str(e)}",
                "results": []
            }
        
        # Parse response
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse search response: {e}")
            return {
                "success": False,
                "error": "Failed to parse search response",
                "results": []
            }
        
        # Extract and format results
        search_results = []
        web_results = data.get("web", {}).get("results", [])
        
        for result in web_results:
            search_result = {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("description", ""),
                "published": result.get("published", ""),
                "thumbnail": result.get("thumbnail", {}).get("src", "") if result.get("thumbnail") else ""
            }
            search_results.append(search_result)
        
        # Save results to file for reference
        try:
            results_file = results_dir / f"search_{query.replace(' ', '_')[:50]}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "query": query,
                    "timestamp": data.get("query", {}).get("posted_at", ""),
                    "results": search_results
                }, f, indent=2, ensure_ascii=False)
            logger.info(f"Search results saved to {results_file}")
        except Exception as e:
            logger.warning(f"Failed to save search results: {e}")
        
        logger.info(f"Found {len(search_results)} search results")
        
        return {
            "success": True,
            "query": query,
            "total_results": len(search_results),
            "results": search_results
        }
        
    except Exception as e:
        logger.exception("Search operation failed")
        return {
            "success": False,
            "error": str(e),
            "results": []
        }

@mcp.tool(name="search_news", description="Search for news using Brave Search API")
def search_news(query: str, count: int = 5) -> Dict[str, Any]:
    """
    Search for news using Brave Search API
    
    Args:
        query: Search query string
        count: Number of news results to return (max 20)
    
    Returns:
        Dictionary containing news search results
    """
    try:
        logger.info(f"Searching news for: {query}")
        
        if not api_key:
            return {
                "success": False,
                "error": "BRAVE_API_KEY not configured",
                "results": []
            }
        
        # Limit count to reasonable range
        count = max(1, min(count, 20))
        
        # Request headers
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip", 
            "X-Subscription-Token": api_key
        }
        
        # Request parameters for news search
        params = {
            "q": query,
            "count": count,
            "search_lang": "en",
            "country": "US",
            "safesearch": "moderate",
            "freshness": "pd",  # Past day for latest news
            "text_decorations": False,
            "result_filter": "news"  # Focus on news results
        }
        
        # Make API request
        try:
            response = requests.get(
                BRAVE_SEARCH_URL,
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"News search API request failed: {e}")
            return {
                "success": False,
                "error": f"News search API request failed: {str(e)}",
                "results": []
            }
        
        # Parse response
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse news search response: {e}")
            return {
                "success": False,
                "error": "Failed to parse news search response",
                "results": []
            }
        
        # Extract news results
        news_results = []
        
        # Check for news section in response
        news_data = data.get("news", {}).get("results", [])
        if not news_data:
            # Fallback to web results if no dedicated news section
            news_data = data.get("web", {}).get("results", [])
        
        for result in news_data:
            news_result = {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("description", ""),
                "published": result.get("age", result.get("published", "")),
                "source": result.get("profile", {}).get("name", "") if result.get("profile") else "",
                "thumbnail": result.get("thumbnail", {}).get("src", "") if result.get("thumbnail") else ""
            }
            news_results.append(news_result)
        
        logger.info(f"Found {len(news_results)} news results")
        
        return {
            "success": True,
            "query": query,
            "total_results": len(news_results),
            "results": news_results
        }
        
    except Exception as e:
        logger.exception("News search operation failed")
        return {
            "success": False,
            "error": str(e),
            "results": []
        }

if __name__ == "__main__":
    logger.info("Starting Brave Search MCP Server")
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        logger.exception("Search server crashed")
        # Add pause to see error in Windows
        input("Press Enter to exit...")
        raise 