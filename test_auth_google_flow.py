import os
import sys
import json
import urllib.parse
from unittest.mock import patch, MagicMock

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models.user import User
from services.user_service import UserService

def test_display_name_resolution():
    print("=== 1. Testing Display Name Resolution & Fallback Hierarchy ===")
    
    # 1. Real Display Name
    assert UserService.resolve_display_name("Farhan Attar", "example@gmail.com") == "Farhan Attar"
    assert UserService.resolve_display_name("John Doe", "john@example.com") == "John Doe"
    assert UserService.resolve_display_name("Farhan", "farhan@example.com") == "Farhan"
    
    # 2. Rejection of Placeholder / Mock strings -> Fallback to email username
    assert UserService.resolve_display_name("Alex Candidate", "farhan.attar@gmail.com") == "Farhan Attar"
    assert UserService.resolve_display_name("Google Candidate", "sarah.connor@gmail.com") == "Sarah Connor"
    assert UserService.resolve_display_name("Google User", "attarfarhan02@gmail.com") == "Attarfarhan02"
    assert UserService.resolve_display_name(None, "john_smith@domain.com") == "John Smith"
    assert UserService.resolve_display_name("", "alex_candidate@domain.com") == "Alex Candidate"
    assert UserService.resolve_display_name(None, "user123@domain.com") == "User123"
    
    # 3. Complete fallback when neither name nor email available
    assert UserService.resolve_display_name(None, None) == "User"
    assert UserService.resolve_display_name("", "") == "User"
    print("[OK] Display Name Fallback Hierarchy verified successfully.")

def test_initials_and_avatar_generation():
    print("=== 2. Testing Dynamic Initials & Avatar Generation ===")
    
    u1 = User(full_name="Farhan Attar", email="farhan@gmail.com")
    assert u1.get_initials() == "FA", f"Expected FA, got {u1.get_initials()}"
    assert u1.initials == "FA"

    u2 = User(full_name="John Doe", email="johndoe@gmail.com")
    assert u2.get_initials() == "JD", f"Expected JD, got {u2.get_initials()}"

    u3 = User(full_name="Farhan", email="farhan@gmail.com")
    assert u3.get_initials() == "F", f"Expected F, got {u3.get_initials()}"

    u4 = User(full_name="", email="sarah.connor@gmail.com")
    assert u4.get_initials() == "SC", f"Expected SC, got {u4.get_initials()}"

    # Avatar URL with Google picture URL
    u_google = User(
        full_name="Farhan Attar",
        email="farhan@gmail.com",
        profile_image="https://lh3.googleusercontent.com/a/ACg8ocK..."
    )
    assert u_google.get_avatar_url() == "https://lh3.googleusercontent.com/a/ACg8ocK..."
    
    # Avatar URL default fallback to UI-Avatars
    u_default = User(full_name="Farhan Attar", email="farhan@gmail.com", profile_image="default_avatar.png")
    assert "https://ui-avatars.com/api/?name=Farhan+Attar" in u_default.get_avatar_url()

    print("[OK] Dynamic Initials & Avatar Generation verified successfully.")

def test_google_user_creation_and_uid_priority():
    print("=== 3. Testing Google User Creation & UID-First DB Resolution ===")
    
    with app.app_context():
        # Clean up any existing test user
        test_email = "farhan.oauth.test@gmail.com"
        test_gid = "google_uid_9988776655"
        
        existing = User.query.filter((User.email == test_email) | (User.google_id == test_gid)).all()
        for u in existing:
            db.session.delete(u)
        db.session.commit()

        # 1. Create Google User
        user = UserService.create_or_get_google_user(
            email=test_email,
            full_name="Farhan Attar",
            google_id=test_gid,
            picture_url="https://lh3.googleusercontent.com/a/farhan_pic.png"
        )
        assert user is not None
        assert user.full_name == "Farhan Attar"
        assert user.email == test_email
        assert user.google_id == test_gid
        assert user.profile_image == "https://lh3.googleusercontent.com/a/farhan_pic.png"
        user_id = user.id

        # 2. Retrieve same user by Google UID (even if email casing differs)
        user_by_uid = UserService.create_or_get_google_user(
            email=test_email.upper(),
            full_name="Farhan Attar",
            google_id=test_gid
        )
        assert user_by_uid.id == user_id
        assert user_by_uid.full_name == "Farhan Attar"

        print("[OK] Google User Creation & UID Priority verified successfully.")

def test_google_oauth_full_flow_and_dashboard():
    print("=== 4. Testing End-to-End Google OAuth Flow to Dashboard ===")

    with app.test_client() as client:
        test_email = "farhan.dashboard@gmail.com"
        test_gid = "google_uid_11223344"
        test_name = "Farhan Attar"

        with app.app_context():
            existing = User.query.filter_by(email=test_email).first()
            if existing:
                db.session.delete(existing)
            db.session.commit()

        # Mock Google Token & Userinfo HTTP requests in callback
        mock_tokens = json.dumps({'access_token': 'mock_access_token_xyz123'}).encode('utf-8')
        mock_userinfo = json.dumps({
            'sub': test_gid,
            'name': test_name,
            'given_name': 'Farhan',
            'family_name': 'Attar',
            'email': test_email,
            'picture': 'https://lh3.googleusercontent.com/a/farhan_profile.jpg'
        }).encode('utf-8')

        # Mock urllib.request.urlopen to simulate Google OAuth response
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_resp_tokens = MagicMock()
            mock_resp_tokens.read.return_value = mock_tokens
            mock_resp_tokens.__enter__.return_value = mock_resp_tokens

            mock_resp_userinfo = MagicMock()
            mock_resp_userinfo.read.return_value = mock_userinfo
            mock_resp_userinfo.__enter__.return_value = mock_resp_userinfo

            mock_urlopen.side_effect = [mock_resp_tokens, mock_resp_userinfo]

            os.environ['GOOGLE_CLIENT_ID'] = 'mock_google_client_id'
            os.environ['GOOGLE_CLIENT_SECRET'] = 'mock_google_secret'

            res = client.get('/google/callback?code=mock_oauth_code_123', follow_redirects=True)
            assert res.status_code == 200

            # Verify that the dashboard displays the actual Google user name and NOT "Alex Candidate"
            assert b"Welcome back, Farhan Attar!" in res.data, "Real Google account name missing from Dashboard"
            assert b"Alex Candidate" not in res.data, "Mock/Default 'Alex Candidate' was incorrectly displayed!"
            assert b"Farhan Attar" in res.data, "Profile name missing from top navigation"

            print("[OK] Google OAuth Callback successfully logged in user and displayed real name on Dashboard.")

        # Test authenticated Profile API
        api_res = client.get('/api/user/profile')
        assert api_res.status_code == 200
        user_json = api_res.get_json()['user']
        assert user_json['full_name'] == "Farhan Attar"
        assert user_json['email'] == test_email
        assert user_json['initials'] == "FA"
        assert user_json['avatar_url'] == "https://lh3.googleusercontent.com/a/farhan_profile.jpg"
        print("[OK] Authenticated Profile API (/api/user/profile) verified.")

        # Test Dashboard Refresh (GET /dashboard)
        refresh_res = client.get('/dashboard')
        assert refresh_res.status_code == 200
        assert b"Welcome back, Farhan Attar!" in refresh_res.data
        print("[OK] Dashboard refresh preserves authenticated user profile.")

def run_all_tests():
    test_display_name_resolution()
    test_initials_and_avatar_generation()
    test_google_user_creation_and_uid_priority()
    test_google_oauth_full_flow_and_dashboard()
    print("\nALL GOOGLE AUTH & USER PROFILE TESTS PASSED WITH 100% SUCCESS!\n")

if __name__ == '__main__':
    run_all_tests()
