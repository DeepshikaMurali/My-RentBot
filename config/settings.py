import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask settings
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'

# HuggingFace settings
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')