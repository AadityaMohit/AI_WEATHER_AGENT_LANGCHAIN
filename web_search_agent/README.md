# Web Search AI Agent

An AI agent built with LangChain that can search the web and retrieve information, perfect for enriching notes with real-time data.

## Features

- AI-powered web search using DuckDuckGo (free) or Serper API (better results)
- Natural language search queries
- Returns formatted results with titles, snippets, and URLs
- Perfect for research and information gathering

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r ../requirement.txt
   ```

2. **Get API Keys:**
   - **Google API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **Serper API Key** (Optional but recommended): Get from [Serper.dev](https://serper.dev) - Free tier available

3. **Create/Update `.env` file** in the root directory:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   SERPER_API_KEY=your_serper_api_key_here  # Optional but recommended
   ```

## Usage

Run the agent:
```bash
python app.py
```

The agent can handle queries like:
- "Search for latest AI news"
- "Find information about Python decorators"
- "What are the latest developments in LangChain?"
- "Search for best practices in machine learning"
- "Find recent articles about quantum computing"

## Search Providers

- **DuckDuckGo** (Default): Free, no API key required, basic results
- **Serper API** (Recommended): Better results, free tier available, requires API key

## Example Output

```
Query: What are the latest developments in LangChain?

Result:
Search results for 'latest developments in LangChain':
Title: LangChain 0.2.0 Release Notes
Snippet: New features include improved agent capabilities...
URL: https://python.langchain.com/...

Title: LangChain Updates 2024
Snippet: Latest updates to the LangChain framework...
URL: https://blog.langchain.dev/...
```

## Integration with Notes App

This agent is perfect for:
- Researching topics and adding to notes
- Finding current information on any subject
- Enriching notes with web content
- Staying updated on topics of interest


