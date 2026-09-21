import os
from flask import Flask
from config import config_by_name as config
from database.db import db
import models
import routes

# Base directory for absolute paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, 'templates'),
        static_folder=os.path.join(BASE_DIR, 'static')
    )
    app.config.from_object(config.get(config_name, config['default']))

    # Enable Werkzeug ProxyFix for Cloudflare / Render / Vercel reverse proxy HTTPS support
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Ensure upload directories exist safely
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'resumes'), exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'avatars'), exist_ok=True)
    except Exception as e:
        print(f"[Upload Directory Notice] {e}")

    # Initialize extensions
    db.init_app(app)

    from routes.auth import login_manager
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(routes.main_bp)
    app.register_blueprint(routes.auth_bp)
    app.register_blueprint(routes.dashboard_bp)
    app.register_blueprint(routes.interview_bp)
    app.register_blueprint(routes.analyzers_bp)
    app.register_blueprint(routes.reports_bp)
    app.register_blueprint(routes.system_bp)

    # Register error handlers
    app.register_error_handler(404, routes.page_not_found)
    app.register_error_handler(500, routes.internal_server_error)

    # Create tables and run lightweight migrations safely without blocking app start
    with app.app_context():
        try:
            db.create_all()
            from sqlalchemy import text, inspect
            inspector = inspect(db.engine)
            if 'users' in inspector.get_table_names():
                user_cols = [c['name'] for c in inspector.get_columns('users')]
                if 'google_id' not in user_cols:
                    db.session.execute(text("ALTER TABLE users ADD COLUMN google_id VARCHAR(255)"))
                    db.session.commit()
            if 'interviews' in inspector.get_table_names():
                inv_cols = [c['name'] for c in inspector.get_columns('interviews')]
                if 'mode' not in inv_cols:
                    db.session.execute(text("ALTER TABLE interviews ADD COLUMN mode VARCHAR(50) DEFAULT 'text'"))
                    db.session.commit()
        except Exception as e:
            print(f"[Database Init/Migration Notice] {e}")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
