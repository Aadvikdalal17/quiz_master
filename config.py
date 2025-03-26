import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for sessions and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///quiz_master.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Application Configuration
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    # Additional production-specific configurations
    pass