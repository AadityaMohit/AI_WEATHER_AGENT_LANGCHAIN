# Email AI Agent

An AI agent built with LangChain that can send emails using SMTP.

## Features

- AI-powered email agent using Google's Gemini model
- SMTP integration for sending emails
- Natural language email composition and sending
- Support for email attachments

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r ../requirement.txt
   ```

2. **Get API Keys:**
   - **Google API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

3. **Email Configuration:**
   
   **For Gmail:**
   - Enable 2-Factor Authentication in your [Google Account Security](https://myaccount.google.com/security)
   - Generate an App Password: [Google App Passwords](https://myaccount.google.com/apppasswords)
     - Select "Mail" and "Other (Custom name)"
     - Enter "LangChain Email Agent" as the name
     - Copy the 16-character password (remove spaces)
   - Use the app password as EMAIL_PASSWORD (NOT your regular password!)
   
   **For other email providers:**
   - Check your provider's documentation for generating app passwords
   - Update SMTP_SERVER and SMTP_PORT accordingly
   
   **📖 See SETUP_GUIDE.md for detailed step-by-step instructions**

4. **Create/Update `.env` file** in the root directory:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password_here
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ```

## Usage

Run the agent:
```bash
python app.py
```

The agent can handle queries like:
- "Send an email to user@example.com with subject Hello and body This is a test email"
- "Email user@example.com saying Happy Birthday with subject Birthday Wishes"

## Security Note

- Never commit your `.env` file to version control
- Use app passwords instead of your main email password
- Keep your API keys secure

