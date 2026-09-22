from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from services.user_service import UserService
from services.interview_service import InterviewService
from services.resume_service import ResumeService
from services.system_service import SystemService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    try:
        db_stats = InterviewService.get_user_dashboard_stats(current_user.id)
    except Exception as e:
        print(f"[Dashboard Stats Notice] {e}")
        db_stats = {
            'total_interviews': 0,
            'average_score': 0,
            'best_score': 0,
            'weekly_hours': '0.0 hrs',
            'recent_activities': []
        }
    
    try:
        latest_ats = ResumeService.get_latest_user_ats_score(current_user.id)
    except Exception:
        latest_ats = None
        
    try:
        latest_match = ResumeService.get_latest_user_job_match(current_user.id)
    except Exception:
        latest_match = None
        
    try:
        latest_resume = ResumeService.get_latest_user_resume(current_user.id)
    except Exception:
        latest_resume = None
    
    try:
        streak = SystemService.calculate_practice_streak(current_user.id)
    except Exception:
        streak = 0
        
    try:
        unlocked = SystemService.check_and_unlock_achievements(current_user.id)
    except Exception:
        unlocked = []

    stats = {
        'total_interviews': db_stats.get('total_interviews', 0),
        'average_score': db_stats.get('average_score', 0),
        'best_score': db_stats.get('best_score', 0),
        'weekly_hours': db_stats.get('weekly_hours', '0.0 hrs'),
        'streak': streak
    }
    recent_activities = db_stats.get('recent_activities', [])

    return render_template(
        'dashboard/index.html',
        stats=stats,
        activities=recent_activities,
        ats=latest_ats,
        match=latest_match,
        resume=latest_resume,
        achievements=unlocked
    )

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '')
        email = request.form.get('email', '')
        target_role = request.form.get('target_role', '')
        skills = request.form.get('skills', '')
        file_obj = request.files.get('profile_photo')

        success, msg = UserService.update_profile(
            user_id=current_user.id,
            full_name=full_name,
            email=email,
            target_role=target_role,
            skills=skills,
            file_obj=file_obj,
            upload_folder=current_app.config['UPLOAD_FOLDER'],
            allowed_extensions=current_app.config['ALLOWED_EXTENSIONS']
        )

        if success:
            session['user_name'] = full_name
            session['user_role'] = target_role
            flash(msg, 'success')
            return redirect(url_for('dashboard.profile'))
        else:
            flash(msg, 'danger')

    db_stats = InterviewService.get_user_dashboard_stats(current_user.id)
    return render_template('dashboard/profile.html', user_stats=db_stats)

@dashboard_bp.route('/settings')
@login_required
def settings():
    return render_template('dashboard/settings.html')
