# In your __init__.py or app factory
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
    db.init_app(app)
    # Rest of your app setup
    return app