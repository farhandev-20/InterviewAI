import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models.user import User
from models.resume import Resume, ResumeAnalysis, JobDescription, ResumeJobMatch, SkillGap
from services.user_service import UserService
from services.resume_service import ResumeService
from services.interview_service import InterviewService
from services.gemini_service import GeminiService
from utils.file_parser import extract_text_from_file

def test_interviewai_phase4():
    print("=== Testing InterviewAI Phase 4 Core Systems ===")

    with app.test_client() as client:
        test_email = "resume_candidate@interviewai.com"
        test_pass = "Password123!"

        with app.app_context():
            u = User.query.filter_by(email=test_email).first()
            if u:
                db.session.delete(u)
            db.session.commit()

            user, _ = UserService.create_user("Resume Candidate", test_email, test_pass, "Senior Full Stack Engineer")
            user_id = user.id

        print("[OK] Test user created.")

        # 1. Test Resume Service & ATS Audit
        resume_text_sample = """
        John Doe - Senior Software Engineer
        Email: john@example.com | Phone: (555) 019-2834 | Portfolio: github.com/johndoe
        
        SKILLS:
        Python, Flask, Django, SQL, PostgreSQL, HTML5, CSS3, JavaScript, React, Git, Docker, REST APIs
        
        EXPERIENCE:
        Senior Full Stack Engineer @ Tech Solutions (2021 - Present)
        • Architected microservices platform handling 50k daily active users.
        • Optimized SQL database queries reducing latency by 35%.
        • Led team of 4 software engineers in agile sprints.
        
        PROJECTS:
        • Smart Parking System: Built IoT dashboard using Python, Flask, and React.
        • E-Commerce Analytics Engine: Real-time event streaming pipeline.
        
        EDUCATION:
        B.S. in Computer Science - State University
        """

        with app.app_context():
            resume, analysis, err = ResumeService.save_and_analyze_resume(
                user_id=user_id,
                raw_text_input=resume_text_sample,
                target_role="Senior Full Stack Engineer"
            )
            assert err is None, f"Resume analysis failed with error: {err}"
            assert resume is not None, "Resume DB record missing"
            assert analysis is not None, "ResumeAnalysis DB record missing"
            assert analysis.ats_score > 0, "ATS score missing"
            resume_id = resume.id
            analysis_id = analysis.id
            print(f"[OK] Resume #{resume_id} saved and ATS Analysis #{analysis_id} computed with score: {analysis.ats_score}%")

        # 2. Test Job Description Matching & Skill Gap Analysis
        jd_sample = """
        Job Title: Senior Backend Developer
        Company: CloudCorp Inc.
        Requirements:
        Must have strong experience with Python, SQL, REST APIs, Docker, and Redis caching.
        Preferred skills: Kubernetes, AWS, GraphQL, CI/CD pipeline automation.
        Responsibilities: Build scalable cloud APIs and optimize microservices.
        """

        with app.app_context():
            match, gap, err = ResumeService.match_resume_with_jd(
                user_id=user_id,
                resume_id=resume_id,
                jd_raw_text=jd_sample
            )
            assert err is None, f"JD matching failed: {err}"
            assert match is not None, "ResumeJobMatch record missing"
            assert gap is not None, "SkillGap record missing"
            assert match.overall_match_pct > 0, "Match percentage missing"
            print(f"[OK] Resume vs JD Match computed: {match.overall_match_pct}% (Hiring Probability: {match.hiring_probability})")

        # 3. Test Resume-Based Personalized Interview Generation
        with app.app_context():
            personalized_q = GeminiService.generate_resume_interview_questions(resume_text_sample, jd_sample, 3)
            assert len(personalized_q) == 3, "Personalized question count mismatch"
            assert "question" in personalized_q[0], "Question key missing"
            print("[OK] Personalized Resume-Based Interview Question Generator verified.")

        # 4. Test Web Routes Login & Navigation
        client.post('/login', data={'email': test_email, 'password': test_pass}, follow_redirects=True)
        print("[OK] User logged in.")

        # Resume Analyzer GET
        res = client.get('/resume-analyzer')
        assert res.status_code == 200, "Resume analyzer GET failed"
        assert b"ATS Compliance Audit" in res.data, "ATS audit content missing"
        print("[OK] Resume Analyzer Page GET (HTTP 200) verified.")

        # JD Analyzer GET
        res = client.get('/jd-analyzer')
        assert res.status_code == 200, "JD analyzer GET failed"
        assert b"Match & Skill Gap Analysis" in res.data, "JD match content missing"
        print("[OK] Job Description Matcher Page GET (HTTP 200) verified.")

        # Resume Report Page GET
        res = client.get(f'/resume/report/{analysis_id}')
        assert res.status_code == 200, "Resume report GET failed"
        assert b"Resume ATS Audit & Skill Report" in res.data, "Resume report content missing"
        print("[OK] Printable Resume ATS & Match Report Page (HTTP 200) verified.")

        # Dashboard GET with Phase 4 Widgets
        res = client.get('/dashboard')
        assert res.status_code == 200, "Dashboard GET failed"
        assert b"Latest ATS Resume Score" in res.data, "ATS Score dashboard widget missing"
        assert b"Target Job Match %" in res.data, "Job Match dashboard widget missing"
        print("[OK] Dashboard Phase 4 Resume Widgets verified.")

    print("\nALL PHASE 4 VERIFICATION TESTS PASSED SUCCESSFULLY!\n")

if __name__ == '__main__':
    test_interviewai_phase4()
