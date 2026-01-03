# Note Categorization AI Agent

An AI agent built with LangChain that automatically categorizes notes, suggests tags, and extracts key entities - perfect for organizing your notes app.

## Features

- Automatic note categorization into predefined categories
- Smart tag suggestions based on content
- Entity extraction (people, places, organizations, dates, topics)
- Natural language queries for organization
- Perfect for notes app organization

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
- "Categorize this note: [note content]"
- "Suggest tags for: [note content]"
- "Extract entities from: [note content]"
- "What category should this note be in: [note content]"
- "Tag this note: [note content]"

## Categories

Default categories include:
- Work, Personal, Study, Meeting, Ideas, Research
- Shopping, Travel, Health, Finance, Project, Journal
- Recipe, Book Notes, Code, Documentation, Reminder, Other

## Example Output

```
Query: Categorize this note and suggest tags

Result:
Primary Category: Meeting
Secondary Categories: Work, Project
Tags: AI, LangChain, meeting, TechCorp, API integration
```

## Integration with Notes App

This agent is perfect for:
- Automatically organizing notes
- Suggesting relevant tags
- Extracting key information
- Improving note searchability
- Building smart note organization features


