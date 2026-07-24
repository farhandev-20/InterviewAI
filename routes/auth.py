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
    return UserService.get_by_id(user_id)

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

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))
