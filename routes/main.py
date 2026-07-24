from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'InterviewAI AI Career Platform',
        'version': '5.0.0'
    }), 200

def page_not_found(e):
    return render_template('404.html'), 404

def internal_server_error(e):
    return render_template('500.html'), 500
