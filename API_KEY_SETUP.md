# API Key Setup Guide

## Google API Key Setup

### Step 1: Get Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key" or "Get API Key"
4. Copy your new API key

### Step 2: Create/Update .env File

Create a `.env` file in the root directory of your project (same level as `requirement.txt`):

```env
# Required for all agents
GOOGLE_API_KEY=your_new_api_key_here

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

### Step 3: Security Best Practices

⚠️ **IMPORTANT:**
- Never commit your `.env` file to version control (Git)
- Never share your API keys publicly
- If a key is leaked, immediately revoke it and create a new one
- Use environment variables, never hardcode keys in your code

### Step 4: Verify Setup

Test your setup by running any agent:

```bash
cd summarization_agent
python app.py
```

If you see the agent working without permission errors, your API key is correctly configured!

## Troubleshooting

### Error: "API key was reported as leaked"
- Your API key has been compromised
- **Solution:** Get a new API key from Google AI Studio and update your `.env` file

### Error: "Please set GOOGLE_API_KEY in your .env file"
- The `.env` file is missing or the key is not set
- **Solution:** Create/update the `.env` file in the root directory with your API key

### Error: "PERMISSION_DENIED"
- API key is invalid, expired, or has insufficient permissions
- **Solution:** Check your API key in Google AI Studio, ensure it's active, and has proper permissions

## Additional API Keys

### OpenWeather API (for Weather Agent)
- Get from: https://openweathermap.org/api
- Free tier available

### Serper API (optional, for Web Search Agent)
- Get from: https://serper.dev
- Free tier available for better search results


