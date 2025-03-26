from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import db
from models.user import User
from models.quiz import Quiz
from models.score import Score

# Create blueprint
user_bp = Blueprint('user', __name__)  # Fixed the syntax error here

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate form data
        if not username or not email or not password:
            flash('All fields are required', 'danger')  # Changed to 'danger' for Bootstrap
            return render_template('user/register.html')
            
        if password != confirm_password:
            flash('Passwords do not match', 'danger')  # Changed to 'danger' for Bootstrap
            return render_template('user/register.html')
            
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'danger')  # Changed to 'danger' for Bootstrap
            return render_template('user/register.html')
            
        # Create new user
        try:
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                is_admin=False
            )
            
            # Add user to database
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('user.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'danger')
            return render_template('user/register.html')
            
    return render_template('user/register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Validate form data
        if not email or not password:
            flash('Email and password are required', 'danger')  # Changed to 'danger' for Bootstrap
            return render_template('user/login.html')
            
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password', 'danger')  # Changed to 'danger' for Bootstrap
            return render_template('user/login.html')
            
        # Log in user
        login_user(user, remember=remember)
        
        # Redirect to admin dashboard if user is admin
        if user.is_admin:
            return redirect(url_for('admin.dashboard'))
            
        return redirect(url_for('user.dashboard'))
        
    return render_template('user/login.html')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route"""
    # Get user's quiz attempts
    quiz_attempts = Quiz.query.all()  # Replace with actual user quiz data query
    return render_template('user/dashboard.html', quiz_attempts=quiz_attempts)

@user_bp.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))