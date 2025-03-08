from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db
from flask_login import LoginManager
from config import Config

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'user_controller.login'

# Import and Register Blueprints
from controllers.admin_controller import admin_bp
from controllers.user_controller import user_bp
from controllers.quiz_controller import quiz_bp

app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(quiz_bp)

# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Run the application
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  