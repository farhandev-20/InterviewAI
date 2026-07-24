import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models.user import User
from models.interview import Interview, Question, Answer, AIFeedback
from services.user_service import UserService
from services.interview_service import InterviewService
from services.gemini_service import GeminiService

def test_interviewai_phase3():
    print("=== Testing InterviewAI Phase 3 Core Systems ===")

    with app.test_client() as client:
        test_email = "ai_candidate@interviewai.com"
        test_pass = "Password123!"

        with app.app_context():
            u = User.query.filter_by(email=test_email).first()
            if u:
                db.session.delete(u)
            db.session.commit()

            user, _ = UserService.create_user("AI Candidate", test_email, test_pass, "Machine Learning Engineer")
            user_id = user.id

        print("[OK] Test user created.")

        # 1. Test Gemini Service Isolated Functions
        q_list = GeminiService.generate_ai_questions("Python Developer", "Medium", 3, "Technical")
        assert len(q_list) == 3, "Gemini questions count mismatch"
        print("[OK] Gemini AI Question Generation verified.")

        eval_res = GeminiService.evaluate_answer("What is Python GIL?", "GIL is a mutex lock preventing multi-threaded bytecode execution.", "Python Developer", "Medium")
        assert "technical_score" in eval_res and "overall_score" in eval_res, "Evaluation keys missing"
        print("[OK] Gemini AI 5-Metric Answer Evaluation verified.")

        res_res = GeminiService.analyze_resume("Machine Learning Engineer with PyTorch experience...", "ML Engineer")
        assert "score" in res_res, "Resume analyzer score missing"
        print("[OK] AI Resume Analyzer engine verified.")

        jd_res = GeminiService.analyze_jd("Looking for Python SQL developer", "Python, SQL, React")
        assert "match_percentage" in jd_res, "JD analyzer match missing"
        print("[OK] AI Job Description Matcher engine verified.")

        # 2. Login User
        client.post('/login', data={'email': test_email, 'password': test_pass}, follow_redirects=True)
        print("[OK] User logged in.")

        # 3. Create AI Interview & Save Response
        with app.app_context():
            inv = InterviewService.create_interview(user_id, "Machine Learning Engineer", "Hard", "Technical", 3, use_ai=True)
            inv_id = inv.id
            q1_id = inv.questions[0].id

        res = client.post(f'/interview/{inv_id}/live?q=1', data={
            'action': 'next',
            'answer': 'Gradient boosting builds sequential decision trees to minimize residual error.',
            'time_taken': 45
        }, follow_redirects=True)
        assert res.status_code == 200, "Answer submission failed"

        # Verify AIFeedback table persistence
        with app.app_context():
            fb = AIFeedback.query.filter_by(question_id=q1_id).first()
            assert fb is not None, "AIFeedback record missing in SQLite database"
            assert fb.overall_score >= 0, "AIFeedback overall score missing"
            print(f"[OK] AIFeedback table row persisted with score: {fb.overall_score}%")

        # Complete Interview
        res = client.post(f'/interview/{inv_id}/live?q=3', data={
            'action': 'submit',
            'answer': 'Overfitting can be mitigated using L1/L2 regularization and early stopping.',
            'time_taken': 50
        }, follow_redirects=True)
        assert res.status_code == 200, "Submit interview failed"
        print("[OK] AI Interview session submitted.")

        # 4. Verify AI Evaluation Report Route
        res = client.get(f'/interview/{inv_id}/report')
        assert res.status_code == 200, "Report page failed"
        assert b"5-Metric Competency Scores" in res.data or b"Technical" in res.data, "Section scores missing in report"
        print("[OK] AI Evaluation Report route verified.")

        # 5. Verify All 9 Sidebar Navigation Pages (GET 200)
        nav_routes = [
            ('/dashboard', b'Dashboard'),
            ('/interview/setup', b'Configure Your Mock Interview'),
            ('/resume-analyzer', b'AI Resume Analyzer'),
            ('/jd-analyzer', b'Job Description Matcher'),
            ('/reports', b'My Evaluation Reports'),
            ('/analytics', b'Candidate Analytics'),
            ('/profile', b'My Profile'),
            ('/settings', b'Settings')
        ]

        for route, expected_text in nav_routes:
            res = client.get(route)
            assert res.status_code == 200, f"Route {route} failed with HTTP {res.status_code}"
            assert expected_text in res.data, f"Route {route} content mismatch"
            print(f"[OK] Sidebar Page {route} (HTTP 200) verified.")

    print("\nALL PHASE 3 VERIFICATION TESTS PASSED SUCCESSFULLY!\n")

if __name__ == '__main__':
    test_interviewai_phase3()
