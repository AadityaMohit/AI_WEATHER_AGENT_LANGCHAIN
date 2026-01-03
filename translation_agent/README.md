# Translation AI Agent

An AI agent built with LangChain that can translate notes and text between languages, perfect for multilingual notes apps.

## Features

- AI-powered translation using Google's Gemini model
- Support for 100+ languages
- Language detection
- Natural language queries for translation
- Perfect for international notes app users

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
- "Translate this to Spanish: [text]"
- "Translate this note to French: [note content]"
- "What language is this: [text]"
- "Convert this to Japanese: [text]"
- "Translate to German: [text]"

## Supported Languages

The agent supports all major languages including:
- Spanish, French, German, Italian, Portuguese
- Chinese (Simplified & Traditional), Japanese, Korean
- Hindi, Arabic, Russian, Dutch, Swedish
- And many more!

## Example Output

```
Query: Translate this to Spanish: Hello, how are you today?

Result: Hola, ¿cómo estás hoy?
```

## Integration with Notes App

This agent is perfect for:
- Translating notes between languages
- Creating multilingual notes
- Understanding notes in foreign languages
- Supporting international users


