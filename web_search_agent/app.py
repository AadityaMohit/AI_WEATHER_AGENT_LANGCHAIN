import os
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

# Load environment variables from parent directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# Get API keys from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # Optional: for better search results

if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

# Set GOOGLE_API_KEY in environment for LangChain to use
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

@tool
def search_web(query: str, num_results: int = 5) -> str:
    """
    Search the web for information. Returns search results with titles, snippets, and URLs.
    
    Args:
        query: The search query
        num_results: Number of results to return (default: 5, max: 10)
    
    Returns:
        Formatted string with search results including titles, snippets, and URLs
    """
    try:
        # Limit results
        num_results = min(num_results, 10)
        
        # Use Serper API if available, otherwise use DuckDuckGo
        if SERPER_API_KEY:
            return _search_with_serper(query, num_results)
        else:
            return _search_with_duckduckgo(query, num_results)
    
    except Exception as e:
        return f"Error searching web: {str(e)}"

def _search_with_serper(query: str, num_results: int) -> str:
    """Search using Serper API (more accurate, requires API key)"""
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": num_results
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        if "organic" in data:
            for item in data["organic"][:num_results]:
                title = item.get("title", "No title")
                snippet = item.get("snippet", "No description")
                link = item.get("link", "")
                results.append(f"Title: {title}\nSnippet: {snippet}\nURL: {link}\n")
        
        if results:
            return f"Search results for '{query}':\n\n" + "\n".join(results)
        else:
            return f"No results found for '{query}'"
    
    except Exception as e:
        return f"Error with Serper API: {str(e)}. Falling back to DuckDuckGo."

def _search_with_duckduckgo(query: str, num_results: int) -> str:
    """Search using DuckDuckGo (free, no API key required)"""
    try:
        # Simple DuckDuckGo search using their instant answer API
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        
        # Get abstract if available
        if data.get("AbstractText"):
            results.append(f"Summary: {data['AbstractText']}\nSource: {data.get('AbstractURL', 'N/A')}\n")
        
        # Get related topics
        if data.get("RelatedTopics"):
            for topic in data["RelatedTopics"][:num_results]:
                if isinstance(topic, dict) and "Text" in topic:
                    results.append(f"Related: {topic['Text']}\nURL: {topic.get('FirstURL', 'N/A')}\n")
        
        if results:
            return f"Search results for '{query}':\n\n" + "\n".join(results)
        else:
            # Fallback: Use a simple web scraping approach or return message
            return f"Search query: '{query}'\n\nNote: For better results, consider using Serper API. Add SERPER_API_KEY to your .env file.\nYou can get a free API key at https://serper.dev"
    
    except Exception as e:
        return f"Error with DuckDuckGo search: {str(e)}"

# Initialize Gemini model
chat = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Define tools
tools = [search_web]

# Create agent graph
agent_graph = create_agent(
    model=chat,
    tools=tools,
    debug=True
)

if __name__ == "__main__":
    # Example usage
    print("Web Search Agent is ready!")
    print("Example queries:")
    print("- 'Search for latest AI news'")
    print("- 'Find information about Python decorators'")
    print("- 'What are the latest developments in LangChain?'")
    print("\nNote: For better results, add SERPER_API_KEY to your .env file")
    print("Get a free API key at: https://serper.dev")
    print("\n" + "="*50 + "\n")
    
    # Example: Search the web
    query = "What are the latest developments in LangChain?"
    print(f"Query: {query}\n")
    
    # Invoke the agent graph
    result = agent_graph.invoke({"messages": [HumanMessage(content=query)]})
    
    # Extract the response
    if "messages" in result and len(result["messages"]) > 0:
        last_message = result["messages"][-1]
        if hasattr(last_message, "content"):
            print(f"\nResult: {last_message.content}")
        else:
            print(f"\nResult: {last_message}")
    else:
        print(f"\nResult: {result}")

