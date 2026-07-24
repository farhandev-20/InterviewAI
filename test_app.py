import sys
import os

# Ensure project dir is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models.user import User
from services.user_service import UserService

def test_interviewai_phase1():
    print("=== Testing InterviewAI Phase 1 Core Systems ===")
    
    with app.test_client() as client:
        # 1. Test Landing Page
        res = client.get('/')
        assert res.status_code == 200, f"Landing page failed with status {res.status_code}"
        assert b"Prepare for Interviews with AI" in res.data, "Landing page content missing"
        print("[OK] Landing Page (HTTP 200) verified.")

        # 2. Test Login Page GET
        res = client.get('/login')
        assert res.status_code == 200, f"Login page failed with status {res.status_code}"
        assert b"Welcome Back" in res.data, "Login page content missing"
        print("[OK] Login Page GET (HTTP 200) verified.")

        # 3. Test Register Page GET
        res = client.get('/register')
        assert res.status_code == 200, f"Register page failed with status {res.status_code}"
        assert b"Create Your Account" in res.data, "Register page content missing"
        print("[OK] Register Page GET (HTTP 200) verified.")

        # 4. Test Registration POST
        test_email = "testuser@interviewai.com"
        test_pass = "SecurePass123!"
        
        # Clean up previous test user if exists
        with app.app_context():
            existing = User.query.filter_by(email=test_email).first()
            if existing:
                db.session.delete(existing)
                db.session.commit()

        res = client.post('/register', data={
            'full_name': 'Test Engineer',
            'email': test_email,
            'password': test_pass,
            'confirm_password': test_pass
        }, follow_redirects=True)
        
        assert res.status_code == 200, f"Registration failed with status {res.status_code}"
        assert b"Registration successful" in res.data, "Success message missing after registration"
        print("[OK] User Registration & Password Hashing verified.")

        # 5. Verify User in Database
        with app.app_context():
            user = User.query.filter_by(email=test_email).first()
            assert user is not None, "User not found in SQLite database"
            assert user.check_password(test_pass), "Password hash verification failed"
            print("[OK] Database Persistence & Password Hash Check verified.")

        # 6. Test Login POST
        res = client.post('/login', data={
            'email': test_email,
            'password': test_pass,
            'remember': 'on'
        }, follow_redirects=True)
        assert res.status_code == 200, f"Login failed with status {res.status_code}"
        assert b"Welcome back, Test Engineer" in res.data, "Dashboard welcome header missing after login"
        print("[OK] Authentication & Flask-Login Session redirect to Dashboard verified.")

        # 7. Test Profile View & Profile Update POST
        res = client.post('/profile', data={
            'full_name': 'Test Engineer Updated',
            'email': test_email,
            'target_role': 'Senior AI Systems Engineer',
            'skills': 'Python, Flask, PyTorch, SQL'
        }, follow_redirects=True)
        assert res.status_code == 200, f"Profile update failed with status {res.status_code}"
        assert b"Profile updated successfully" in res.data, "Profile update flash message missing"
        print("[OK] Profile Information Update verified.")

        # 8. Test Settings Page GET
        res = client.get('/settings')
        assert res.status_code == 200, f"Settings page failed with status {res.status_code}"
        assert b"Settings" in res.data, "Settings page content missing"
        print("[OK] Settings UI Page (HTTP 200) verified.")

        # 9. Test Logout
        res = client.get('/logout', follow_redirects=True)
        assert res.status_code == 200, f"Logout failed with status {res.status_code}"
        assert b"logged out safely" in res.data, "Logout message missing"
        print("[OK] Logout Session Cleanup verified.")

        # 10. Test Protected Route Access Control (Dashboard without login)
        res = client.get('/dashboard', follow_redirects=True)
        assert b"Please log in to access this page" in res.data or b"Welcome Back" in res.data, "Protected route failed"
        print("[OK] Protected Route Access Control verified.")

    print("\nALL 10 VERIFICATION TESTS PASSED SUCCESSFULLY!\n")

if __name__ == '__main__':
    test_interviewai_phase1()
