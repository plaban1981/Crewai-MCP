from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
import requests
import base64
import logging
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("image_server")

# Initialize FastMCP server
mcp = FastMCP("image_server")

# Get current directory
current_dir = Path(__file__).parent
output_dir = current_dir / "images"
os.makedirs(output_dir, exist_ok=True)

# Validate API key
api_key = os.getenv("SEGMIND_API_KEY")
if not api_key:
    logger.error("SEGMIND_API_KEY environment variable is not set!")
    raise RuntimeError("Missing Segmind API key")

url = "https://api.segmind.com/v1/imagen-4"

@mcp.tool(name="image_creation_openai", description="Create an image using Segmind API")
def image_creation_openai(query: str, image_name: str) -> str:
    try:
        logger.info(f"Creating image for query: {query}")
        
        # Request payload
        data = {
            "prompt": f"Generate an image: {query}",
            "negative_prompt": "blurry, pixelated",
            "aspect_ratio": "4:3"
        }

        headers = {'x-api-key': os.getenv("SEGMIND_API_KEY")}

        # Add timeout and error handling
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {"success": False, "error": f"API request failed: {str(e)}"}

        # Save the image
        image_path = output_dir / f"{image_name}.jpeg"
        with open(image_path, "wb") as f:
            f.write(response.content)
            
        logger.info(f"Image saved to {image_path}")
        return {"success": True, "image_path": str(image_path)}
    except Exception as e:
        logger.exception("Image creation failed")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    logger.info("Starting Image Creation MCP Server")
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        logger.exception("Server crashed")
        # Add pause to see error in Windows
        input("Press Enter to exit...")
        raise