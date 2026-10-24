from datetime import datetime
from database.db import db

class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=True)
    raw_text = db.Column(db.Text, nullable=False)
    
    parsed_name = db.Column(db.String(100), nullable=True)
    parsed_email = db.Column(db.String(120), nullable=True)
    parsed_phone = db.Column(db.String(50), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    education = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    projects = db.Column(db.Text, nullable=True)
    certifications = db.Column(db.Text, nullable=True)
    tools = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    analyses = db.relationship('ResumeAnalysis', backref='resume', lazy=True, cascade="all, delete-orphan")
    matches = db.relationship('ResumeJobMatch', backref='resume', lazy=True, cascade="all, delete-orphan")
    skill_gaps = db.relationship('SkillGap', backref='resume', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Resume id={self.id} filename='{self.filename}'>"


class ResumeAnalysis(db.Model):
    __tablename__ = 'resume_analyses'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False, index=True)
    
    # 7 ATS Sub-metrics (0-100)
    ats_score = db.Column(db.Float, default=0.0)
    skills_score = db.Column(db.Float, default=0.0)
    keywords_score = db.Column(db.Float, default=0.0)
    experience_score = db.Column(db.Float, default=0.0)
    projects_score = db.Column(db.Float, default=0.0)
    education_score = db.Column(db.Float, default=0.0)
    readability_score = db.Column(db.Float, default=0.0)
    formatting_score = db.Column(db.Float, default=0.0)

    summary = db.Column(db.Text, nullable=True)
    strengths = db.Column(db.Text, nullable=True)
    weaknesses = db.Column(db.Text, nullable=True)
    missing_skills = db.Column(db.Text, nullable=True)
    grammar_suggestions = db.Column(db.Text, nullable=True)
    formatting_suggestions = db.Column(db.Text, nullable=True)
    project_suggestions = db.Column(db.Text, nullable=True)
    career_recommendations = db.Column(db.Text, nullable=True)
    actionable_improvements = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ResumeAnalysis id={self.id} ats_score={self.ats_score}>"


class JobDescription(db.Model):
    __tablename__ = 'job_descriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(150), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    raw_text = db.Column(db.Text, nullable=False)

    required_skills = db.Column(db.Text, nullable=True)
    preferred_skills = db.Column(db.Text, nullable=True)
    responsibilities = db.Column(db.Text, nullable=True)
    experience_level = db.Column(db.String(100), nullable=True)
    technologies = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    matches = db.relationship('ResumeJobMatch', backref='job_description', lazy=True, cascade="all, delete-orphan")
    skill_gaps = db.relationship('SkillGap', backref='job_description', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<JobDescription id={self.id} title='{self.title}'>"


class ResumeJobMatch(db.Model):
    __tablename__ = 'resume_job_matches'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False, index=True)
    job_description_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False, index=True)

    overall_match_pct = db.Column(db.Float, default=0.0)
    hiring_probability = db.Column(db.String(50), default='Moderate')  # High, Moderate, Low
    matching_skills = db.Column(db.Text, nullable=True)
    missing_skills = db.Column(db.Text, nullable=True)
    missing_keywords = db.Column(db.Text, nullable=True)
    recommended_improvements = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ResumeJobMatch id={self.id} match={self.overall_match_pct}%>"


class SkillGap(db.Model):
    __tablename__ = 'skill_gaps'

    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False, index=True)
    job_description_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False, index=True)

    present_skills = db.Column(db.Text, nullable=True)
    missing_skills = db.Column(db.Text, nullable=True)
    priority_skills = db.Column(db.Text, nullable=True)
    learning_path = db.Column(db.Text, nullable=True)  # JSON or formatted list
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<SkillGap id={self.id}>"
