import time
from crewai.tools import tool

from crewai_tools import TavilySearchTool
from config import config
import os

# Set API key for the tool
os.environ["TAVILY_API_KEY"] = config.TAVILY_API_KEY

# Initialize the real tool
tavily_tool = TavilySearchTool()

@tool
def search_web(query: str) -> str:
    """
    Search the web for current information, facts, and evidence using Tavily.
    Use this tool when you need to verify a claim against real-time public knowledge.
    """
    return tavily_tool._run(search_query=query)

@tool
def analyze_image(image_path_or_url: str) -> str:
    """
    Analyze an image to extract text, identify objects, and detect potential manipulation.
    Use this tool when the input includes an image that needs verification.
    """
    # Simulate processing time
    time.sleep(2)
    
    # Mock analysis based on string
    if "fake" in image_path_or_url.lower():
        return "Image Analysis Report: The image shows clear signs of digital manipulation around the edges of the main subject. Lighting shadows are inconsistent."
    
    return "Image Analysis Report: The image appears to be an unaltered photograph of a standard scene. No obvious signs of tampering detected."
