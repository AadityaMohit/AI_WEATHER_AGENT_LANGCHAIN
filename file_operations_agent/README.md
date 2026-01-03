# File Operations AI Agent

An AI agent built with LangChain that can save, read, list, and delete note files - essential for any notes app integration.

## Features

- Save notes to files with automatic timestamping
- Read note files by name
- List all available note files
- Delete note files
- Automatic notes directory management
- Support for .txt, .md, and .json formats

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
- "Save this note: [content]"
- "Save this to a file named 'my_notes': [content]"
- "Read the note file: [filename]"
- "List all my note files"
- "Delete the note file: [filename]"
- "Show me all available notes"

## File Storage

Notes are saved in the `notes/` directory in the project root. The directory is created automatically if it doesn't exist.

## Example Output

```
Query: Save this note to a file named 'meeting_notes'

Result: Note saved successfully to: notes/meeting_notes.txt
```

## Integration with Notes App

This agent is essential for:
- Persisting notes to disk
- Retrieving saved notes
- Managing note files
- Organizing note storage


