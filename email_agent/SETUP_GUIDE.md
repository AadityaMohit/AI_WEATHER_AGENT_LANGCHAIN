# Email Agent Setup Guide

This guide explains how to get all the required environment variables for the email agent.

## Required Environment Variables

### 1. GOOGLE_API_KEY
**Where to get it:**
- Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- Sign in with your Google account
- Click "Create API Key" or "Get API Key"
- Copy the generated API key

### 2. EMAIL_ADDRESS
**This is your email address:**
- Simply use your Gmail address (e.g., `yourname@gmail.com`)
- Or use any other email provider (Outlook, Yahoo, etc.)
- Make sure you have access to this email account

### 3. EMAIL_PASSWORD
**Important: This is NOT your regular email password!**

#### For Gmail users:
1. **Enable 2-Factor Authentication** (Required):
   - Go to your [Google Account Security](https://myaccount.google.com/security)
   - Enable "2-Step Verification" if not already enabled

2. **Generate an App Password**:
   - Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
   - Or navigate: Google Account → Security → 2-Step Verification → App passwords
   - Select "Mail" as the app
   - Select "Other (Custom name)" as the device
   - Enter a name like "LangChain Email Agent"
   - Click "Generate"
   - **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

3. **Use the App Password**:
   - Remove spaces: `abcdefghijklmnop`
   - Use this as your `EMAIL_PASSWORD` in the `.env` file

#### For other email providers:
- **Outlook/Hotmail**: Similar process - generate an app password from your Microsoft account
- **Yahoo**: Go to Account Security → Generate App Password
- **Other providers**: Check your email provider's documentation for "app passwords" or "application-specific passwords"

### 4. SMTP_SERVER (Optional - defaults to Gmail)
- **Gmail**: `smtp.gmail.com` (default)
- **Outlook**: `smtp-mail.outlook.com`
- **Yahoo**: `smtp.mail.yahoo.com`
- Check your email provider's SMTP settings

### 5. SMTP_PORT (Optional - defaults to 587)
- **Gmail**: `587` (default) or `465` for SSL
- **Outlook**: `587`
- **Yahoo**: `587` or `465`
- Most providers use port `587` for TLS

## Creating the .env File

Create a `.env` file in the **root directory** (parent of `email_agent` folder) with:

```env
# Google API Key for Gemini AI
GOOGLE_API_KEY=your_google_api_key_here

# Email Configuration
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_16_character_app_password_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## Example .env File

```env
GOOGLE_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
EMAIL_ADDRESS=john.doe@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## Important Security Notes

1. **Never commit your `.env` file to version control** (it should be in `.gitignore`)
2. **Never share your app password** - treat it like your regular password
3. **Use app passwords, not your main email password** - this is more secure
4. **If you suspect your app password is compromised**, revoke it and generate a new one

## Troubleshooting

### "Authentication failed" error:
- Make sure you're using an App Password, not your regular password
- Verify 2-Factor Authentication is enabled
- Check that the password has no spaces (remove spaces if copied with spaces)

### "Connection refused" error:
- Check your SMTP_SERVER and SMTP_PORT settings
- Some networks block SMTP ports - try a different network
- For Gmail, make sure "Less secure app access" is NOT the issue (use App Passwords instead)

### Still having issues?
- Verify your email and password are correct
- Check your email provider's SMTP documentation
- Make sure your firewall/antivirus isn't blocking the connection

