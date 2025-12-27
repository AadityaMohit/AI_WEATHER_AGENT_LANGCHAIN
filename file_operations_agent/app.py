import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from datetime import datetime

# Load environment variables from parent directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# Get API keys from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

# Set GOOGLE_API_KEY in environment for LangChain to use
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Default notes directory
NOTES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "notes")
os.makedirs(NOTES_DIR, exist_ok=True)

@tool
def save_note_to_file(content: str, filename: str = None) -> str:
    """
    Save note content to a file. If filename is not provided, generates one with timestamp.
    
    Args:
        content: The note content to save
        filename: Optional filename (without extension). If not provided, uses timestamp.
                  If provided without extension, adds .txt. If provided with extension, uses as-is.
    
    Returns:
        Success message with file path
    """
    try:
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"note_{timestamp}.txt"
        elif not filename.endswith(('.txt', '.md', '.json')):
            filename = f"{filename}.txt"
        
        filepath = os.path.join(NOTES_DIR, filename)
        
        # Save content to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Note saved successfully to: {filepath}"
    
    except Exception as e:
        return f"Error saving note: {str(e)}"

@tool
def read_note_from_file(filename: str) -> str:
    """
    Read content from a note file.
    
    Args:
        filename: Name of the file to read (with or without extension)
    
    Returns:
        Content of the file or error message
    """
    try:
        # Add .txt extension if not present
        if not filename.endswith(('.txt', '.md', '.json')):
            filename = f"{filename}.txt"
        
        filepath = os.path.join(NOTES_DIR, filename)
        
        if not os.path.exists(filepath):
            return f"Error: File '{filename}' not found in notes directory"
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f"Content of {filename}:\n\n{content}"
    
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def list_note_files() -> str:
    """
    List all note files in the notes directory.
    
    Returns:
        List of available note files
    """
    try:
        files = [f for f in os.listdir(NOTES_DIR) if os.path.isfile(os.path.join(NOTES_DIR, f))]
        
        if not files:
            return "No note files found in the notes directory."
        
        files.sort(key=lambda x: os.path.getmtime(os.path.join(NOTES_DIR, x)), reverse=True)
        
        file_list = "Available note files:\n"
        for i, file in enumerate(files, 1):
            filepath = os.path.join(NOTES_DIR, file)
            size = os.path.getsize(filepath)
            modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
            file_list += f"{i}. {file} ({size} bytes, modified: {modified})\n"
        
        return file_list.strip()
    
    except Exception as e:
        return f"Error listing files: {str(e)}"

@tool
def delete_note_file(filename: str) -> str:
    """
    Delete a note file.
    
    Args:
        filename: Name of the file to delete (with or without extension)
    
    Returns:
        Success or error message
    """
    try:
        # Add .txt extension if not present
        if not filename.endswith(('.txt', '.md', '.json')):
            filename = f"{filename}.txt"
        
        filepath = os.path.join(NOTES_DIR, filename)
        
        if not os.path.exists(filepath):
            return f"Error: File '{filename}' not found"
        
        os.remove(filepath)
        return f"File '{filename}' deleted successfully"
    
    except Exception as e:
        return f"Error deleting file: {str(e)}"

# Initialize Gemini model
chat = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Define tools
tools = [save_note_to_file, read_note_from_file, list_note_files, delete_note_file]

# Create agent graph
agent_graph = create_agent(
    model=chat,
    tools=tools,
    debug=True
)

if __name__ == "__main__":
    # Example usage
    print("File Operations Agent is ready!")
    print("Example queries:")
    print("- 'Save this note: [content]'")
    print("- 'Read the note file: [filename]'")
    print("- 'List all my note files'")
    print("- 'Delete the note file: [filename]'")
    print("\n" + "="*50 + "\n")
    
    # Example: Save a note
    example_content = """Meeting Notes - AI Project Discussion
    
    Date: 2024-01-15
    Participants: Team members
    
    Key Points:
    1. Discussed new AI agent features
    2. Planned integration with notes app
    3. Next steps: Implement web search agent
    
    Action Items:
    - Review agent suggestions
    - Start implementation
    """
    
    query = f"Save this note to a file named 'meeting_notes': {example_content}"
    print(f"Query: Save this note to a file named 'meeting_notes'\n")
    
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

