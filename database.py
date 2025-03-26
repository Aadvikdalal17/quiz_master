from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    """
    Initialize database with Flask app context
    
    :param app: Flask application instance
    """
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    migrate.init_app(app, db)
    
    # Create all tables within application context
    with app.app_context():
        try:
            # This will create tables that don't exist
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    
    return db

def get_db():
    """
    Provide a database session
    
    :return: SQLAlchemy database session
    """
    return db.session