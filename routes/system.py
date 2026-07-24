from flask import Blueprint, jsonify, request, flash, redirect, url_for
from flask_login import login_required, logout_user, current_user
from services.system_service import SystemService
from database.db import db

system_bp = Blueprint('system', __name__)

@system_bp.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    notifications = SystemService.get_user_notifications(current_user.id, limit=10)
    unread_count = SystemService.get_unread_count(current_user.id)
    return jsonify({
        'status': 'success',
        'unread_count': unread_count,
        'notifications': [n.to_dict() for n in notifications]
    })

@system_bp.route('/api/notifications/read-all', methods=['POST'])
@login_required
def mark_read():
    SystemService.mark_all_notifications_read(current_user.id)
    return jsonify({'status': 'success'})

@system_bp.route('/settings/update-voice', methods=['POST'])
@login_required
def update_voice_settings():
    voice = request.form.get('voice_name', 'Default')
    speed = request.form.get('speech_rate', '1.0')
    flash(f'Voice preferences updated successfully (Voice: {voice}, Rate: {speed}x).', 'success')
    return redirect(url_for('dashboard.settings'))

@system_bp.route('/settings/delete-account', methods=['POST'])
@login_required
def delete_account():
    confirm_text = request.form.get('confirm_text', '')
    if confirm_text.strip().upper() != 'DELETE':
        flash('Account deletion cancelled. Confirmation text did not match.', 'warning')
        return redirect(url_for('dashboard.settings'))

    user = current_user
    logout_user()
    db.session.delete(user)
    db.session.commit()

    flash('Your account and associated interview data have been permanently deleted.', 'info')
    return redirect(url_for('main.index'))
