import re
from datetime import datetime

def format_timestamp(timestamp):
    """Format a timestamp for display"""
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def sanitize_input(text):
    """Basic input sanitization"""
    # Remove any HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()