from db.database import execute_query, execute_update
from utils.helpers import sanitize_html

def get_messages(secure=False):
    """
    Retrieve all messages from the database.
    
    Args:
        secure (bool): Whether to use secure practices
        
    Returns:
        list: List of message dictionaries
    """
    query = "SELECT m.id, m.content, m.created_at, u.username FROM messages m JOIN users u ON m.user_id = u.id ORDER BY m.created_at DESC"
    messages = execute_query(query)
    
    # If secure mode is enabled, sanitize the content to prevent XSS
    if secure:
        for message in messages:
            message['content'] = sanitize_html(message['content'])
    
    return messages

def add_message(user_id, content, secure=False):
    """
    Add a new message to the database.
    
    Args:
        user_id (int): ID of the user posting the message
        content (str): Content of the message
        secure (bool): Whether to use secure practices
        
    Returns:
        bool: True if message was added successfully
    """
    # In secure mode, sanitize the content before storing
    if secure:
        content = sanitize_html(content)
    
    query = "INSERT INTO messages (user_id, content) VALUES (%s, %s)"
    execute_update(query, (user_id, content))
    return True

def get_vulnerable_code():
    """Return the vulnerable XSS code sample."""
    return """
# Vulnerable Code - XSS
@app.route('/messages', methods=['GET'])
def display_messages():
    # Directly insert user input into the page without sanitization
    messages = get_messages(secure=False)
    return render_template('messages.html', messages=messages)

@app.route('/post', methods=['POST'])
def post_message():
    # Accept raw user input and store it directly
    content = request.form['content']
    user_id = session.get('user_id', 1)  # Default to admin for demo
    add_message(user_id, content, secure=False)
    return redirect('/messages')
"""

def get_secure_code():
    """Return the secure XSS code sample."""
    return """
# Secure Code - XSS Prevention
@app.route('/messages', methods=['GET'])
def display_messages():
    # Retrieve messages with HTML sanitization enabled
    messages = get_messages(secure=True)
    return render_template('messages.html', messages=messages)

@app.route('/post', methods=['POST'])
def post_message():
    # Sanitize user input before storing
    content = request.form['content']
    content = sanitize_html(content)  # Escape HTML special characters
    user_id = session.get('user_id', 1)
    add_message(user_id, content, secure=True)
    return redirect('/messages')
"""