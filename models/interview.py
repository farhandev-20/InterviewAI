from datetime import datetime
from database.db import db

class Interview(db.Model):
    __tablename__ = 'interviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    role = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    interview_type = db.Column(db.String(50), nullable=False)  # Technical, HR, Mixed
    total_questions = db.Column(db.Integer, nullable=False, default=5)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='in_progress', nullable=False)  # in_progress, completed

    # Relationships
    user = db.relationship('User', backref=db.backref('interviews', lazy=True, cascade="all, delete-orphan"))
    questions = db.relationship('Question', backref='interview', lazy=True, cascade="all, delete-orphan", order_by="Question.order_number")
    ai_feedbacks = db.relationship('AIFeedback', backref='interview', lazy=True, cascade="all, delete-orphan")

    @property
    def duration_seconds(self):
        if self.end_time and self.start_time:
            return int((self.end_time - self.start_time).total_seconds())
        return int((datetime.utcnow() - self.start_time).total_seconds())

    @property
    def formatted_duration(self):
        secs = self.duration_seconds
        mins = secs // 60
        remaining_secs = secs % 60
        if mins > 0:
            return f"{mins}m {remaining_secs}s"
        return f"{remaining_secs}s"

    def __repr__(self):
        return f"<Interview id={self.id} role='{self.role}' status='{self.status}'>"


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    sample_answer = db.Column(db.Text, nullable=False)
    order_number = db.Column(db.Integer, nullable=False)

    # Relationships
    answers = db.relationship('Answer', backref='question', lazy=True, cascade="all, delete-orphan")
    ai_feedback = db.relationship('AIFeedback', backref='question_rel', uselist=False, cascade="all, delete-orphan")

    def get_user_answer(self):
        """Returns the most recent user answer string or None."""
        if self.answers:
            return self.answers[-1].answer_text
        return None

    def __repr__(self):
        return f"<Question id={self.id} order={self.order_number} topic='{self.topic}'>"


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, index=True)
    answer_text = db.Column(db.Text, nullable=True)
    time_taken = db.Column(db.Integer, default=0)  # in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Answer id={self.id} question_id={self.question_id}>"


class AIFeedback(db.Model):
    __tablename__ = 'ai_feedback'

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey('interviews.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, index=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=True)
    
    # 5 Section Scores (0-100)
    technical_score = db.Column(db.Float, default=0.0)
    communication_score = db.Column(db.Float, default=0.0)
    confidence_score = db.Column(db.Float, default=0.0)
    grammar_score = db.Column(db.Float, default=0.0)
    relevance_score = db.Column(db.Float, default=0.0)
    overall_score = db.Column(db.Float, default=0.0)

    strengths = db.Column(db.Text, nullable=True)
    weaknesses = db.Column(db.Text, nullable=True)
    improved_answer = db.Column(db.Text, nullable=True)
    missing_key_points = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<AIFeedback id={self.id} score={self.overall_score}>"
