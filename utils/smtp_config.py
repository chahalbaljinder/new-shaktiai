"""
SMTP Configuration for SHAKTI-AI Email Service
"""

import os
from typing import Dict, Any


class SMTPConfig:
    """SMTP Configuration class for email sending."""
    
    def __init__(self):
        # Load SMTP settings from environment variables
        self.host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.port = int(os.getenv('SMTP_PORT', '587'))
        self.username = os.getenv('SMTP_USER')
        self.password = os.getenv('SMTP_PASSWORD')
        self.from_name = os.getenv('SMTP_FROM_NAME', 'SHAKTI-AI Support')
        self.from_email = os.getenv('SMTP_FROM_EMAIL', self.username)
        self.use_tls = True  # Always use TLS for security
    
    def is_configured(self) -> bool:
        """Check if SMTP is properly configured."""
        return bool(self.username and self.password)
    
    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return {
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': '***' if self.password else None,  # Hide password in logs
            'from_name': self.from_name,
            'from_email': self.from_email,
            'use_tls': self.use_tls,
            'configured': self.is_configured()
        }
    
    @classmethod
    def get_provider_settings(cls, provider: str) -> Dict[str, Any]:
        """Get common SMTP settings for popular email providers."""
        providers = {
            'gmail': {
                'host': 'smtp.gmail.com',
                'port': 587,
                'use_tls': True,
                'instructions': 'Use App Password (not regular password). Enable 2FA and generate App Password in Google Account settings.'
            },
            'outlook': {
                'host': 'smtp-mail.outlook.com',
                'port': 587,
                'use_tls': True,
                'instructions': 'Use your regular Outlook password.'
            },
            'yahoo': {
                'host': 'smtp.mail.yahoo.com',
                'port': 587,
                'use_tls': True,
                'instructions': 'Use App Password. Enable 2FA and generate App Password in Yahoo Account settings.'
            },
            'sendgrid': {
                'host': 'smtp.sendgrid.net',
                'port': 587,
                'use_tls': True,
                'instructions': 'Use "apikey" as username and your API key as password.'
            }
        }
        return providers.get(provider.lower(), {})


# Global SMTP configuration instance
smtp_config = SMTPConfig()
