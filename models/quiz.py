import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db
from datetime import datetime

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, default=datetime.utcnow)
    time_duration = db.Column(db.Interval)
    remarks = db.Column(db.Text)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy='dynamic')
    scores = db.relationship('Score', backref='quiz', lazy='dynamic')