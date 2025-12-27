import os
import sys
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Load environment variables from parent directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# Get API keys from environment
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "").strip("'\"")  # Remove quotes if present
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "").strip("'\"")  # Remove quotes if present

if not OPENWEATHER_API_KEY:
    raise ValueError("Please set OPENWEATHER_API_KEY in your .env file")
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")
if not EMAIL_ADDRESS:
    raise ValueError("Please set EMAIL_ADDRESS in your .env file")
if not EMAIL_PASSWORD:
    raise ValueError("Please set EMAIL_PASSWORD in your .env file")

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

@tool
def send_email(email_input: str) -> str:
    """
    Send an email using SMTP. The input should be formatted as: "to_email|subject|body" or "to_email|subject|body|attachment_path"
    
    Args:
        email_input: Formatted string containing email details separated by |
                    Format: "recipient@example.com|Subject|Email body content"
                    Optional: "recipient@example.com|Subject|Email body|path/to/attachment"
                    Example: "user@example.com|Hello|This is the email body"
    
    Returns:
        Success or error message indicating whether the email was sent successfully
    """
    try:
        # Parse the input string
        parts = email_input.split("|")
        if len(parts) < 3:
            return "Error: Input format should be 'to_email|subject|body' or 'to_email|subject|body|attachment_path'"
        
        to_email = parts[0].strip()
        subject = parts[1].strip()
        body = parts[2].strip()
        attachment_path = parts[3].strip() if len(parts) > 3 else None
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachment if provided
        if attachment_path and attachment_path.lower() != "none" and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
        
        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        server.quit()
        
        return f"Email sent successfully to {to_email}"
    
    except Exception as e:
        return f"Error sending email: {str(e)}"

# Initialize Gemini model
chat = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Define tools - both weather and email
tools = [get_weather, send_email]

# Create agent graph using the new LangChain 1.x API
agent_graph = create_agent(
    model=chat,
    tools=tools,
    debug=True  # debug=True enables verbose output
)

if __name__ == "__main__":
    # Example usage
    print("Weather & Email Agent is ready!")
    print("This agent can:")
    print("1. Get weather information for any city")
    print("2. Send emails with weather information")
    print("\nExample queries:")
    print("- 'Get the weather in Bangalore and send it to aadityamohit0308@gmail.com'")
    print("- 'What's the weather in New York? Send it to user@example.com'")
    print("- 'Get weather for Tokyo and email it to me at aadityamohit0308@gmail.com'")
    print("\n" + "="*50 + "\n")
    
    # Run agent with example query
    query = "Get the weather in Bangalore and send it to aadityamohit0308@gmail.com with subject 'Weather Update for Bangalore'"
    print(f"Query: {query}\n")
    
    # Invoke the agent graph with the query
    result = agent_graph.invoke({"messages": [HumanMessage(content=query)]})
    
    # Extract the response from the result
    if "messages" in result and len(result["messages"]) > 0:
        last_message = result["messages"][-1]
        if hasattr(last_message, "content"):
            # Handle both string and dict content
            content = last_message.content
            if isinstance(content, list) and len(content) > 0:
                if isinstance(content[0], dict) and 'text' in content[0]:
                    print(f"\nResult: {content[0]['text']}")
                else:
                    print(f"\nResult: {content[0]}")
            elif isinstance(content, str):
                print(f"\nResult: {content}")
            else:
                print(f"\nResult: {content}")
        else:
            print(f"\nResult: {last_message}")
    else:
        print(f"\nResult: {result}")

