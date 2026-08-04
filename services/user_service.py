import os
from werkzeug.utils import secure_filename
from database.db import db
from models.user import User

class UserService:
    @staticmethod
    def get_by_id(user_id):
        """Retrieve user by ID."""
        return User.query.get(int(user_id))

    @staticmethod
    def get_by_email(email):
        """Retrieve user by email (case-insensitive)."""
        if not email:
            return None
        return User.query.filter(User.email.ilike(email.strip())).first()

    @staticmethod
    def create_user(full_name, email, password, target_role="Full Stack Developer", skills="Python, SQL"):
        """Create and register a new user in the database."""
        email_clean = email.strip().lower()
        if UserService.get_by_email(email_clean):
            return None, "Email address is already registered."

        user = User(
            full_name=full_name.strip(),
            email=email_clean,
            target_role=target_role,
            skills=skills
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user, None

    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user credentials."""
        user = UserService.get_by_email(email)
        if not user:
            return None, "Invalid email or password."
        if not user.check_password(password):
            return None, "Invalid email or password."
        
        user.update_last_login()
        return user, None

    @staticmethod
    def create_or_get_google_user(email, full_name, google_id=None):
        """Authenticate or register user via Google OAuth while preserving existing accounts."""
        email_clean = email.strip().lower()
        user = UserService.get_by_email(email_clean)
        if user:
            if google_id and not user.google_id:
                user.google_id = google_id
            user.update_last_login()
            db.session.commit()
            return user

        user = User(
            full_name=full_name.strip() if full_name else "Google Candidate",
            email=email_clean,
            google_id=google_id or f"google_{int(os.path.getmtime(__file__))}",
            target_role="Software Engineer",
            skills="Python, Web Development, Problem Solving"
        )
        user.set_password(f"google_oauth_dummy_{int(os.path.getmtime(__file__))}")
        db.session.add(user)
        db.session.commit()
        user.update_last_login()
        return user

    @staticmethod
    def update_profile(user_id, full_name, email, target_role, skills, file_obj=None, upload_folder=None, allowed_extensions=None):
        """Update user profile information and profile photo."""
        user = UserService.get_by_id(user_id)
        if not user:
            return False, "User not found."

        # Check if email changed and if new email is taken
        email_clean = email.strip().lower()
        if email_clean != user.email:
            existing = UserService.get_by_email(email_clean)
            if existing and existing.id != user.id:
                return False, "Email address is already in use by another account."
            user.email = email_clean

        user.full_name = full_name.strip()
        user.target_role = target_role.strip() if target_role else ""
        user.skills = skills.strip() if skills else ""

        # Handle Profile Photo Upload if present
        if file_obj and file_obj.filename:
            filename = secure_filename(file_obj.filename)
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            if allowed_extensions and ext not in allowed_extensions:
                return False, f"Invalid file format. Allowed extensions: {', '.join(allowed_extensions)}"
            
            new_filename = f"user_{user.id}_{int(os.path.getmtime(__file__))}.{ext}"
            os.makedirs(upload_folder, exist_ok=True)
            save_path = os.path.join(upload_folder, new_filename)
            file_obj.save(save_path)
            user.profile_image = new_filename

        db.session.commit()
        return True, "Profile updated successfully."
