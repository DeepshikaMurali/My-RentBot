# RentBot

A property management chatbot that helps tenants submit maintenance requests, ask about their lease, and report issues. Built with Flask and integrated with Hugging Face's AI models.

## Features

- Chat interface for tenant communication
- Handles maintenance requests
- Stores conversation history in SQLite database
- Uses AI to generate helpful, slightly sassy responses

## Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your Hugging Face API key
6. Run the app: `python app.py`