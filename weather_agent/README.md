# Weather AI Agent

An AI agent built with LangChain that uses the OpenWeather API as a tool to provide weather information.

## Features

- AI-powered weather agent using Google's Gemini model
- OpenWeather API integration for real-time weather data
- Natural language queries for weather information

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r ../requirement.txt
   ```

2. **Get API Keys:**
   - **Google API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **OpenWeather API Key**: Get free API key from [OpenWeatherMap](https://openweathermap.org/api)

3. **Create a `.env` file** in the root directory with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   OPENWEATHER_API_KEY=your_openweather_api_key_here
   ```

## Usage

Run the agent:
```bash
python app.py
```

The agent can answer questions like:
- "What's the weather in Bangalore?"
- "Get weather for New York"
- "How's the weather in Tokyo?"

## Example Output

```
Query: What's the weather in Bangalore?

Weather in Bangalore, IN:
- Temperature: 28°C (feels like 30°C)
- Condition: Partly Cloudy
- Humidity: 65%
- Wind Speed: 3.2 m/s
```
