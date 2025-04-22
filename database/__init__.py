from .models import db, User, Chat, Message
from .db import init_db

# This makes these components importable from the database package
__all__ = ['db', 'init_db', 'User', 'Chat', 'Message']