from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from services.resume_service import ResumeService
from models.resume import Resume, ResumeAnalysis, ResumeJobMatch, SkillGap

analyzers_bp = Blueprint('analyzers', __name__)

@analyzers_bp.route('/resume-analyzer', methods=['GET', 'POST'])
@login_required
def resume_analyzer():
    resume = None
    analysis = None
    target_role = current_user.target_role or "Full Stack Developer"
    raw_text_input = ""

    # Fetch user's latest resume if exists
    resume = ResumeService.get_latest_user_resume(current_user.id)
    if resume and resume.analyses:
        analysis = resume.analyses[-1]

    if request.method == 'POST':
        target_role = request.form.get('target_role', target_role).strip()
        raw_text_input = request.form.get('resume_text', '').strip()
        file_obj = request.files.get('resume_file')

        res_obj, analysis_obj, err_msg = ResumeService.save_and_analyze_resume(
            user_id=current_user.id,
            file_obj=file_obj,
            raw_text_input=raw_text_input,
            target_role=target_role
        )

        if err_msg:
            flash(err_msg, 'danger')
        else:
            resume = res_obj
            analysis = analysis_obj
            flash('AI Resume Analysis complete! Check your ATS Score breakdown.', 'success')

    return render_template(
        'analyzers/resume.html',
        resume=resume,
        analysis=analysis,
        target_role=target_role,
        resume_text=raw_text_input
    )

@analyzers_bp.route('/jd-analyzer', methods=['GET', 'POST'])
@login_required
def jd_analyzer():
    latest_resume = ResumeService.get_latest_user_resume(current_user.id)
    match_record = None
    skill_gap = None
    jd_raw_text = ""

    if latest_resume and latest_resume.matches:
        match_record = latest_resume.matches[-1]
    if latest_resume and latest_resume.skill_gaps:
        skill_gap = latest_resume.skill_gaps[-1]

    if request.method == 'POST':
        jd_raw_text = request.form.get('jd_text', '').strip()
        jd_file = request.files.get('jd_file')

        if not latest_resume:
            flash('Please upload or analyze your resume first before running JD Matcher.', 'warning')
            return redirect(url_for('analyzers.resume_analyzer'))

        match_obj, gap_obj, err_msg = ResumeService.match_resume_with_jd(
            user_id=current_user.id,
            resume_id=latest_resume.id,
            jd_file_obj=jd_file,
            jd_raw_text=jd_raw_text
        )

        if err_msg:
            flash(err_msg, 'danger')
        else:
            match_record = match_obj
            skill_gap = gap_obj
            flash('Job Description Matcher & Skill Gap Analysis complete!', 'success')

    return render_template(
        'analyzers/jd_analyzer.html',
        resume=latest_resume,
        match=match_record,
        skill_gap=skill_gap,
        jd_text=jd_raw_text
    )

@analyzers_bp.route('/resume/report/<int:analysis_id>')
@login_required
def resume_report(analysis_id):
    analysis = ResumeAnalysis.query.get(int(analysis_id))
    if not analysis or analysis.resume.user_id != current_user.id:
        flash('Unauthorized access or report not found.', 'danger')
        return redirect(url_for('analyzers.resume_analyzer'))

    resume = analysis.resume
    latest_match = resume.matches[-1] if resume.matches else None
    latest_gap = resume.skill_gaps[-1] if resume.skill_gaps else None

    return render_template(
        'analyzers/resume_report.html',
        resume=resume,
        analysis=analysis,
        match=latest_match,
        skill_gap=latest_gap
    )
