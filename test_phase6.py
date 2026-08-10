import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models.user import User
from models.interview import Interview
from services.user_service import UserService
from services.interview_service import InterviewService
from services.gemini_service import GeminiService

def test_interviewai_phase6_upgrades():
    print("=== Testing InterviewAI Phase 6 Modern Platform Upgrades ===")

    with app.test_client() as client:
        test_email = "google_candidate@example.com"

        # 1. Test Google OAuth User Creation & Login Endpoint
        with app.app_context():
            u = User.query.filter_by(email=test_email).first()
            if u:
                db.session.delete(u)
            db.session.commit()

            google_user = UserService.create_or_get_google_user(
                email=test_email,
                full_name="Google Candidate",
                google_id="g_123456789"
            )
            assert google_user is not None, "Google user creation failed"
            assert google_user.google_id == "g_123456789", "Google ID mismatch"
            print("[OK] Google OAuth User Registration & DB Schema verified.")

        res = client.get('/google_login', follow_redirects=False)
        assert res.status_code in (302, 200), f"Google login endpoint failed with status {res.status_code}"
        print("[OK] Continue with Google Authentication endpoint verified.")

        # Test prompt=select_account parameter when GOOGLE_CLIENT_ID is set
        os.environ['GOOGLE_CLIENT_ID'] = 'test_google_client_id_123'
        res_oauth = client.get('/google_login', follow_redirects=False)
        assert res_oauth.status_code == 302
        assert 'prompt=select_account' in res_oauth.location, f"Expected prompt=select_account in redirect location: {res_oauth.location}"
        del os.environ['GOOGLE_CLIENT_ID']
        print("[OK] Google Account Chooser (prompt=select_account) parameter verified.")

        # 2. Test Interview Creation for 3 Modes (Text, Voice, Video)
        with app.app_context():
            inv_text = InterviewService.create_interview(
                user_id=google_user.id,
                role="Python Developer",
                difficulty="Easy",
                interview_type="Technical",
                count=3,
                mode="text"
            )
            inv_voice = InterviewService.create_interview(
                user_id=google_user.id,
                role="Frontend Developer",
                difficulty="Medium",
                interview_type="HR",
                count=3,
                mode="voice"
            )
            inv_video = InterviewService.create_interview(
                user_id=google_user.id,
                role="Lead Architect",
                difficulty="Hard",
                interview_type="Behavioral",
                count=3,
                mode="video"
            )

            assert inv_text.mode == "text", "Text mode mismatch"
            assert inv_voice.mode == "voice", "Voice mode mismatch"
            assert inv_video.mode == "video", "Video mode mismatch"
            video_inv_id = inv_video.id
            print("[OK] 3 Interview Modes (Text, Voice, Video) model persistence verified.")

        # Log in user for protected route access
        with client.session_transaction() as sess:
            sess['_user_id'] = str(google_user.id)
            sess['_fresh'] = True

        # 3. Test Video Mode Live Runner Page (Webcam & Live Transcript UI)
        res = client.get(f'/interview/{video_inv_id}/live?q=1')
        assert res.status_code == 200, "Video mode live GET failed"
        assert b"webcam-preview" in res.data, "Webcam preview missing in Video mode"
        assert b"live-transcript" in res.data, "Live transcript area missing in Video mode"
        print("[OK] Video Mode Live Room with Webcam Preview & Speech Transcript verified.")

        # 4. Test Dynamic AI Follow-up Endpoint
        res = client.post(f'/interview/{video_inv_id}/follow-up', json={
            'question_text': 'Explain microservices architecture.',
            'answer': 'Microservices decouple monolithic applications into smaller independent services.'
        })
        assert res.status_code == 200, "Follow-up API failed"
        json_data = res.get_json()
        assert json_data['status'] == 'success', "Follow-up status failed"
        assert 'followup' in json_data and len(json_data['followup']) > 0, "Followup text missing"
        print(f"[OK] Dynamic AI Follow-up API verified: \"{json_data['followup'][:60]}...\"")

    print("\nALL PHASE 6 PLATFORM UPGRADE VERIFICATION TESTS PASSED SUCCESSFULLY!\n")

if __name__ == '__main__':
    test_interviewai_phase6_upgrades()
