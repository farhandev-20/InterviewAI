from .auth import auth_bp
from .dashboard import dashboard_bp
from .interview import interview_bp
from .analyzers import analyzers_bp
from .reports_analytics import reports_bp
from .system import system_bp
from .main import main_bp, page_not_found, internal_server_error

__all__ = [
    'auth_bp', 'dashboard_bp', 'interview_bp', 'analyzers_bp',
    'reports_bp', 'system_bp', 'main_bp', 'page_not_found', 'internal_server_error'
]
