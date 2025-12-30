import os
import sys
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
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not OPENWEATHER_API_KEY:
    raise ValueError("Please set OPENWEATHER_API_KEY in your .env file")
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

# Set GOOGLE_API_KEY in environment for LangChain to use
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

@tool
def get_weather(city_name: str) -> str:
    """
    Get current weather information for a city.
    
    Args:
        city_name: The name of the city to get weather for (e.g., "London", "New York", "Bangalore", "Tokyo")
    
    Returns:
        String containing weather information including temperature, condition, humidity, and wind speed
    """
    try:
        # OpenWeather API endpoint
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city_name,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"  # Use metric units (Celsius)
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant information
        city = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].title()
        wind_speed = data["wind"]["speed"]
        
        weather_info = f"""
Weather in {city}, {country}:
- Temperature: {temp}°C (feels like {feels_like}°C)
- Condition: {description}
- Humidity: {humidity}%
- Wind Speed: {wind_speed} m/s
"""
        return weather_info.strip()
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"
    except KeyError as e:
        return f"Error parsing weather data: Missing key {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Initialize Gemini model
chat = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Define tools - using the @tool decorator automatically creates the tool
tools = [get_weather]

# Create agent graph using the new LangChain 1.x API
agent_graph = create_agent(
    model=chat,
    tools=tools,
    debug=True  # debug=True enables verbose output
)

if __name__ == "__main__":
    # Example usage
    print("Weather Agent is ready!")
    print("Example queries:")
    print("- 'What's the weather in Bangalore yesterday?'")
    print("- 'Get weather for New York'")
    print("- 'How's the weather in Tokyo?'")
    print("\n" + "="*50 + "\n")
    
    # Run agent with example query
    query = "What's the weather in Bangalore?"
    print(f"Query: {query}\n")
    
    # Invoke the agent graph with the query
    result = agent_graph.invoke({"messages": [HumanMessage(content=query)]})
    
    # Extract the response from the result
    if "messages" in result and len(result["messages"]) > 0:
        last_message = result["messages"][-1]
        if hasattr(last_message, "content"):
            print(f"\nResult: {last_message.content}")
        else:
            print(f"\nResult: {last_message}")
    else:
        print(f"\nResult: {result}")
