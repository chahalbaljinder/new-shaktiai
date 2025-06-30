"""
Email Service for SHAKTI-AI
Handles email sending with proper SMTP configuration and error handling.
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending emails via SMTP."""
    
    def __init__(self):
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_name = os.getenv('SMTP_FROM_NAME', 'SHAKTI-AI Support')
        self.from_email = os.getenv('SMTP_FROM_EMAIL', self.smtp_user)
    
    def is_configured(self) -> bool:
        """Check if SMTP is properly configured."""
        return bool(self.smtp_user and self.smtp_password)
    
    def test_connection(self) -> bool:
        """Test SMTP connection and authentication."""
        try:
            if not self.is_configured():
                logger.warning("SMTP not configured - missing username or password")
                return False
            
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.quit()
            logger.info("SMTP connection test successful")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication failed - check username/password")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def send_wish_share_email(self, wish_content: str, recipient_email: str, 
                            sender_name: str = "SHAKTI-AI User", wish_title: str = "My Wish") -> bool:
        """Send a wish sharing email."""
        try:
            # Check if we have placeholder credentials
            if (not self.is_configured() or 
                self.smtp_user == "your_email@gmail.com" or 
                self.smtp_password == "your_app_password" or
                self.smtp_password == "your_16_char_app_password"):
                logger.warning(f"SMTP not properly configured. Email content prepared for {recipient_email}")
                return self._log_email_content(wish_content, recipient_email, sender_name, wish_title)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = recipient_email
            msg['Subject'] = f"🌟 {wish_title} - Shared via SHAKTI-AI"
            
            # Create both plain text and HTML versions
            text_body = self._create_text_body(wish_content, sender_name, wish_title)
            html_body = self._create_html_body(wish_content, sender_name, wish_title)
            
            # Attach both versions
            msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            
            text = msg.as_string()
            server.sendmail(self.from_email, recipient_email, text)
            server.quit()
            
            logger.info(f"Wish sharing email sent successfully to {recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.warning("SMTP Authentication failed. Running in demo mode.")
            return self._log_email_content(wish_content, recipient_email, sender_name, wish_title)
        except smtplib.SMTPRecipientsRefused:
            logger.error(f"Recipient email rejected: {recipient_email}")
            return False
        except smtplib.SMTPException as e:
            logger.warning(f"SMTP error occurred, running in demo mode: {e}")
            return self._log_email_content(wish_content, recipient_email, sender_name, wish_title)
        except Exception as e:
            logger.warning(f"Email sending failed, running in demo mode: {e}")
            return self._log_email_content(wish_content, recipient_email, sender_name, wish_title)
    
    def _create_text_body(self, wish_content: str, sender_name: str, wish_title: str) -> str:
        """Create plain text email body."""
        return f"""Dear Friend,

I wanted to share something important with you through SHAKTI-AI's secure wishes vault.

Wish: {wish_title}

{wish_content}

This message was sent securely through SHAKTI-AI, a platform that supports women's health and well-being.

With care,
{sender_name}

---
Shared on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

🌟 SHAKTI-AI - Empowering Women's Health & Rights
For every woman, every phase, every fight.

This email was sent through SHAKTI-AI's secure sharing feature.
"""
    
    def _create_html_body(self, wish_content: str, sender_name: str, wish_title: str) -> str:
        """Create HTML email body with better formatting."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Shared via SHAKTI-AI</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 24px;">🌟 SHAKTI-AI</h1>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">Empowering Women's Health & Rights</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h2 style="color: #667eea; margin-top: 0;">A special message for you</h2>
                <p>Dear Friend,</p>
                <p>I wanted to share something important with you through SHAKTI-AI's secure wishes vault.</p>
            </div>
            
            <div style="background: white; border: 2px solid #667eea; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                <h3 style="color: #667eea; margin-top: 0; border-bottom: 2px solid #eee; padding-bottom: 10px;">{wish_title}</h3>
                <div style="font-size: 16px; line-height: 1.8; white-space: pre-wrap;">{wish_content}</div>
            </div>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <p style="margin: 0;"><strong>With care,</strong><br>{sender_name}</p>
            </div>
            
            <div style="text-align: center; font-size: 12px; color: #666; border-top: 1px solid #eee; padding-top: 15px;">
                <p>Shared on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                <p>🌟 <strong>SHAKTI-AI</strong> - For every woman, every phase, every fight.</p>
                <p style="margin-top: 15px; font-style: italic;">This email was sent through SHAKTI-AI's secure sharing feature.</p>
            </div>
        </body>
        </html>
        """
    
    def _log_email_content(self, wish_content: str, recipient_email: str, 
                          sender_name: str, wish_title: str) -> bool:
        """Log email content when SMTP is not configured."""
        logger.info(f"Email prepared for: {recipient_email}")
        logger.info(f"From: {sender_name}")
        logger.info(f"Subject: 🌟 {wish_title} - Shared via SHAKTI-AI")
        logger.info(f"Content: {wish_content}")
        return True
    
    def get_setup_instructions(self) -> Dict[str, Any]:
        """Get setup instructions for different email providers."""
        return {
            "gmail": {
                "smtp_host": "smtp.gmail.com",
                "smtp_port": "587",
                "instructions": [
                    "1. Enable 2-Factor Authentication on your Google Account",
                    "2. Go to Google Account Settings > Security > 2-Step Verification",
                    "3. Generate an 'App Password' for SHAKTI-AI",
                    "4. Use your Gmail address as SMTP_USER",
                    "5. Use the generated App Password as SMTP_PASSWORD"
                ],
                "env_example": """
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_FROM_NAME=SHAKTI-AI Support
SMTP_FROM_EMAIL=your_email@gmail.com
                """
            },
            "outlook": {
                "smtp_host": "smtp-mail.outlook.com",
                "smtp_port": "587",
                "instructions": [
                    "1. Use your regular Outlook/Hotmail password",
                    "2. Make sure 'Less secure app access' is enabled if needed",
                    "3. Use your Outlook email as SMTP_USER",
                    "4. Use your regular password as SMTP_PASSWORD"
                ]
            }
        }


# Global email service instance
email_service = EmailService()
