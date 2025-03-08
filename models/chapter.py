from database import db

class Chapter(db.Model):
    __tablename__ = 'chapters'  # Note: use double underscores, not single asterisks
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
    # Relationships
    quizzes = db.relationship('Quiz', backref='chapter', lazy='dynamic')

    def __repr__(self):
        return f"<Chapter {self.name}>"