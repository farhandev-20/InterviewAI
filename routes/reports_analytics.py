from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.interview import Interview
from services.interview_service import InterviewService

reports_bp = Blueprint('reports_bp', __name__)

@reports_bp.route('/reports')
@login_required
def list_reports():
    # Fetch user's completed interviews
    interviews = Interview.query.filter_by(user_id=current_user.id).order_by(Interview.start_time.desc()).all()
    return render_template('reports/list.html', interviews=interviews)

@reports_bp.route('/analytics')
@login_required
def analytics():
    db_stats = InterviewService.get_user_dashboard_stats(current_user.id)
    return render_template('reports/analytics.html', stats=db_stats, user_stats=db_stats)
