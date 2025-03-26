from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db
from models.quiz import Quiz
from models.score import Score
from models.question import Question

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/start_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions.all()
    
    if request.method == 'POST':
        # Quiz submission logic
        score = calculate_score(quiz, request.form)
        
        # Save score
        new_score = Score(
            user_id=current_user.id, 
            quiz_id=quiz_id, 
            total_score=score
        )
        db.session.add(new_score)
        db.session.commit()
        
        return redirect(url_for('quiz.quiz_result', quiz_id=quiz_id))
    
    return render_template('quiz/start_quiz.html', quiz=quiz, questions=questions)

def calculate_score(quiz, submitted_answers):
    questions = quiz.questions.all()
    total_correct = 0
    
    for question in questions:
        user_answer = submitted_answers.get(f'question_{question.id}')
        if user_answer == str(question.correct_option):
            total_correct += 1
    
    total_score = (total_correct / len(questions)) * 100
    return total_score

@quiz_bp.route('/quiz_result/<int:quiz_id>')
@login_required
def quiz_result(quiz_id):
    score = Score.query.filter_by(
        user_id=current_user.id, 
        quiz_id=quiz_id
    ).first()
    
    return render_template('quiz/quiz_result.html', score=score)