from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.user import User
from services.user_service import UserService
from utils.validators import validate_registration, validate_email, validate_password_strength

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    try:
        user = UserService.get_by_id(user_id)
        if not user and session.get('user_google_id'):
            user = UserService.get_by_google_id(session.get('user_google_id'))
        if not user and session.get('user_email'):
            user = UserService.create_or_get_google_user(
                email=session.get('user_email'),
                full_name=session.get('user_name'),
                google_id=session.get('user_google_id'),
                picture_url=session.get('user_picture')
            )
        return user
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

        # Log user in with Flask-Login & synchronize session
        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.full_name
        session['user_role'] = user.target_role
        session['user_google_id'] = user.google_id
        session['user_picture'] = user.profile_image
        login_user(user, remember=remember)
        flash(f'Welcome back, {user.full_name}!', 'success')
        
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('dashboard.index')

        return redirect(next_page)

    return render_template('auth/login.html')

def _decode_id_token_payload(id_token_str):
    """Safely decode Google ID Token JSON payload (claims) without external JWT dependencies."""
    import base64
    import json
    if not id_token_str or not isinstance(id_token_str, str):
        return {}
    try:
        parts = id_token_str.split('.')
        if len(parts) >= 2:
            payload_b64 = parts[1]
            rem = len(payload_b64) % 4
            if rem > 0:
                payload_b64 += '=' * (4 - rem)
            decoded = base64.urlsafe_b64decode(payload_b64.encode('utf-8')).decode('utf-8', errors='ignore')
            return json.loads(decoded)
    except Exception as e:
        print(f"[ID Token Decode Notice] {e}")
    return {}

def _get_google_credentials():
    """Retrieve configured Google credentials and dynamically determine redirect URI."""
    import os
    from flask import current_app
    
    client_id = (os.getenv('GOOGLE_CLIENT_ID') or current_app.config.get('GOOGLE_CLIENT_ID') or '').strip().strip('"').strip("'")
    client_secret = (os.getenv('GOOGLE_CLIENT_SECRET') or current_app.config.get('GOOGLE_CLIENT_SECRET') or '').strip().strip('"').strip("'")
    env_uri = (os.getenv('GOOGLE_REDIRECT_URI') or current_app.config.get('GOOGLE_REDIRECT_URI') or '').strip().strip('"').strip("'")
    
    current_host = request.host
    is_live = ('localhost' not in current_host and '127.0.0.1' not in current_host)
    
    if not is_live:
        redirect_uri = url_for('auth.google_callback', _external=True)
    elif env_uri and 'localhost' not in env_uri and '127.0.0.1' not in env_uri:
        redirect_uri = env_uri.rstrip('/')
    else:
        proto = request.headers.get('X-Forwarded-Proto', 'https' if is_live else 'http')
        redirect_uri = f"{proto}://{current_host}/google/callback"

    return client_id, client_secret, redirect_uri

@auth_bp.route('/google_login')
@auth_bp.route('/google')
def google_login():
    """Redirect to Google OAuth."""
    import urllib.parse
    
    try:
        client_id, client_secret, redirect_uri = _get_google_credentials()
        
        if not client_id or client_id.startswith('your_'):
            flash('Google Client ID (GOOGLE_CLIENT_ID) is missing. Please add it to your Vercel Environment Variables.', 'danger')
            return redirect(url_for('auth.login'))

        if not client_secret or client_secret.startswith('your_'):
            flash('Google Client Secret (GOOGLE_CLIENT_SECRET) is missing. Please add it to your Vercel Environment Variables.', 'danger')
            return redirect(url_for('auth.login'))

        # Store the exact redirect_uri in session for guaranteed parity during token exchange
        session['oauth_redirect_uri'] = redirect_uri

        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'prompt': 'select_account'
        }
        google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
        return redirect(google_auth_url)
    except Exception as e:
        print(f"[Google Auth Exception] {e}")
        flash(f'Authentication error: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/google/callback')
def google_callback():
    """Handle Google OAuth authorization callback."""
    import json
    import urllib.request
    import urllib.parse
    import urllib.error

    code = request.args.get('code')
    error = request.args.get('error')
    if error:
        flash(f'Google sign in was cancelled or denied: {error}', 'warning')
        return redirect(url_for('auth.login'))

    client_id, client_secret, redirect_uri = _get_google_credentials()
    login_redirect_uri = session.pop('oauth_redirect_uri', None)
    if login_redirect_uri:
        redirect_uri = login_redirect_uri

    if not code:
        flash('No authorization code was received from Google.', 'warning')
        return redirect(url_for('auth.login'))

    if not client_id or client_id.startswith('your_'):
        flash('Google Client ID (GOOGLE_CLIENT_ID) is missing in environment variables. Please check Vercel settings.', 'danger')
        return redirect(url_for('auth.login'))

    if not client_secret or client_secret.startswith('your_'):
        flash('Google Client Secret (GOOGLE_CLIENT_SECRET) is missing in environment variables. Please check Vercel settings.', 'danger')
        return redirect(url_for('auth.login'))

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
            id_token_str = tokens.get('id_token')

        info = {}
        # 1. Parse id_token claims if available
        if id_token_str:
            info = _decode_id_token_payload(id_token_str)

        # 2. Query userinfo endpoint with access_token if present
        if access_token:
            try:
                userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
                user_req = urllib.request.Request(
                    userinfo_url,
                    headers={
                        'Authorization': f'Bearer {access_token}',
                        'User-Agent': 'InterviewAI-OAuth-Client/1.0'
                    }
                )
                with urllib.request.urlopen(user_req, timeout=15) as user_resp:
                    userinfo_data = json.loads(user_resp.read().decode('utf-8'))
                    info.update(userinfo_data)
            except Exception as uerr:
                print(f"[UserInfo Fetch Notice] {uerr}")

        email = info.get('email')
        
        # Extract full name, given_name, family_name
        name = info.get('name')
        if not name:
            given = (info.get('given_name') or '').strip()
            family = (info.get('family_name') or '').strip()
            if given or family:
                name = f"{given} {family}".strip()
        
        picture = info.get('picture') or info.get('avatar_url')
        g_id = info.get('sub') or info.get('id')

        if not email and not g_id:
            flash('Failed to retrieve user profile from Google. Please try again.', 'danger')
            return redirect(url_for('auth.login'))

        user = UserService.create_or_get_google_user(
            email=email,
            full_name=name,
            google_id=g_id,
            picture_url=picture
        )

        if not user:
            flash('Error creating or retrieving user account in database.', 'danger')
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id
        session['user_email'] = user.email
        session['user_name'] = user.full_name
        session['user_role'] = user.target_role
        session['user_google_id'] = user.google_id
        session['user_picture'] = user.profile_image
        login_user(user, remember=True)
        flash(f'Signed in as {user.full_name} ({user.email})!', 'success')
        return redirect(url_for('dashboard.index'))

    except urllib.error.HTTPError as he:
        err_body = he.read().decode('utf-8', errors='ignore') if hasattr(he, 'read') else ''
        print(f"[Google OAuth HTTPError {he.code}] {he.reason}: {err_body}")
        try:
            err_json = json.loads(err_body)
            error_desc = err_json.get('error_description') or err_json.get('error') or he.reason
        except Exception:
            error_desc = err_body or he.reason
        flash(f'Google authentication error: {error_desc}', 'danger')
        return redirect(url_for('auth.login'))
    except Exception as e:
        print(f"[Google OAuth Error] {e}")
        flash(f'Google login error: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))
