# Summarization AI Agent

An AI agent built with LangChain that can summarize text content, perfect for condensing long notes, articles, or meeting transcripts.

## Features

- AI-powered summarization using Google's Gemini model
- Multiple summary formats: bullet points, paragraph, or key points
- Natural language queries for summarization
- Perfect for notes app integration

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r ../requirement.txt
   ```

2. **Get API Keys:**
   - **Google API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. **Create/Update `.env` file** in the root directory:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

Run the agent:
```bash
python app.py
```

The agent can handle queries like:
- "Summarize this text: [your text here]"
- "Create bullet points from this note: [note content]"
- "Give me a paragraph summary of: [text]"
- "Extract key points from: [text]"

## Example Output

```
Query: Summarize this text in bullet points

Result:
- AI has revolutionized many industries through machine learning, NLP, and computer vision
- Applied in healthcare, finance, transportation, and other sectors
- Concerns exist about job displacement, privacy, and ethical implications
- Need to balance innovation with responsible development and regulation
```

## Integration with Notes App

This agent is perfect for:
- Summarizing long meeting notes
- Condensing articles saved to notes
- Creating quick overviews of lengthy documents
- Extracting key points from research notes

