"""Security utilities for input validation and key generation"""
import secrets
import re

def generate_secret_key():
    """Generate a secure random key for session management"""
    return secrets.token_hex(32)

def sanitize_input(text: str) -> str:
    """Remove potentially harmful characters from input"""
    # Remove HTML tags and extra whitespace
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None