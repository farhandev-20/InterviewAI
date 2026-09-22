import os
import tempfile
# pyrefly: ignore [missing-import]
from werkzeug.utils import secure_filename
from database.db import db
from models.resume import Resume, ResumeAnalysis, JobDescription, ResumeJobMatch, SkillGap
from utils.file_parser import extract_text_from_file
from services.gemini_service import GeminiService

def _get_resumes_upload_folder():
    """Helper to safely get writable resumes upload folder."""
    try:
        # pyrefly: ignore [missing-import]
        from flask import current_app
        folder = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'static/uploads'), 'resumes')
    except Exception:
        folder = os.path.join(tempfile.gettempdir(), 'uploads', 'resumes') if os.getenv('VERCEL') else 'static/uploads/resumes'
    try:
        os.makedirs(folder, exist_ok=True)
    except Exception:
        pass
    return folder

class ResumeService:
    @staticmethod
    def save_and_analyze_resume(user_id, file_obj=None, raw_text_input="", target_role="Software Engineer", upload_folder=None):
        """
        Saves uploaded PDF/DOCX file or text input, parses extracted info,
        runs Gemini AI ATS audit, and persists into resumes & resume_analyses tables.
        """
        if upload_folder is None:
            upload_folder = _get_resumes_upload_folder()
        else:
            try:
                os.makedirs(upload_folder, exist_ok=True)
            except Exception:
                pass
        filename = "resume_text_input.txt"
        file_path = None
        extracted_text = ""

        # Handle file upload if present
        if file_obj and file_obj.filename:
            orig_filename = secure_filename(file_obj.filename)
            ext = orig_filename.rsplit('.', 1)[-1].lower() if '.' in orig_filename else ''
            
            if ext not in ['pdf', 'docx', 'doc', 'txt']:
                return None, None, "Invalid file format. Please upload PDF or DOCX documents."

            new_filename = f"resume_{user_id}_{orig_filename}"
            save_path = os.path.join(upload_folder, new_filename)
            file_obj.save(save_path)
            
            filename = orig_filename
            file_path = save_path
            extracted_text = extract_text_from_file(save_path)

        if not extracted_text and raw_text_input:
            extracted_text = raw_text_input.strip()

        if not extracted_text or len(extracted_text) < 10:
            return None, None, "Could not extract readable text from file. Please ensure the document is not encrypted or paste plain text."

        # Parse Contact & Skill Info
        parsed_info = GeminiService.parse_resume_info(extracted_text)

        # Create Resume DB Record
        resume = Resume(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            raw_text=extracted_text,
            parsed_name=parsed_info.get("name"),
            parsed_email=parsed_info.get("email"),
            parsed_phone=parsed_info.get("phone"),
            skills=parsed_info.get("skills"),
            education=parsed_info.get("education"),
            experience=parsed_info.get("experience"),
            projects=parsed_info.get("projects"),
            certifications=parsed_info.get("certifications"),
            tools=parsed_info.get("tools")
        )
        db.session.add(resume)
        db.session.flush()

        # Run Comprehensive ATS AI Evaluation
        ats_eval = GeminiService.evaluate_ats_score_comprehensive(extracted_text, target_role)

        analysis = ResumeAnalysis(
            resume_id=resume.id,
            ats_score=float(ats_eval.get("ats_score", 75)),
            skills_score=float(ats_eval.get("skills_score", 75)),
            keywords_score=float(ats_eval.get("keywords_score", 70)),
            experience_score=float(ats_eval.get("experience_score", 80)),
            projects_score=float(ats_eval.get("projects_score", 75)),
            education_score=float(ats_eval.get("education_score", 85)),
            readability_score=float(ats_eval.get("readability_score", 90)),
            formatting_score=float(ats_eval.get("formatting_score", 85)),
            summary=str(ats_eval.get("summary", "")),
            strengths=str(ats_eval.get("strengths", "")),
            weaknesses=str(ats_eval.get("weaknesses", "")),
            missing_skills=str(ats_eval.get("missing_skills", "")),
            grammar_suggestions=str(ats_eval.get("grammar_suggestions", "")),
            formatting_suggestions=str(ats_eval.get("formatting_suggestions", "")),
            project_suggestions=str(ats_eval.get("project_suggestions", "")),
            career_recommendations=str(ats_eval.get("career_recommendations", "")),
            actionable_improvements=str(ats_eval.get("actionable_improvements", ""))
        )
        db.session.add(analysis)
        db.session.commit()

        return resume, analysis, None

    @staticmethod
    def match_resume_with_jd(user_id, resume_id, jd_file_obj=None, jd_raw_text=""):
        """
        Saves JobDescription, calculates Resume vs JD match, skill gaps, and stores records in DB.
        """
        resume = Resume.query.get(int(resume_id))
        if not resume or resume.user_id != user_id:
            return None, None, "Resume not found or unauthorized."

        extracted_jd = ""
        if jd_file_obj and jd_file_obj.filename:
            save_path = os.path.join(_get_resumes_upload_folder(), f"jd_{user_id}_{secure_filename(jd_file_obj.filename)}")
            jd_file_obj.save(save_path)
            extracted_jd = extract_text_from_file(save_path)

        if not extracted_jd and jd_raw_text:
            extracted_jd = jd_raw_text.strip()

        if not extracted_jd or len(extracted_jd) < 10:
            return None, None, "Please provide valid Job Description text or document."

        # Parse JD Info
        jd_info = GeminiService.parse_job_description_advanced(extracted_jd)
        jd_record = JobDescription(
            user_id=user_id,
            title=jd_info.get("title", "Software Developer"),
            company=jd_info.get("company", "Target Company"),
            raw_text=extracted_jd,
            required_skills=jd_info.get("required_skills"),
            preferred_skills=jd_info.get("preferred_skills"),
            responsibilities=jd_info.get("responsibilities"),
            experience_level=jd_info.get("experience_level"),
            technologies=jd_info.get("technologies")
        )
        db.session.add(jd_record)
        db.session.flush()

        # Run AI Matcher
        match_res = GeminiService.match_resume_vs_jd_advanced(resume.raw_text, extracted_jd)
        match_record = ResumeJobMatch(
            resume_id=resume.id,
            job_description_id=jd_record.id,
            overall_match_pct=float(match_res.get("overall_match_pct", 80)),
            hiring_probability=str(match_res.get("hiring_probability", "Moderate")),
            matching_skills=str(match_res.get("matching_skills", "")),
            missing_skills=str(match_res.get("missing_skills", "")),
            missing_keywords=str(match_res.get("missing_keywords", "")),
            recommended_improvements=str(match_res.get("recommended_improvements", ""))
        )
        db.session.add(match_record)

        # Run Skill Gap Analysis
        gap_res = GeminiService.generate_skill_gap_analysis(resume.raw_text, extracted_jd)
        skill_gap = SkillGap(
            resume_id=resume.id,
            job_description_id=jd_record.id,
            present_skills=str(gap_res.get("present_skills", "")),
            missing_skills=str(gap_res.get("missing_skills", "")),
            priority_skills=str(gap_res.get("priority_skills", "")),
            learning_path=str(gap_res.get("learning_path", ""))
        )
        db.session.add(skill_gap)
        db.session.commit()

        return match_record, skill_gap, None

    @staticmethod
    def get_latest_user_resume(user_id):
        """Retrieve latest uploaded resume for user."""
        return Resume.query.filter_by(user_id=user_id).order_by(Resume.created_at.desc()).first()

    @staticmethod
    def get_latest_user_ats_score(user_id):
        """Retrieve latest ATS score for dashboard widget."""
        resume = ResumeService.get_latest_user_resume(user_id)
        if resume and resume.analyses:
            return resume.analyses[-1]
        return None

    @staticmethod
    def get_latest_user_job_match(user_id):
        """Retrieve latest job match for dashboard widget."""
        resume = ResumeService.get_latest_user_resume(user_id)
        if resume and resume.matches:
            return resume.matches[-1]
        return None
