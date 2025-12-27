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

# Common note categories
COMMON_CATEGORIES = [
    "Work", "Personal", "Study", "Meeting", "Ideas", "Research", 
    "Shopping", "Travel", "Health", "Finance", "Project", "Journal",
    "Recipe", "Book Notes", "Code", "Documentation", "Reminder", "Other"
]

@tool
def categorize_note(note_content: str, suggested_categories: str = None) -> str:
    """
    Categorize a note into appropriate categories and suggest tags.
    
    Args:
        note_content: The content of the note to categorize
        suggested_categories: Optional comma-separated list of custom categories to consider
    
    Returns:
        Categorization result with primary category, secondary categories, and suggested tags
    """
    try:
        categorization_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3  # Lower temperature for more consistent categorization
        )
        
        # Build category list
        categories = COMMON_CATEGORIES.copy()
        if suggested_categories:
            custom_cats = [cat.strip() for cat in suggested_categories.split(",")]
            categories.extend(custom_cats)
        
        prompt = f"""Analyze the following note and categorize it. 
        Provide:
        1. Primary category (one of: {', '.join(COMMON_CATEGORIES)} or a new appropriate category)
        2. Secondary categories (if applicable, up to 2)
        3. Suggested tags (3-5 relevant keywords)
        
        Format your response as:
        Primary Category: [category]
        Secondary Categories: [category1, category2] or None
        Tags: [tag1, tag2, tag3, tag4, tag5]
        
        Note content:
        {note_content}
        
        Categorization:"""
        
        response = categorization_model.invoke(prompt)
        result = response.content if hasattr(response, 'content') else str(response)
        
        return result.strip()
    
    except Exception as e:
        return f"Error categorizing note: {str(e)}"

@tool
def suggest_tags(note_content: str, num_tags: int = 5) -> str:
    """
    Suggest relevant tags for a note based on its content.
    
    Args:
        note_content: The content of the note
        num_tags: Number of tags to suggest (default: 5)
    
    Returns:
        Comma-separated list of suggested tags
    """
    try:
        tag_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.4
        )
        
        prompt = f"""Based on the following note content, suggest {num_tags} relevant tags (keywords).
        Tags should be short, descriptive, and useful for searching.
        Return only the tags as a comma-separated list, no additional text.
        
        Note content:
        {note_content}
        
        Tags:"""
        
        response = tag_model.invoke(prompt)
        tags = response.content if hasattr(response, 'content') else str(response)
        
        return f"Suggested tags: {tags.strip()}"
    
    except Exception as e:
        return f"Error suggesting tags: {str(e)}"

@tool
def extract_key_entities(note_content: str) -> str:
    """
    Extract key entities (people, places, organizations, dates, topics) from a note.
    
    Args:
        note_content: The content of the note
    
    Returns:
        Extracted entities organized by type
    """
    try:
        entity_model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2
        )
        
        prompt = f"""Extract key entities from the following note. 
        Identify and list:
        - People (names mentioned)
        - Places/Locations
        - Organizations/Companies
        - Dates/Time references
        - Main topics/subjects
        
        Format as:
        People: [list or None]
        Places: [list or None]
        Organizations: [list or None]
        Dates: [list or None]
        Topics: [list or None]
        
        Note content:
        {note_content}
        
        Entities:"""
        
        response = entity_model.invoke(prompt)
        entities = response.content if hasattr(response, 'content') else str(response)
        
        return entities.strip()
    
    except Exception as e:
        return f"Error extracting entities: {str(e)}"

# Initialize Gemini model
chat = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Define tools
tools = [categorize_note, suggest_tags, extract_key_entities]

# Create agent graph
agent_graph = create_agent(
    model=chat,
    tools=tools,
    debug=True
)

if __name__ == "__main__":
    # Example usage
    print("Note Categorization Agent is ready!")
    print("Example queries:")
    print("- 'Categorize this note: [note content]'")
    print("- 'Suggest tags for: [note content]'")
    print("- 'Extract entities from: [note content]'")
    print("\n" + "="*50 + "\n")
    
    # Example note
    example_note = """Meeting Notes - AI Project Discussion
    
    Date: January 15, 2024
    Participants: John Smith, Sarah Johnson, Mike Chen
    
    We discussed the implementation of new AI agents for our notes application.
    The team at TechCorp is interested in integrating our LangChain-based agents.
    Next meeting scheduled for February 1st.
    
    Key topics: Machine learning, Natural language processing, API integration
    """
    
    query = f"Categorize this note and suggest tags: {example_note}"
    print(f"Query: Categorize this note and suggest tags\n")
    
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

