# SMTP Email Setup Guide for SHAKTI-AI

This guide will help you configure email sending functionality for the SHAKTI-AI Wishes Vault sharing feature.

## Quick Setup

### 1. Choose Your Email Provider

The most common and reliable option is **Gmail** with App Passwords.

### 2. Gmail Setup (Recommended)

#### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Navigate to **Security** > **2-Step Verification**
3. Follow the steps to enable 2FA if not already enabled

#### Step 2: Generate App Password
1. In Google Account Settings, go to **Security**
2. Under "2-Step Verification", click on **App passwords**
3. Select app: **Mail** and device: **Other (custom name)**
4. Enter "SHAKTI-AI" as the custom name
5. Click **Generate**
6. **Copy the 16-character password** (you'll need this)

#### Step 3: Update Environment Variables
Edit the `.env` file in your SHAKTI-AI root directory:

```bash
# SMTP Configuration for Email Sending
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_FROM_NAME=SHAKTI-AI Support
SMTP_FROM_EMAIL=your_email@gmail.com
```

**Replace:**
- `your_email@gmail.com` with your actual Gmail address
- `your_16_char_app_password` with the App Password you generated

### 3. Alternative Providers

#### Outlook/Hotmail
```bash
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your_email@outlook.com
SMTP_PASSWORD=your_regular_password
```

#### Yahoo Mail
```bash
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your_email@yahoo.com
SMTP_PASSWORD=your_app_password
```
*Note: Yahoo also requires App Passwords*

#### SendGrid (Professional)
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your_sendgrid_api_key
```

## Testing Your Configuration

### 1. Restart the Backend Service
After updating the `.env` file, restart the backend:

```bash
# Stop current backend
taskkill /f /im python.exe

# Start backend again
cd "c:\Users\balli\Desktop\new shaktiai"
uvicorn backend_service:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Test SMTP Configuration
You can test your configuration using the API endpoint:

```bash
# Test configuration
Invoke-WebRequest -Uri "http://localhost:8000/api/email/test" -Method GET
```

### 3. Test Email Sending
Try sharing a wish via email through the frontend, or test directly:

```bash
# Test email sharing
Invoke-WebRequest -Uri "http://localhost:8000/api/wishes/share" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"wish_id":11,"method":"email","recipient":"test@example.com","sender_name":"Test User"}'
```

## Troubleshooting

### Common Issues

#### 1. "SMTP Authentication failed"
- **Gmail**: Make sure you're using App Password, not regular password
- **Yahoo**: Generate and use App Password
- **Outlook**: Try enabling "Less secure app access" if needed

#### 2. "Connection refused" or "Connection timeout"
- Check SMTP_HOST and SMTP_PORT settings
- Ensure your firewall allows outbound connections on port 587
- Try port 465 with SSL instead of 587 with TLS

#### 3. "Sender address rejected"
- Make sure SMTP_FROM_EMAIL matches SMTP_USER
- Verify the email address is correctly formatted

### Security Best Practices

1. **Never commit credentials** to version control
2. **Use App Passwords** instead of regular passwords when possible
3. **Enable 2FA** on your email account
4. **Regularly rotate** your App Passwords
5. **Monitor email usage** for any suspicious activity

## Environment File Example

Here's a complete example of the SMTP section in your `.env` file:

```bash
# Database Configuration
DB_HOST=localhost
DB_NAME=shakti_ai_db
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_PORT=5432

# Google API
GOOGLE_API_KEY=your_google_api_key

# SMTP Configuration for Email Sending
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop  # 16-char App Password
SMTP_FROM_NAME=SHAKTI-AI Support
SMTP_FROM_EMAIL=your_email@gmail.com

# Model Configuration
MODEL_NAME=gemini-2.0-flash
TEMPERATURE=0.7
MAX_TOKENS=4096
```

## Verification

Once configured, you should see logs like this when sharing emails:

```
INFO:backend_service:Email successfully sent to recipient@example.com
```

Instead of:

```
INFO:backend_service:SMTP not configured. Email content prepared for recipient@example.com
```

## Support

If you encounter issues:

1. Check the backend logs for specific error messages
2. Test the configuration using the `/api/email/test` endpoint
3. Verify your email provider's SMTP settings
4. Ensure your environment variables are loaded correctly

The email sharing feature will work in "demo mode" (logging only) even without SMTP configuration, but will send actual emails once properly configured.
