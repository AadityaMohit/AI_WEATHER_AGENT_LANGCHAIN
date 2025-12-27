# LangChain AI Agents

A collection of AI agents built with LangChain and Google's Gemini model.

## Projects

### 1. Weather & Email Agent (`weather_email_agent/`) ⭐ **NEW!**
A combined AI agent that fetches weather information and sends it via email in one go.

**Features:**
- Get weather for any city
- Automatically send weather data via email
- Natural language queries combining both actions

**Quick Start:**
```bash
cd weather_email_agent
python app.py
```

**Example:** "Get the weather in Bangalore and send it to aadityamohit0308@gmail.com"

### 2. Weather Agent (`weather_agent/`)
An AI agent that provides real-time weather information using the OpenWeather API.

**Features:**
- Natural language weather queries
- Real-time weather data integration
- Multiple city support

**Quick Start:**
```bash
cd weather_agent
python app.py
```

### 3. Email Agent (`email_agent/`)
An AI agent that can send emails using SMTP.

**Features:**
- Natural language email composition
- SMTP integration
- Email attachment support

**Quick Start:**
```bash
cd email_agent
python app.py
```

### 4. Summarization Agent (`summarization_agent/`) ⭐ **NEW!**
An AI agent that summarizes text content, perfect for condensing long notes.

**Features:**
- Multiple summary formats (bullet points, paragraph, key points)
- Natural language summarization queries
- Perfect for notes app integration

**Quick Start:**
```bash
cd summarization_agent
python app.py
```

**Example:** "Summarize this text in bullet points: [your text]"

### 5. File Operations Agent (`file_operations_agent/`) ⭐ **NEW!**
An AI agent for managing note files - save, read, list, and delete notes.

**Features:**
- Save notes to files with automatic timestamping
- Read note files by name
- List all available note files
- Delete note files
- Essential for notes app integration

**Quick Start:**
```bash
cd file_operations_agent
python app.py
```

**Example:** "Save this note: [content]" or "List all my note files"

### 6. Translation Agent (`translation_agent/`) ⭐ **NEW!**
An AI agent that translates notes and text between languages.

**Features:**
- Support for 100+ languages
- Language detection
- Natural language translation queries
- Perfect for multilingual notes apps

**Quick Start:**
```bash
cd translation_agent
python app.py
```

**Example:** "Translate this to Spanish: [text]"

### 7. Web Search Agent (`web_search_agent/`) ⭐ **NEW!**
An AI agent that searches the web and retrieves information.

**Features:**
- Web search using DuckDuckGo (free) or Serper API
- Returns formatted results with titles, snippets, and URLs
- Perfect for research and information gathering

**Quick Start:**
```bash
cd web_search_agent
python app.py
```

**Example:** "Search for latest AI news" or "Find information about Python decorators"

### 8. Note Categorization Agent (`note_categorization_agent/`) ⭐ **NEW!**
An AI agent that automatically categorizes notes, suggests tags, and extracts entities.

**Features:**
- Automatic note categorization
- Smart tag suggestions
- Entity extraction (people, places, organizations, dates, topics)
- Perfect for organizing notes apps

**Quick Start:**
```bash
cd note_categorization_agent
python app.py
```

**Example:** "Categorize this note: [note content]" or "Suggest tags for: [note content]"

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirement.txt
   ```

2. **Get API Keys:**
   - **Google API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **OpenWeather API Key** (for Weather Agent): Get from [OpenWeatherMap](https://openweathermap.org/api)
   - **Serper API Key** (optional, for Web Search Agent): Get from [Serper.dev](https://serper.dev) - Free tier available

3. **Create a `.env` file** in the root directory:
   ```
   # Required for all agents
   GOOGLE_API_KEY=your_google_api_key_here
   
   # Required for Weather Agent
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   
   # Required for Email Agent
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password_here
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   
   # Optional for Web Search Agent (better results)
   SERPER_API_KEY=your_serper_api_key_here
   ```

## Project Structure

```
LangChain/
├── weather_email_agent/        # Combined Weather & Email Agent ⭐
│   ├── app.py
│   └── README.md
├── weather_agent/              # Weather AI Agent
│   ├── app.py
│   └── README.md
├── email_agent/                # Email AI Agent
│   ├── app.py
│   └── README.md
├── summarization_agent/       # Summarization Agent ⭐ NEW
│   ├── app.py
│   └── README.md
├── file_operations_agent/      # File Operations Agent ⭐ NEW
│   ├── app.py
│   └── README.md
├── translation_agent/          # Translation Agent ⭐ NEW
│   ├── app.py
│   └── README.md
├── web_search_agent/           # Web Search Agent ⭐ NEW
│   ├── app.py
│   └── README.md
├── note_categorization_agent/  # Note Categorization Agent ⭐ NEW
│   ├── app.py
│   └── README.md
├── notes/                      # Notes directory (created by file_operations_agent)
├── requirement.txt             # Shared dependencies
├── .env                        # Environment variables (create this)
├── AI_AGENT_SUGGESTIONS.md     # Complete list of agent suggestions
└── README.md                   # This file
```

## Requirements

See `requirement.txt` for all dependencies. The main packages include:
- `langchain>=0.2.0`
- `langchain-google-genai>=1.0.0`
- `python-dotenv>=1.0.0`
- `requests>=2.31.0`

## Notes

- Each agent is in its own folder for better organization
- All agents share the same virtual environment and dependencies
- The `.env` file should be in the root directory
- Each agent's README contains specific setup and usage instructions
