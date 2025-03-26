# Add this to a file called 'seed_data.py'
from app import app, db
from models.user import User
from models.subject import Subject
from models.chapter import Chapter
from models.quiz import Quiz
from models.question import Question

with app.app_context():
    # Create admin user
    admin = User(username="admin", email="admin@example.com", is_admin=True)
    admin.set_password("securepassword")
    db.session.add(admin)
    
    # Create some subjects
    math = Subject(name="Mathematics", description="Math topics")
    db.session.add(math)
    
    # Add chapters
    algebra = Chapter(name="Algebra", subject=math)
    db.session.add(algebra)
    
    # Add a quiz
    quiz = Quiz(title="Basic Algebra", chapter=algebra, time_limit=15)
    db.session.add(quiz)
    
    # Add some questions
    question1 = Question(
        quiz=quiz,
        text="Solve for x: 2x + 5 = 13",
        option_a="x = 4",
        option_b="x = 5", 
        option_c="x = 6",
        option_d="x = 7",
        correct_option="a"
    )
    db.session.add(question1)
    
    db.session.commit()