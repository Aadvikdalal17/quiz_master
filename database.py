from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy without binding to an app
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """
    Initialize database with the given Flask app
    
    Args:
        app (Flask): The Flask application instance
    """
    # Bind the database to the app
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate.init_app(app, db)
    
    # Import models to ensure they are recognized by SQLAlchemy
    from models.user import User
    from models.subject import Subject
    from models.chapter import Chapter
    from models.quiz import Quiz
    from models.question import Question
    
    # Create tables (alternative to using migrations)
    with app.app_context():
        db.create_all()

def reset_database(app):
    """
    Reset the entire database (use with caution!)
    
    Args:
        app (Flask): The Flask application instance
    """
    with app.app_context():
        # Drop all existing tables
        db.drop_all()
        
        # Recreate all tables
        db.create_all()
        print("Database reset and tables recreated!")