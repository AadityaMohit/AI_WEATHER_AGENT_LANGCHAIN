import os
import sys
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
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "").strip("'\"")  # Remove quotes if present
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "").strip("'\"")  # Remove quotes if present

if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")
if not EMAIL_ADDRESS:
    raise ValueError("Please set EMAIL_ADDRESS in your .env file")
if not EMAIL_PASSWORD:
    raise ValueError("Please set EMAIL_PASSWORD in your .env file")

# Set GOOGLE_API_KEY in environment for LangChain to use
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

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

# Define tools - using the @tool decorator automatically creates the tool
tools = [send_email]

# Create agent graph using the new LangChain 1.x API
agent_graph = create_agent(
    model=chat,
    tools=tools,
    debug=True  # debug=True enables verbose output
)

if __name__ == "__main__":
    # Example usage
    print("Email Agent is ready!")
    print("Example queries:")
    print("- 'Send an email to user@example.com with subject Hello and body This is a test email'")
    print("- 'Email user@example.com saying Happy Birthday with subject Birthday Wishes'")
    print("\n" + "="*50 + "\n")
    
    # Run agent with example query - send to aadityamohit0308@gmail.com
    query = "Send an email to aadityamohit0308@gmail.com with subject 'Test Email from AI Agent' and body 'Hello! This is a test email sent from the LangChain AI email agent. The agent is working correctly!'"
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

