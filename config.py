import os
import tempfile
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)

def get_database_url():
    """
    Retrieves database URL with normalization for PostgreSQL (e.g. Supabase, Neon, Render)
    and graceful fallback for serverless (Vercel / AWS Lambda) or local SQLite.
    """
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        # SQLAlchemy 1.4+ requires postgresql:// instead of deprecated postgres://
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        return db_url
    
    # In serverless environments like Vercel, root filesystem is read-only, so fallback SQLite to /tmp
    if os.getenv('VERCEL') or os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
        return f'sqlite:///{os.path.join(tempfile.gettempdir(), "interviewai.db")}'
        
    return f'sqlite:///{os.path.join(BASE_DIR, "interviewai.db")}'

def get_upload_folder():
    """
    Determines upload directory path based on environment.
    """
    if os.getenv('VERCEL') or os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
        return os.path.join(tempfile.gettempdir(), 'uploads')
    return os.path.join(BASE_DIR, 'static', 'uploads')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_fallback_secret_key_8492749281739')
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    
    # Upload Settings
    UPLOAD_FOLDER = get_upload_folder()
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'svg', 'pdf', 'docx', 'doc', 'txt'}

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
