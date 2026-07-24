import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models.user import User
from models.system import Notification, Achievement
from services.user_service import UserService
from services.system_service import SystemService
from services.interview_service import InterviewService

def test_interviewai_phase5():
    print("=== Testing InterviewAI Phase 5 Production Systems ===")

    with app.test_client() as client:
        test_email = "phase5_user@interviewai.com"
        test_pass = "ProductionPass123!"

        with app.app_context():
            u = User.query.filter_by(email=test_email).first()
            if u:
                db.session.delete(u)
            db.session.commit()

            user, _ = UserService.create_user("Phase5 Candidate", test_email, test_pass, "Lead Platform Architect")
            user_id = user.id

        print("[OK] Test user created.")

        # 1. Test System Service Notifications
        with app.app_context():
            n1 = SystemService.add_notification(user_id, "Welcome to Phase 5", "Production platform ready.", "info")
            assert n1 is not None, "Notification creation failed"
            unread = SystemService.get_unread_count(user_id)
            assert unread >= 1, "Unread count mismatch"
            print(f"[OK] Notification #{n1.id} created with unread count: {unread}")

        # 2. Test Gamified Achievements System
        with app.app_context():
            # Create dummy interview to unlock 'first_interview' badge
            inv = InterviewService.create_interview(user_id, "Python Lead", "Hard", "Technical", 5)
            InterviewService.complete_interview(inv.id)
            SystemService.check_and_unlock_achievements(user_id)

            achievements_count = Achievement.query.filter_by(user_id=user_id).count()
            assert achievements_count >= 1, "Achievement count zero"
            print(f"[OK] Gamified achievements verified with count: {achievements_count}")

        # 3. Test Web Routes Login & Notification API
        client.post('/login', data={'email': test_email, 'password': test_pass}, follow_redirects=True)
        print("[OK] User logged in.")

        # API: Notifications GET
        res = client.get('/api/notifications')
        assert res.status_code == 200, "Notification API failed"
        data = res.get_json()
        assert data['status'] == 'success', "Notification API status error"
        assert len(data['notifications']) >= 1, "Notification JSON list empty"
        print("[OK] Notification API GET endpoint verified.")

        # API: Read All POST
        res = client.post('/api/notifications/read-all')
        assert res.status_code == 200, "Read-all API failed"
        print("[OK] Mark Notifications Read-all API verified.")

        # Container Health Endpoint
        res = client.get('/health')
        assert res.status_code == 200, "Health check failed"
        assert b"healthy" in res.data, "Health status missing"
        print("[OK] Production Container /health check endpoint verified.")

        # Settings Voice Update POST
        res = client.post('/settings/update-voice', data={'voice_name': 'Google US English', 'speech_rate': '1.15'}, follow_redirects=True)
        assert res.status_code == 200, "Voice settings update failed"
        assert b"Voice preferences updated" in res.data, "Voice update toast missing"
        print("[OK] Voice Settings update endpoint verified.")

        # Analytics Page with Activity Heatmap GET
        res = client.get('/analytics')
        assert res.status_code == 200, "Analytics page GET failed"
        assert b"Practice Activity Heatmap" in res.data, "Heatmap grid content missing"
        print("[OK] Candidate Analytics & 30-Day Heatmap Page (HTTP 200) verified.")

    print("\nALL PHASE 5 VERIFICATION TESTS PASSED SUCCESSFULLY!\n")

if __name__ == '__main__':
    test_interviewai_phase5()
