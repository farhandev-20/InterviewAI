from datetime import datetime, timedelta
from database.db import db
from models.system import Notification, Achievement
from models.interview import Interview
from models.resume import Resume, ResumeAnalysis

class SystemService:
    @staticmethod
    def add_notification(user_id, title, message, n_type='info'):
        """Creates an in-app notification for the user."""
        n = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=n_type,
            is_read=False
        )
        db.session.add(n)
        db.session.commit()
        return n

    @staticmethod
    def get_user_notifications(user_id, limit=10):
        """Retrieves user's notifications."""
        return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_unread_count(user_id):
        """Counts unread notifications."""
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()

    @staticmethod
    def mark_all_notifications_read(user_id):
        """Marks all notifications for user as read."""
        Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
        db.session.commit()

    @staticmethod
    def calculate_practice_streak(user_id):
        """Calculates current consecutive practice days streak."""
        interviews = Interview.query.filter_by(user_id=user_id, status='completed').order_by(Interview.start_time.desc()).all()
        if not interviews:
            return 0

        dates = sorted(list(set(inv.start_time.date() for inv in interviews)), reverse=True)
        today = datetime.utcnow().date()
        
        # Check if user practiced today or yesterday
        if dates[0] < today - timedelta(days=1):
            return 0

        streak = 0
        current_date = dates[0]
        for d in dates:
            if d == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        return streak

    @staticmethod
    def check_and_unlock_achievements(user_id):
        """
        Evaluates user activity and unlocks gamified achievements.
        """
        unlocked = []

        # Helper to check if already unlocked
        existing_keys = set(a.badge_key for a in Achievement.query.filter_by(user_id=user_id).all())

        completed_interviews = Interview.query.filter_by(user_id=user_id, status='completed').all()
        completed_count = len(completed_interviews)
        resumes = Resume.query.filter_by(user_id=user_id).all()
        analyses = ResumeAnalysis.query.join(Resume).filter(Resume.user_id == user_id).all()

        # Badge 1: First Interview
        if completed_count >= 1 and 'first_interview' not in existing_keys:
            a = Achievement(
                user_id=user_id,
                badge_key='first_interview',
                title='First Step',
                description='Completed your first AI mock interview session.',
                icon='fas fa-flag-checkered'
            )
            db.session.add(a)
            unlocked.append(a)
            SystemService.add_notification(user_id, "Achievement Unlocked! 🏆", "You earned the 'First Step' badge!", "success")

        # Badge 2: 10 Interviews
        if completed_count >= 10 and 'ten_interviews' not in existing_keys:
            a = Achievement(
                user_id=user_id,
                badge_key='ten_interviews',
                title='Practice Veteran',
                description='Completed 10 AI mock interview practice sessions.',
                icon='fas fa-medal'
            )
            db.session.add(a)
            unlocked.append(a)
            SystemService.add_notification(user_id, "Achievement Unlocked! 🏆", "You earned the 'Practice Veteran' badge!", "success")

        # Badge 3: High Score (90+)
        has_high_score = any(inv.score >= 90.0 for inv in completed_interviews)
        if has_high_score and 'high_score' not in existing_keys:
            a = Achievement(
                user_id=user_id,
                badge_key='high_score',
                title='Top Performer',
                description='Scored 90% or higher in an interview session.',
                icon='fas fa-star'
            )
            db.session.add(a)
            unlocked.append(a)
            SystemService.add_notification(user_id, "Achievement Unlocked! 🌟", "You earned the 'Top Performer' badge!", "success")

        # Badge 4: Resume Uploaded
        if len(resumes) >= 1 and 'resume_uploaded' not in existing_keys:
            a = Achievement(
                user_id=user_id,
                badge_key='resume_uploaded',
                title='Resume Ready',
                description='Uploaded a resume for ATS compliance auditing.',
                icon='fas fa-file-check'
            )
            db.session.add(a)
            unlocked.append(a)

        # Badge 5: Perfect ATS (90+)
        has_high_ats = any(an.ats_score >= 90.0 for an in analyses)
        if has_high_ats and 'perfect_ats' not in existing_keys:
            a = Achievement(
                user_id=user_id,
                badge_key='perfect_ats',
                title='ATS Master',
                description='Achieved a 90%+ ATS resume score.',
                icon='fas fa-award'
            )
            db.session.add(a)
            unlocked.append(a)

        db.session.commit()
        return unlocked
