from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from database import db, init_db
from flask_login import LoginManager
from config import Config

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a real secret key
    
    # Initialize extensions
    init_db(app)
    migrate = Migrate(app, db)
    
    # Login Manager
    login_manager = LoginManager(app)
    login_manager.login_view = 'user.login'
    
    # Import models (use the correct import paths)
    from models.user import User
    from models.subject import Subject
    from models.chapter import Chapter
    from models.quiz import Quiz
    from models.question import Question
    
    # Register blueprints
    from controllers.admin_controller import admin_bp
    from controllers.user_controller import user_bp
    from controllers.quiz_controller import quiz_bp
    
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    
    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Home route
    @app.route('/')
    def index():
        """Home page route"""
        return render_template('home.html')
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)