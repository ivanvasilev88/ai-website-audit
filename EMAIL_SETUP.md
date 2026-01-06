# Email Setup Guide

## Quick Setup

The application now sends real emails with PDF reports attached! Here's how to configure it:

### Option 1: Gmail (Recommended for Testing)

1. **Enable App Password in Gmail:**
   - Go to your Google Account settings
   - Security → 2-Step Verification (enable if not already)
   - App passwords → Generate app password
   - Copy the 16-character password

2. **Set Environment Variables:**

```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASSWORD=your-16-char-app-password
export FROM_EMAIL=your-email@gmail.com
```

3. **Run Server:**
```bash
python3 server_standalone.py
```

### Option 2: Other Email Providers

**Outlook/Hotmail:**
```bash
export SMTP_SERVER=smtp-mail.outlook.com
export SMTP_PORT=587
export SMTP_USER=your-email@outlook.com
export SMTP_PASSWORD=your-password
export FROM_EMAIL=your-email@outlook.com
```

**SendGrid:**
```bash
export SMTP_SERVER=smtp.sendgrid.net
export SMTP_PORT=587
export SMTP_USER=apikey
export SMTP_PASSWORD=your-sendgrid-api-key
export FROM_EMAIL=your-verified-email@domain.com
```

**Mailgun:**
```bash
export SMTP_SERVER=smtp.mailgun.org
export SMTP_PORT=587
export SMTP_USER=your-mailgun-username
export SMTP_PASSWORD=your-mailgun-password
export FROM_EMAIL=your-verified-email@domain.com
```

### Option 3: No SMTP (Development Mode)

If you don't configure SMTP:
- ✅ User emails are still saved to `user_database.json`
- ✅ Email content is saved to `emails_to_send/` folder
- ❌ Emails won't be sent automatically

You can manually send the saved emails later.

---

## User Database

All user emails are automatically saved to `user_database.json` with:
- Email address
- Website URL
- Report ID
- Score
- Timestamp

This database is perfect for:
- Marketing campaigns
- Follow-up emails
- Analytics
- User retention

---

## Testing

1. Start the server with SMTP configured
2. Scan a website
3. Click "See the full AI interpretation"
4. Enter a valid email address
5. Complete payment
6. Check your email inbox for the PDF report!

---

## Troubleshooting

**"SMTP not configured" message:**
- Set the environment variables above
- Restart the server

**"Authentication failed":**
- For Gmail: Use App Password, not regular password
- Check credentials are correct
- Verify 2FA is enabled (for Gmail)

**Emails not arriving:**
- Check spam folder
- Verify SMTP credentials
- Check server logs for errors
- Try a different email provider

---

## Security Notes

- Never commit `user_database.json` to Git (already in .gitignore)
- Use environment variables, not hardcoded passwords
- For production, use a dedicated email service (SendGrid, Mailgun, etc.)

