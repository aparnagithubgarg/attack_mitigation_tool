from db.database import execute_query, execute_update
from utils.helpers import sanitize_sql_input

def search_users(username, secure=False):
    """
    Search for users by username.
    
    Args:
        username (str): The username to search for
        secure (bool): Whether to use secure practices
        
    Returns:
        list: List of user dictionaries
    """
    if secure:
        # Use parameterized query to prevent SQL injection
        query = "SELECT * FROM users WHERE username LIKE %s"
        users = execute_query(query, (f"%{username}%",))
    else:
        # Vulnerable to SQL injection
        query = f"SELECT * FROM users WHERE username LIKE '%{username}%'"
        users = execute_query(query)
    
    return users

def login_user(username, password, secure=False):
    """
    Authenticate a user.
    
    Args:
        username (str): The username
        password (str): The password
        secure (bool): Whether to use secure practices
        
    Returns:
        dict or None: User data if authenticated, None otherwise
    """
    if secure:
        # Use parameterized query to prevent SQL injection
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        users = execute_query(query, (username, password))
    else:
        # Vulnerable to SQL injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        users = execute_query(query)
    
    if users:
        return users[0]
    return None

def get_vulnerable_code():
    """Return the vulnerable SQL injection code sample."""
    return """
# Vulnerable Code - SQL Injection
@app.route('/users/search', methods=['GET'])
def search_users_route():
    username = request.args.get('username', '')
    # Direct string concatenation in SQL query
    users = search_users(username, secure=False)
    return render_template('users.html', users=users)

@app.route('/login', methods=['POST'])
def login_route():
    username = request.form['username']
    password = request.form['password']
    # Direct string concatenation in SQL query
    user = login_user(username, password, secure=False)
    if user:
        session['user_id'] = user['id']
        return redirect('/dashboard')
    return render_template('login.html', error='Invalid credentials')
"""

def get_secure_code():
    """Return the secure SQL injection code sample."""
    return """
# Secure Code - SQL Injection Prevention
@app.route('/users/search', methods=['GET'])
def search_users_route():
    username = request.args.get('username', '')
    # Using parameterized queries
    users = search_users(username, secure=True)
    return render_template('users.html', users=users)

@app.route('/login', methods=['POST'])
def login_route():
    username = request.form['username']
    password = request.form['password']
    # Using parameterized queries
    user = login_user(username, password, secure=True)
    if user:
        session['user_id'] = user['id']
        return redirect('/dashboard')
    return render_template('login.html', error='Invalid credentials')
"""