import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models.user import User
from models.interview import Interview, Question
from services.user_service import UserService
from services.interview_service import InterviewService
from services.gemini_service import GeminiService
from services.question_bank import normalize_role, normalize_focus

def run_comprehensive_checks():
    print("=================================================================")
    print("STARTING COMPREHENSIVE QUESTION GENERATION FLOW VERIFICATION")
    print("=================================================================")

    with app.app_context():
        # Setup Test User
        test_email = "flow_verifier@interviewai.com"
        u = User.query.filter_by(email=test_email).first()
        if not u:
            u, _ = UserService.create_user("Flow Verifier", test_email, "Password123!", "Full Stack Developer")
        user_id = u.id

        # -------------------------------------------------------------
        # REPRESENTATIVE COMBINATION 1: Python Developer + Technical + Medium
        # -------------------------------------------------------------
        print("\n--- Testing Combination 1: Python Developer + Technical + Medium ---")
        q1_list = GeminiService.generate_ai_questions(
            role="Python Developer",
            difficulty="Medium",
            count=5,
            question_type="Technical"
        )
        assert len(q1_list) == 5, f"Expected 5 questions, got {len(q1_list)}"
        print(f"Generated {len(q1_list)} questions:")
        for idx, q in enumerate(q1_list, 1):
            print(f"  [{idx}] ({q['difficulty']}) [{q['topic']}]: {q['question']}")
            # Verify Python relevance
            q_text = q['question'].lower()
            assert any(w in q_text for w in ['python', 'gil', 'generator', 'decorator', 'asyncio', 'memory', 'concurrency', 'multiprocessing', 'type', 'list', 'dictionary', 'meta', 'pydantic', 'flask', 'django', 'fastapi', 'code', 'function', 'class', 'context manager', '__exit__', 'with']), f"Question does not sound like Python Developer: {q['question']}"
            assert not any(w in q_text for w in ['figma', 'wireframe', 'tell me about a time', 'conflict with a coworker']), f"Drift detected in Python Tech interview: {q['question']}"
        print("[PASS] Python Developer + Technical + Medium is authentic and strictly role-focused.")

        # -------------------------------------------------------------
        # REPRESENTATIVE COMBINATION 2: UI/UX Designer + Problem Solving + Easy
        # -------------------------------------------------------------
        print("\n--- Testing Combination 2: UI/UX Designer + Problem Solving + Easy ---")
        q2_list = GeminiService.generate_ai_questions(
            role="UI/UX Designer",
            difficulty="Easy",
            count=5,
            question_type="Problem Solving Interview"
        )
        assert len(q2_list) == 5, f"Expected 5 questions, got {len(q2_list)}"
        print(f"Generated {len(q2_list)} questions:")
        for idx, q in enumerate(q2_list, 1):
            print(f"  [{idx}] ({q['difficulty']}) [{q['topic']}]: {q['question']}")
            q_text = q['question'].lower()
            # Verify UI/UX problem solving focus
            assert any(w in q_text for w in ['user', 'ux', 'ui', 'drop-off', 'accessibility', 'mobile', 'onboarding', 'checkout', 'layout', 'design', 'conversion', 'test', 'friction']), f"Question does not sound like UI/UX Designer Problem Solving: {q['question']}"
            assert not any(w in q_text for w in ['python', 'docker', 'sql query', 'spring boot', 'kubernetes']), f"Drift detected in UI/UX interview: {q['question']}"
        print("[PASS] UI/UX Designer + Problem Solving + Easy is authentic and role-focused.")

        # -------------------------------------------------------------
        # REPRESENTATIVE COMBINATION 3: HR Interview + Behavioral + Medium
        # -------------------------------------------------------------
        print("\n--- Testing Combination 3: HR Interview + Behavioral + Medium ---")
        q3_list = GeminiService.generate_ai_questions(
            role="HR Interview",
            difficulty="Medium",
            count=5,
            question_type="Behavioral Interview"
        )
        assert len(q3_list) == 5, f"Expected 5 questions, got {len(q3_list)}"
        print(f"Generated {len(q3_list)} questions:")
        for idx, q in enumerate(q3_list, 1):
            print(f"  [{idx}] ({q['difficulty']}) [{q['topic']}]: {q['question']}")
            q_text = q['question'].lower()
            # Behavioral question requirement: ask about past experience using prompts like 'Tell me about a time'
            assert any(phrase in q_text for phrase in ['tell me about a time', 'describe a situation', 'can you share an example', 'give an example', 'share a situation']), f"Behavioral focus missing STAR prompt: {q['question']}"
            assert not any(w in q_text for w in ['git rebase', 'sql join', 'css grid', 'pytorch']), f"Drift detected in HR Behavioral interview: {q['question']}"
        print("[PASS] HR Interview + Behavioral + Medium is authentic and uses proper behavioral prompts.")

        # -------------------------------------------------------------
        # CHECK 4: All 9 Roles x 5 Focus Types
        # -------------------------------------------------------------
        print("\n--- Checking All 9 Roles x 5 Focus Types ---")
        roles = [
            "Python Developer", "Frontend Developer", "Backend Developer",
            "Full Stack Developer", "Java Developer", "UI/UX Designer",
            "Data Analyst", "Machine Learning Engineer", "HR Interview"
        ]
        focuses = [
            "Technical Interview", "HR Interview", "Behavioral Interview",
            "Scenario Based Interview", "Problem Solving Interview"
        ]

        total_tested = 0
        for r in roles:
            for f in focuses:
                res = GeminiService.generate_ai_questions(role=r, difficulty="Medium", count=5, question_type=f)
                assert len(res) == 5, f"Expected 5 questions for {r} / {f}, got {len(res)}"
                # Verify no duplicates
                texts = [item['question'].lower() for item in res]
                assert len(set(texts)) == 5, f"Duplicates detected in {r} / {f}"
                total_tested += 1
        print(f"[PASS] Verified all {total_tested} role-focus combinations return exactly 5 non-repeating questions.")

        # -------------------------------------------------------------
        # CHECK 5: Resume Grounding vs Hallucination Prevention
        # -------------------------------------------------------------
        print("\n--- Checking Resume-Tailored Questions Grounding ---")
        sample_resume = """
        Candidate: Sarah Chen
        Skills: React, Next.js, TypeScript, TailwindCSS, GraphQL
        Experience:
        Frontend Engineer @ FinTech Corp (2022 - Present)
        • Spearheaded financial dashboard redesign improving Lighthouse accessibility score from 68 to 98.
        Projects:
        • CryptoPortfolio Tracker: Real-time crypto asset tracker using Next.js and CoinGecko API.
        • Design System UI Library: Accessible component library for financial charts.
        """

        resume_q = GeminiService.generate_resume_interview_questions(
            resume_text=sample_resume,
            count=5,
            role="Frontend Developer",
            difficulty="Medium",
            interview_type="Technical Interview"
        )
        assert len(resume_q) == 5, f"Expected 5 resume questions, got {len(resume_q)}"
        print(f"Generated {len(resume_q)} resume questions:")
        for idx, q in enumerate(resume_q, 1):
            print(f"  [{idx}]: {q['question']}")
            # Must reference candidate's actual projects or skills
            q_text = q['question'].lower()
            assert any(term in q_text for term in ['cryptoportfolio tracker', 'design system ui library', 'fintech corp', 'react', 'next.js', 'typescript', 'graphql', 'accessibility']), f"Resume question not grounded in candidate's resume: {q['question']}"
        print("[PASS] Resume-tailored questions are strictly grounded in candidate's actual projects and tools.")

        # -------------------------------------------------------------
        # CHECK 6: Resume-Tailored Fallback when no resume is uploaded
        # -------------------------------------------------------------
        print("\n--- Checking Resume-Tailored Fallback when no resume is present ---")
        empty_resume_q = GeminiService.generate_resume_interview_questions(
            resume_text="",
            count=5,
            role="Backend Developer",
            difficulty="Hard",
            interview_type="Scenario Based Interview"
        )
        assert len(empty_resume_q) == 5, f"Expected 5 questions, got {len(empty_resume_q)}"
        print(f"Generated {len(empty_resume_q)} role-based fallback questions:")
        for idx, q in enumerate(empty_resume_q, 1):
            print(f"  [{idx}]: {q['question']}")
            assert any(w in q['question'].lower() for w in ['service', 'traffic', 'database', 'api', 'outage', 'circuit', 'queue', 'redis', 'deadlock', 'dependency', 'scenario']), f"Question not relevant to Backend Scenario: {q['question']}"
        print("[PASS] Graceful fallback to role-based questions when resume is absent verified.")

        # -------------------------------------------------------------
        # CHECK 7: Full Interview Session Creation Across Text, Voice, Video Modes
        # -------------------------------------------------------------
        print("\n--- Checking Interview Modes (Text, Voice, Video) Persistence ---")
        for mode in ['text', 'voice', 'video']:
            inv = InterviewService.create_interview(
                user_id=user_id,
                role="Machine Learning Engineer",
                difficulty="Hard",
                interview_type="Problem Solving Interview",
                count=5,
                mode=mode
            )
            assert inv.mode == mode, f"Mode mismatch: expected {mode}, got {inv.mode}"
            assert len(inv.questions) == 5, f"Expected 5 questions in DB, got {len(inv.questions)}"
            print(f"  Mode '{mode}': Interview #{inv.id} created with 5 questions.")
        print("[PASS] All modes created consistently with exact question count.")

        # -------------------------------------------------------------
        # CHECK 8: Question Counts (5, 10, 15, 20)
        # -------------------------------------------------------------
        print("\n--- Checking Question Counts: 5, 10, 15, 20 ---")
        for c in [5, 10, 15, 20]:
            questions = GeminiService.generate_ai_questions(
                role="Full Stack Developer",
                difficulty="Medium",
                count=c,
                question_type="Technical Interview"
            )
            assert len(questions) == c, f"Expected {c} questions, got {len(questions)}"
            unique_q = {q['question'].lower() for q in questions}
            assert len(unique_q) == c, f"Duplicates found in count {c}: {len(unique_q)} unique out of {c}"
            print(f"  Count {c}: Successfully generated {c} distinct, non-repeating questions.")
        print("[PASS] All question counts generated without duplicates.")

    print("\n=================================================================")
    print("ALL COMPREHENSIVE QUESTION FLOW CHECKS PASSED WITH ZERO ERRORS!")
    print("=================================================================")

if __name__ == '__main__':
    run_comprehensive_checks()
