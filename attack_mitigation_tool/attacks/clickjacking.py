from flask import request, session, render_template, redirect, url_for

def delete_account(user_id, confirm=False):
    """
    Delete a user account.
    
    Args:
        user_id (int): The ID of the user account to delete
        confirm (bool): Whether the action is confirmed
        
    Returns:
        str: Success or error message
    """
    if not confirm:
        return "Confirmation required to delete account."
    
    # In a real application, this would delete the account
    # For demo purposes, we'll just return a success message
    return f"Account {user_id} has been deleted."

def apply_clickjacking_protection(response, secure=False):
    """
    Apply clickjacking protection headers to a response.
    
    Args:
        response: The Flask response object
        secure (bool): Whether to use secure practices
        
    Returns:
        response: The modified response object
    """
    if secure:
        # Add X-Frame-Options header to prevent clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        # Add Content-Security-Policy header for additional protection
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
    
    return response

def get_vulnerable_code():
    """Return the vulnerable clickjacking code sample."""
    return """
# Vulnerable Code - Clickjacking
@app.route('/profile/delete', methods=['POST'])
def delete_profile():
    user_id = session.get('user_id', 1)  # Default to admin for demo
    confirm = request.form.get('confirm', False)
    
    result = delete_account(user_id, confirm=confirm)
    return render_template('profile.html', message=result)

# No headers set to prevent framing
"""

def get_secure_code():
    """Return the secure clickjacking code sample."""
    return """
# Secure Code - Clickjacking Prevention
@app.route('/profile/delete', methods=['POST'])
def delete_profile():
    user_id = session.get('user_id', 1)  # Default to admin for demo
    confirm = request.form.get('confirm', False)
    
    # CSRF token validation would be here in a real application
    
    result = delete_account(user_id, confirm=confirm)
    return render_template('profile.html', message=result)

# Add clickjacking protection headers
@app.after_request
def add_security_headers(response):
    # Add X-Frame-Options header to prevent clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # Add Content-Security-Policy header for additional protection
    response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
    return response
"""