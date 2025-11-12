import json
from flask import session, request

def process_payment(credit_card, amount, secure=False):
    """
    Process a payment.
    
    Args:
        credit_card (str): Credit card number
        amount (float): Payment amount
        secure (bool): Whether to use secure practices
        
    Returns:
        dict: Payment result
    """
    # Simulate payment processing
    if secure:
        # In a secure implementation, data would be encrypted
        # and processed over HTTPS
        result = {
            "success": True,
            "amount": amount,
            "transaction_id": "sec_12345",
            "message": "Payment processed securely."
        }
    else:
        # In an insecure implementation, sensitive data is exposed
        result = {
            "success": True,
            "credit_card": credit_card,  # Sensitive data exposed
            "amount": amount,
            "transaction_id": "12345",
            "message": "Payment processed."
        }
    
    return result

def get_vulnerable_code():
    """Return the vulnerable MITM code sample."""
    return """
# Vulnerable Code - Man in the Middle (MITM)
@app.route('/checkout', methods=['POST'])
def checkout():
    # No TLS/SSL requirement
    credit_card = request.form['credit_card']
    amount = float(request.form['amount'])
    
    # Process payment without encryption
    result = process_payment(credit_card, amount, secure=False)
    
    # Return sensitive data in the response
    return json.dumps(result)

# No HSTS headers set
"""

def get_secure_code():
    """Return the secure MITM code sample."""
    return """
# Secure Code - MITM Prevention
@app.route('/checkout', methods=['POST'])
def checkout():
    # Force HTTPS in a production application
    if not request.is_secure and not app.debug:
        return redirect(url_for('checkout', _scheme='https', _external=True))
    
    credit_card = request.form['credit_card']
    amount = float(request.form['amount'])
    
    # Process payment with proper security
    result = process_payment(credit_card, amount, secure=True)
    
    # Only return necessary info, no sensitive data
    secure_result = {
        "success": result["success"],
        "transaction_id": result["transaction_id"],
        "message": result["message"]
    }
    
    return json.dumps(secure_result)

# Set security headers
@app.after_request
def add_security_headers(response):
    # HTTP Strict Transport Security
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
"""