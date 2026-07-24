from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    target_role = db.Column(db.String(100), nullable=True, default="Full Stack Developer")
    skills = db.Column(db.Text, nullable=True, default="Python, JavaScript, Data Structures, System Design")
    profile_image = db.Column(db.String(255), nullable=True, default="default_avatar.png")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify password hash."""
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Record the login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def get_avatar_url(self):
        """Returns the avatar URL or default placeholder."""
        if self.profile_image and self.profile_image != "default_avatar.png":
            return f"/static/uploads/{self.profile_image}"
        return f"https://ui-avatars.com/api/?name={self.full_name.replace(' ', '+')}&background=6366f1&color=fff&bold=true"

    def __repr__(self):
        return f"<User id={self.id} email='{self.email}'>"
