from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db
from models.subject import Subject
from models.chapter import Chapter
from models.quiz import Quiz
from models.question import Question

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Add admin dashboard logic
    subjects = Subject.query.all()
    return render_template('admin/dashboard.html', subjects=subjects)

@admin_bp.route('/admin/add_subject', methods=['GET', 'POST'])
@login_required
def add_subject():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        new_subject = Subject(name=name, description=description)
        db.session.add(new_subject)
        db.session.commit()
        
        flash('Subject added successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('admin/add_subject.html')