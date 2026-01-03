import os
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

if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

# Set GOOGLE_API_KEY in environment for LangChain to use
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

@tool
def summarize_text(text: str, summary_type: str = "bullet") -> str:
    """
    Summarize a given text. Can create bullet points, paragraph summary, or key points.
    
    Args:
        text: The text content to summarize
        summary_type: Type of summary - "bullet" (bullet points), "paragraph" (single paragraph), or "key" (key points only)
    
    Returns:
        String containing the summary of the text
    """
    try:
        # Initialize a separate model instance for summarization
        summary_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3  # Lower temperature for more consistent summaries
        )
        
        # Create prompt based on summary type
        if summary_type.lower() == "bullet":
            prompt = f"""Please provide a concise bullet-point summary of the following text. 
            Focus on the main ideas and key information. Use 3-5 bullet points.
            
            Text:
            {text}
            
            Summary:"""
        elif summary_type.lower() == "paragraph":
            prompt = f"""Please provide a concise paragraph summary of the following text in 2-3 sentences.
            
            Text:
            {text}
            
            Summary:"""
        elif summary_type.lower() == "key":
            prompt = f"""Extract only the key points from the following text. List them as short phrases.
            
            Text:
            {text}
            
            Key Points:"""
        else:
            prompt = f"""Please provide a concise summary of the following text.
            
            Text:
            {text}
            
            Summary:"""
        
        # Get summary from model
        response = summary_model.invoke(prompt)
        summary = response.content if hasattr(response, 'content') else str(response)
        
        return summary.strip()
    
    except Exception as e:
        return f"Error creating summary: {str(e)}"

# Initialize Gemini model
chat = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Define tools
tools = [summarize_text]

# Create agent graph
agent_graph = create_agent(
    model=chat,
    tools=tools,
    debug=True
)

if __name__ == "__main__":
    # Example usage
    print("Summarization Agent is ready!")
    print("Example queries:")
    print("- 'Summarize this text: [your text here]'")
    print("- 'Create bullet points from this note: [note content]'")
    print("- 'Give me a paragraph summary of: [text]'")
    print("\n" + "="*50 + "\n")
    
    # Example text to summarize
    example_text = """
    Artificial Intelligence (AI) has revolutionized many industries in recent years. 
    Machine learning algorithms can now process vast amounts of data and make predictions 
    with remarkable accuracy. Natural language processing enables computers to understand 
    and generate human language. Computer vision allows machines to interpret visual 
    information. These technologies are being applied in healthcare, finance, transportation, 
    and many other sectors. However, there are also concerns about job displacement, 
    privacy, and the ethical implications of AI systems. As AI continues to advance, 
    it's important to balance innovation with responsible development and regulation.
    """
    
    query = f"Summarize this text in bullet points: {example_text}"
    print(f"Query: Summarize this text in bullet points\n")
    
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


