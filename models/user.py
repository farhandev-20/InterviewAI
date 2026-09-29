import urllib.parse
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), nullable=True, unique=True)
    target_role = db.Column(db.String(100), nullable=True, default="Full Stack Developer")
    skills = db.Column(db.Text, nullable=True, default="Python, JavaScript, Data Structures, System Design")
    profile_image = db.Column(db.String(500), nullable=True, default="default_avatar.png")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Hash and set the user's password."""
        if password:
            self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify password hash."""
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Record the login timestamp."""
        self.last_login = datetime.utcnow()
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    def get_initials(self):
        """Generate user initials dynamically (e.g. 'Farhan Attar' -> 'FA', 'John Doe' -> 'JD', 'Farhan' -> 'F')."""
        name = (self.full_name or '').strip()
        if not name or name.lower() in ['none', 'user', 'google user']:
            if self.email and '@' in self.email:
                name = self.email.split('@')[0]
            else:
                return 'U'
        
        parts = [p for p in name.replace('_', ' ').replace('.', ' ').replace('-', ' ').split() if p]
        if not parts:
            return 'U'
        if len(parts) == 1:
            return parts[0][0].upper()
        return f"{parts[0][0]}{parts[-1][0]}".upper()

    @property
    def initials(self):
        """Property shortcut for user initials."""
        return self.get_initials()

    def get_avatar_url(self):
        """Returns the avatar URL (uploaded image, external OAuth picture URL, or UI-Avatars dynamic avatar)."""
        if self.profile_image and self.profile_image != "default_avatar.png":
            if self.profile_image.startswith('http://') or self.profile_image.startswith('https://'):
                return self.profile_image
            return f"/static/uploads/{self.profile_image}"
        
        display_name = (self.full_name or '').strip()
        if not display_name or display_name.lower() in ['none', 'user']:
            if self.email and '@' in self.email:
                display_name = self.email.split('@')[0]
            else:
                display_name = 'User'
        
        encoded_name = urllib.parse.quote_plus(display_name)
        return f"https://ui-avatars.com/api/?name={encoded_name}&background=6366f1&color=fff&bold=true"

    def to_dict(self):
        """Serialize user object to dictionary."""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'target_role': self.target_role,
            'skills': self.skills,
            'profile_image': self.profile_image,
            'avatar_url': self.get_avatar_url(),
            'initials': self.get_initials(),
            'google_id': self.google_id
        }

    def __repr__(self):
        return f"<User id={self.id} email='{self.email}'>"
