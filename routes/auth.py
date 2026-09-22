from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from services.user_service import UserService
from utils.validators import validate_registration, validate_email, validate_password_strength

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    try:
        return UserService.get_by_id(user_id)
    except Exception as e:
        print(f"[UserLoader Notice] {e}")
        return None

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Input Validation
        is_valid, err_msg = validate_registration(full_name, email, password, confirm_password)
        if not is_valid:
            flash(err_msg, 'danger')
            return render_template('auth/register.html', full_name=full_name, email=email)

        # Create User
        user, err = UserService.create_user(full_name, email, password)
        if err:
            flash(err, 'danger')
            return render_template('auth/register.html', full_name=full_name, email=email)

        flash('Registration successful! Please log in to your new account.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = True if request.form.get('remember') else False

        if not email or not password:
            flash('Please provide both email and password.', 'warning')
            return render_template('auth/login.html', email=email)

        user, err = UserService.authenticate_user(email, password)
        if err:
            flash(err, 'danger')
            return render_template('auth/login.html', email=email)

        # Log user in with Flask-Login
        login_user(user, remember=remember)
        flash(f'Welcome back, {user.full_name}!', 'success')
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard.index')

        return redirect(next_page)

    return render_template('auth/login.html')

def _get_google_redirect_uri():
    """Dynamically determine the exact Google redirect URI based on current request."""
    import os
    env_uri = (os.getenv('GOOGLE_REDIRECT_URI') or '').strip()
    current_host = request.host
    is_live = ('localhost' not in current_host and '127.0.0.1' not in current_host)
    
    if not is_live:
        return url_for('auth.google_callback', _external=True)
        
    if env_uri and 'localhost' not in env_uri and '127.0.0.1' not in env_uri:
        return env_uri
    return f"https://{current_host}/google/callback"

@auth_bp.route('/google_login')
@auth_bp.route('/google')
def google_login():
    """Redirect to Google OAuth or development simulation."""
    import os
    import urllib.parse
    
    try:
        # Check if user requested demo/local simulation mode
        if request.args.get('demo') == '1':
            user = UserService.create_or_get_google_user(
                email="alex.candidate@gmail.com",
                full_name="Alex Candidate",
                google_id="google_sim_1029384756"
            )
            if user:
                login_user(user, remember=True)
                flash(f'Signed in with Google (Demo Account)! Welcome, {user.full_name}.', 'success')
                return redirect(url_for('dashboard.index'))

        client_id = (os.getenv('GOOGLE_CLIENT_ID') or '').strip()
        
        if client_id and client_id != 'your_google_client_id_here' and not client_id.startswith('your_'):
            redirect_uri = _get_google_redirect_uri()
            params = {
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'response_type': 'code',
                'scope': 'openid email profile',
                'prompt': 'select_account'
            }
            google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
            return redirect(google_auth_url)

        # Local simulation fallback when real OAuth credentials are not provided
        user = UserService.create_or_get_google_user(
            email="alex.candidate@gmail.com",
            full_name="Alex Candidate",
            google_id="google_sim_1029384756"
        )
        if user:
            login_user(user, remember=True)
            flash(f'Signed in with Google! Welcome, {user.full_name}.', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Error logging in with Google. Please use email & password registration.', 'warning')
            return redirect(url_for('auth.login'))
    except Exception as e:
        print(f"[Google Auth Exception] {e}")
        flash(f'Authentication error: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/google/callback')
def google_callback():
    """Handle Google OAuth authorization callback."""
    import os
    import json
    import urllib.request
    import urllib.parse
    import urllib.error

    code = request.args.get('code')
    client_id = (os.getenv('GOOGLE_CLIENT_ID') or '').strip()
    client_secret = (os.getenv('GOOGLE_CLIENT_SECRET') or '').strip()
    redirect_uri = _get_google_redirect_uri()

    if code and client_id and client_secret:
        try:
            token_url = "https://oauth2.googleapis.com/token"
            payload = urllib.parse.urlencode({
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }).encode('utf-8')

            token_req = urllib.request.Request(
                token_url,
                data=payload,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'InterviewAI-OAuth-Client/1.0'
                },
                method='POST'
            )

            with urllib.request.urlopen(token_req, timeout=15) as resp:
                tokens = json.loads(resp.read().decode('utf-8'))
                access_token = tokens.get('access_token')

            if access_token:
                userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
                user_req = urllib.request.Request(
                    userinfo_url,
                    headers={
                        'Authorization': f'Bearer {access_token}',
                        'User-Agent': 'InterviewAI-OAuth-Client/1.0'
                    }
                )
                with urllib.request.urlopen(user_req, timeout=15) as user_resp:
                    info = json.loads(user_resp.read().decode('utf-8'))
                    email = info.get('email')
                    name = info.get('name') or info.get('given_name') or 'Google User'
                    g_id = info.get('sub') or info.get('id')

                    if email:
                        user = UserService.create_or_get_google_user(email=email, full_name=name, google_id=g_id)
                        login_user(user, remember=True)
                        flash(f'Signed in as {user.full_name} ({user.email})!', 'success')
                        return redirect(url_for('dashboard.index'))
        except urllib.error.HTTPError as he:
            err_body = he.read().decode('utf-8', errors='ignore') if hasattr(he, 'read') else ''
            print(f"[Google OAuth HTTPError {he.code}] {he.reason}: {err_body}")
            flash(f'Google authentication error: {he.reason}. Please try again.', 'danger')
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(f"[Google OAuth Error] {e}")
            flash(f'Google login error: {str(e)}', 'danger')
            return redirect(url_for('auth.login'))

    flash('Google authentication was cancelled or credentials missing.', 'warning')
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))
