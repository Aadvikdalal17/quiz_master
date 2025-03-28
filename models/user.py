import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    qualification = db.Column(db.String(100), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    
    def set_password(self, password):
        """
        Set the password hash for the user
        
        Args:
            password (str): Plain text password
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Check if the provided password is correct
        
        Args:
            password (str): Plain text password to check
        
        Returns:
            bool: True if password is correct, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def find_by_email(cls, email):
        """
        Find a user by their email address
        
        Args:
            email (str): Email address to search for
        
        Returns:
            User or None: User object if found, None otherwise
        """
        return cls.query.filter_by(email=email).first()