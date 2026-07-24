import re

def validate_email(email):
    """Validate email format."""
    if not email:
        return False, "Email address is required."
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Please enter a valid email address."
    return True, None

def validate_password_strength(password):
    """
    Validate password strength:
    - Minimum 8 characters
    - At least one uppercase or lowercase letter
    - At least one numeric digit or special symbol
    """
    if not password:
        return False, "Password is required."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter."
    if not re.search(r'[0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>?/|\\]', password):
        return False, "Password must contain at least one number or special character."
    return True, None

def validate_registration(full_name, email, password, confirm_password):
    """Comprehensive registration validation."""
    if not full_name or len(full_name.strip()) < 2:
        return False, "Full Name must be at least 2 characters long."
    
    is_email_valid, email_err = validate_email(email)
    if not is_email_valid:
        return False, email_err

    is_pwd_valid, pwd_err = validate_password_strength(password)
    if not is_pwd_valid:
        return False, pwd_err

    if password != confirm_password:
        return False, "Passwords do not match."

    return True, None
