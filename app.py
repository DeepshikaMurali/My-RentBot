from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv

# Import our components
from database.models import db, User, Chat, Message
from database.db import init_db
from models.chatbot import ChatbotModel
from utils.helpers import sanitize_input

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_pyfile('config/settings.py')

# Initialize database
init_db(app)

# Initialize chatbot model
chatbot = ChatbotModel()

# Routes
@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """Render the chat interface"""
    return render_template('chat.html')

@app.route('/api/message', methods=['POST'])
def message():

    print("Raw data from request:", request.get_json())
    
    """Handle incoming chat messages"""
    if request.method == 'POST':
        # Get message from the request
        data = request.get_json()
        user_message = sanitize_input(data.get('message', ''))
        
        # Skip empty messages
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get response from chatbot
        bot_response = chatbot.get_response(user_message)
        
        # For demo purposes, we'll create a user if none exists
        user = User.query.filter_by(username='demo_user').first()
        if not user:
            user = User(username='demo_user', email='demo@example.com')
            db.session.add(user)
            db.session.commit()
        
        # Create or get the latest chat
        chat = Chat.query.filter_by(user_id=user.id).order_by(Chat.started_at.desc()).first()
        if not chat:
            chat = Chat(user_id=user.id)
            db.session.add(chat)
            db.session.commit()
        
        # Save user message
        user_msg = Message(chat_id=chat.id, content=user_message, is_bot=False)
        db.session.add(user_msg)
        
        # Save bot response
        bot_msg = Message(chat_id=chat.id, content=bot_response, is_bot=True)
        db.session.add(bot_msg)
        
        # Commit to database
        db.session.commit()
        
        return jsonify({
            'user_message': user_message,
            'bot_response': bot_response
        })

if __name__ == '__main__':
    app.run(debug=True)