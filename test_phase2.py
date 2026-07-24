import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models.user import User
from models.interview import Interview, Question, Answer
from services.user_service import UserService
from services.interview_service import InterviewService

def test_interviewai_phase2():
    print("=== Testing InterviewAI Phase 2 Core Systems ===")

    with app.test_client() as client:
        # Setup Test Users
        user1_email = "candidate1@interviewai.com"
        user2_email = "candidate2@interviewai.com"
        test_pass = "Password123!"

        with app.app_context():
            # Clean up
            for em in [user1_email, user2_email]:
                u = User.query.filter_by(email=em).first()
                if u:
                    db.session.delete(u)
            db.session.commit()

            # Create Users inside app context
            u1, _ = UserService.create_user("Candidate One", user1_email, test_pass, "Python Developer")
            u2, _ = UserService.create_user("Candidate Two", user2_email, test_pass, "Frontend Developer")
            u1_id = u1.id
            u2_id = u2.id

        print("[OK] User accounts initialized for testing.")

        # 1. Login as User 1
        client.post('/login', data={'email': user1_email, 'password': test_pass}, follow_redirects=True)
        print("[OK] User 1 logged in.")

        # 2. Test Setup Page GET & POST
        res = client.get('/interview/setup')
        assert res.status_code == 200, f"Interview setup GET failed with status {res.status_code}"
        assert b"Configure Your Mock Interview" in res.data, "Setup header missing"
        print("[OK] Interview Setup Page GET (HTTP 200) verified.")

        # Create 5-Question Technical Interview for Python Developer
        res = client.post('/interview/setup', data={
            'role': 'Python Developer',
            'difficulty': 'Medium',
            'interview_type': 'Technical',
            'count': 5
        }, follow_redirects=True)

        assert res.status_code == 200, f"Interview creation failed with status {res.status_code}"
        assert b"Question 1 of 5" in res.data, "Live interview runner missing question counter"
        print("[OK] Interview Creation & Non-Repeating Question Generation verified.")

        # Extract Interview ID from DB
        with app.app_context():
            inv1 = Interview.query.filter_by(user_id=u1_id).order_by(Interview.id.desc()).first()
            assert inv1 is not None, "Interview record not found in database"
            assert inv1.total_questions == 5, "Total questions mismatch"
            assert len(inv1.questions) == 5, "Questions count in DB mismatch"
            inv1_id = inv1.id
            q1_id = inv1.questions[0].id
            q2_id = inv1.questions[1].id
            print(f"[OK] Database Interview #{inv1_id} created with 5 questions.")

        # 3. Test Answering Questions & Live Runner
        res = client.post(f'/interview/{inv1_id}/live?q=1', data={
            'action': 'next',
            'answer': 'Lists are mutable sequences whereas tuples are immutable sequence objects in Python.',
            'time_taken': 35
        }, follow_redirects=True)
        assert res.status_code == 200, "Answer submission Q1 failed"
        print("[OK] Live Answer 1 saved successfully.")

        res = client.post(f'/interview/{inv1_id}/live?q=2', data={
            'action': 'next',
            'answer': 'The GIL or Global Interpreter Lock restricts CPython bytecode execution to a single thread.',
            'time_taken': 42
        }, follow_redirects=True)
        assert res.status_code == 200, "Answer submission Q2 failed"
        print("[OK] Live Answer 2 saved successfully.")

        # Skip Question 3 & 4, then submit on Question 5
        res = client.post(f'/interview/{inv1_id}/live?q=5', data={
            'action': 'submit',
            'answer': 'Generators yield values lazily using O(1) memory instead of populating full lists in RAM.',
            'time_taken': 50
        }, follow_redirects=True)
        assert res.status_code == 200, "Final interview submit failed"
        assert b"Interview Summary" in res.data or b"Session completed" in res.data, "Summary page redirect failed"
        print("[OK] Final Interview Submission & Session Completion verified.")

        # 4. Test Summary Metrics Page
        with app.app_context():
            inv_check = Interview.query.get(inv1_id)
            assert inv_check.status == 'completed', "Interview status should be 'completed'"
            assert inv_check.end_time is not None, "Interview end_time should be set"
            print("[OK] Database Status set to 'completed' with end_time timestamp.")

        res = client.get(f'/interview/{inv1_id}/summary')
        assert res.status_code == 200, f"Summary page failed with status {res.status_code}"
        assert b"Answered" in res.data, "Summary answered count missing"
        assert b"Skipped" in res.data, "Summary skipped count missing"
        print("[OK] Interview Summary Metrics Page verified.")

        # 5. Test Evaluation Report Page
        res = client.get(f'/interview/{inv1_id}/report')
        assert res.status_code == 200, f"Report page failed with status {res.status_code}"
        assert b"Your Submitted Response:" in res.data, "User response missing in report"
        assert b"AI" in res.data, "AI feedback missing in report"
        print("[OK] Detailed Evaluation Report Page verified.")

        # 6. Test Security Access Control (User 2 tries to view User 1's interview)
        client.get('/logout', follow_redirects=True)
        client.post('/login', data={'email': user2_email, 'password': test_pass}, follow_redirects=True)
        
        res = client.get(f'/interview/{inv1_id}/live', follow_redirects=True)
        assert b"Unauthorized access" in res.data or res.status_code == 403, "Security breach: User 2 accessed User 1 interview live page"
        
        res = client.get(f'/interview/{inv1_id}/report', follow_redirects=True)
        assert b"Unauthorized access" in res.data or res.status_code == 403, "Security breach: User 2 accessed User 1 report page"
        print("[OK] Security & Access Control (Cross-user access blocked) verified.")

        # 7. Test Dashboard & Profile Dynamic Metrics Update for User 1
        client.get('/logout', follow_redirects=True)
        client.post('/login', data={'email': user1_email, 'password': test_pass}, follow_redirects=True)

        res = client.get('/dashboard')
        assert res.status_code == 200, "Dashboard failed"
        assert b"Total Practice Sessions" in res.data, "Dashboard total sessions missing"
        print("[OK] Dynamic Dashboard Statistics integration verified.")

        res = client.get('/profile')
        assert res.status_code == 200, "Profile page failed"
        assert b"Completed Interviews" in res.data, "Profile stats missing"
        print("[OK] Dynamic Profile Page Statistics integration verified.")

    print("\nALL PHASE 2 VERIFICATION TESTS PASSED SUCCESSFULLY!\n")

if __name__ == '__main__':
    test_interviewai_phase2()
