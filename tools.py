import time
from crewai.tools import tool

@tool
def search_web(query: str) -> str:
    """
    Search the web for current information, facts, and evidence.
    Use this tool when you need to verify a claim against public knowledge.
    """
    # Simulate network delay for the mock tool
    time.sleep(1.5)
    
    query_lower = query.lower()
    # Provide mocked responses based on simple keyword matching for demonstration
    if "moon landing" in query_lower and "faked" in query_lower:
        return "Multiple credible sources and historical records confirm the Apollo moon landings were real. There is no evidence they were faked."
    elif "eiffel tower" in query_lower and "sold" in query_lower:
        return "Victor Lustig famously conned people into 'buying' the Eiffel Tower in 1925, but it was a scam. The Eiffel Tower was never actually sold."
    elif "president" in query_lower and "2024" in query_lower:
        return "As of recent news, the 2024 presidential election details can be found on major news outlets. (Mock Data)"
    
    return f"Search results for '{query}': Found multiple articles discussing this topic, but no definitive fact-check was found. You may need to infer based on context."

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
