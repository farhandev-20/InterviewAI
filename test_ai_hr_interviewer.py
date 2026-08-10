import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models.user import User
from models.interview import Interview, Question, Answer, AIFeedback
from services.user_service import UserService
from services.interview_service import InterviewService
from services.gemini_service import GeminiService

def test_ai_hr_interviewer_full_flow():
    print("=== Testing AI HR Interviewer & Automated Adaptive Flow ===")

    with app.test_client() as client:
        test_email = "ai_hr_candidate@example.com"

        # 1. Create Test User
        with app.app_context():
            u = User.query.filter_by(email=test_email).first()
            if u:
                db.session.delete(u)
            db.session.commit()

            user, err = UserService.create_user(
                full_name="Alex Mercer",
                email=test_email,
                password="SecurePassword123!"
            )
            assert user is not None, f"User creation failed: {err}"
            user_id = user.id


            # 2. Initialize 3-Question Video Interview
            interview = InterviewService.create_interview(
                user_id=user_id,
                role="Machine Learning Engineer",
                difficulty="Medium",
                interview_type="Technical",
                count=3,
                mode="video"
            )
            assert interview.mode == "video", "Interview mode not video"
            assert len(interview.questions) >= 1, "Interview has no questions"
            inv_id = interview.id
            q1_id = interview.questions[0].id
            print(f"[OK] Video Interview #{inv_id} initialized with {len(interview.questions)} questions.")

        # Log in test user
        with client.session_transaction() as sess:
            sess['_user_id'] = str(user_id)
            sess['_fresh'] = True

        # 3. Test Live Interview Page Rendering with AI HR Stage
        res = client.get(f'/interview/{inv_id}/live?q=1')
        assert res.status_code == 200, f"Live interview page failed: {res.status_code}"
        assert b"ai-stage-container" in res.data, "AI HR stage container missing in DOM"
        assert b"webcam-preview" in res.data, "Webcam preview missing in DOM"
        assert b"live-transcript" in res.data, "Live transcript box missing in DOM"
        assert b"Sophia" in res.data, "AI HR nameplate missing in DOM"
        print("[OK] Video Interview screen with AI HR Avatar Stage & Webcam layout verified.")

        # 4. Test Automated Turn 1 (Candidate answers mentioning ML & Python)
        answer_text_1 = "I am a Machine Learning Engineer with 3 years of experience in Python, PyTorch, and deploying transformer models using FastAPI."
        res = client.post(f'/interview/{inv_id}/turn', json={
            'question_id': q1_id,
            'answer': answer_text_1,
            'time_taken': 35
        })
        assert res.status_code == 200, f"Turn 1 endpoint failed: {res.status_code}"
        data1 = res.get_json()
        assert data1['status'] == 'success', "Turn 1 status not success"
        assert data1['completed'] is False, "Turn 1 should not be completed"
        assert 'next_question' in data1, "Next question data missing"
        q2_id = data1['next_question']['id']
        print(f"[OK] Turn 1 processed: AI evaluated answer (Score: {data1['evaluation']['overall_score']}%) & generated Question 2: \"{data1['next_question']['question_text'][:60]}...\"")

        # 5. Test Turn 2 (Candidate answers Question 2)
        answer_text_2 = "For latency optimization, we implemented ONNX runtime quantization, Redis in-memory caching, and GPU batching which reduced inference latency by 45%."
        res = client.post(f'/interview/{inv_id}/turn', json={
            'question_id': q2_id,
            'answer': answer_text_2,
            'time_taken': 40
        })
        assert res.status_code == 200, f"Turn 2 endpoint failed: {res.status_code}"
        data2 = res.get_json()
        assert data2['status'] == 'success'
        assert data2['completed'] is False
        q3_id = data2['next_question']['id']
        print(f"[OK] Turn 2 processed: AI evaluated answer & adapted to Question 3: \"{data2['next_question']['question_text'][:60]}...\"")

        # 6. Test Final Turn 3 (Completes interview)
        answer_text_3 = "When designing distributed training clusters, we use PyTorch DDP with NCCL backends and gradient accumulation to scale across multi-node setups."
        res = client.post(f'/interview/{inv_id}/turn', json={
            'question_id': q3_id,
            'answer': answer_text_3,
            'time_taken': 30
        })
        assert res.status_code == 200, f"Turn 3 endpoint failed: {res.status_code}"
        data3 = res.get_json()
        assert data3['status'] == 'success'
        assert data3['completed'] is True, "Interview should be marked completed on final question"
        assert 'redirect_url' in data3, "Redirect URL missing on completion"
        print(f"[OK] Final Turn processed: Interview completed with overall score {data3['overall_score']}%.")

        # 7. Test Evaluation Report Page
        res = client.get(f'/interview/{inv_id}/report')
        assert res.status_code == 200, "Report page GET failed"
        assert b"AI Interview Evaluation Report" in res.data, "Report title missing"
        assert b"5-Metric Competency Scores" in res.data, "Competency scores section missing"
        print("[OK] Comprehensive AI Evaluation Report rendered successfully.")

    print("\nALL AI HR INTERVIEWER & AUTOMATED ADAPTIVE FLOW TESTS PASSED SUCCESSFULLY!\n")

if __name__ == '__main__':
    test_ai_hr_interviewer_full_flow()
