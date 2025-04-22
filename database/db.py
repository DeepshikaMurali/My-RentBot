from .models import db

def init_db(app):
    """Initialize the database with the Flask app"""
    # Configure the database connection
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the app with the database
    db.init_app(app)
    
    # Create all tables defined in models.py
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")