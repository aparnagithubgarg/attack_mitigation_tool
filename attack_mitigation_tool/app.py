from flask import Flask, render_template, request, redirect, url_for, session, Response, jsonify
import os
import re
import subprocess
import json
from functools import wraps

# Import attack modules
from attacks import xss, sql_injection, command_injection, directory_traversal, clickjacking, mitm, dos
from utils.helpers import is_secure_mode
from db.database import init_db, execute_query, execute_update
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
@app.before_request
def initialize():
    # Create necessary directories
    os.makedirs('static/files/public', exist_ok=True)
    os.makedirs('static/files/private', exist_ok=True)
    
    # Create sample files
    with open('static/files/public/welcome.txt', 'w') as f:
        f.write('Welcome to the Attack Mitigation Tool!')
    
    with open('static/files/public/notes.txt', 'w') as f:
        f.write('These are some public notes.')
    
    with open('static/files/private/secret.txt', 'w') as f:
        f.write('This is a secret file that should not be accessible.')
    
    # Initialize the database
    init_db()

# Routes
@app.route('/')
def index():
    secure_mode = session.get('secure_mode', False)
    return render_template('index.html', secure_mode=secure_mode)

@app.route('/toggle-security', methods=['POST'])
def toggle_security():
    current_mode = session.get('secure_mode', False)
    session['secure_mode'] = not current_mode
    return redirect(request.referrer or url_for('index'))

# XSS Attack Demo
@app.route('/xss')
def xss_demo():
    secure_mode = session.get('secure_mode', False)
    messages = xss.get_messages(secure=secure_mode)
    vulnerable_code = xss.get_vulnerable_code()
    secure_code = xss.get_secure_code()
    return render_template('attacks/xss.html', 
                          secure_mode=secure_mode,
                          messages=messages,
                          vulnerable_code=vulnerable_code,
                          secure_code=secure_code)

@app.route('/xss/post', methods=['POST'])
def xss_post():
    secure_mode = session.get('secure_mode', False)
    content = request.form.get('content', '')
    user_id = 2  # Default to user1 for demo
    
    xss.add_message(user_id, content, secure=secure_mode)
    return redirect(url_for('xss_demo'))

# SQL Injection Demo
@app.route('/sql-injection')
def sql_injection_demo():
    secure_mode = session.get('secure_mode', False)
    username = request.args.get('username', '')
    users = []
    
    if username:
        users = sql_injection.search_users(username, secure=secure_mode)
    
    vulnerable_code = sql_injection.get_vulnerable_code()
    secure_code = sql_injection.get_secure_code()
    
    return render_template('attacks/sql_injection.html', 
                          secure_mode=secure_mode,
                          username=username,
                          users=users,
                          vulnerable_code=vulnerable_code,
                          secure_code=secure_code)

# Command Injection Demo
@app.route('/command-injection', methods=['GET', 'POST'])
def command_injection_demo():
    secure_mode = session.get('secure_mode', False)
    output = None
    host = None
    
    if request.method == 'POST':
        host = request.form.get('host', '')
        if host:
            output = command_injection.ping_host(host, secure=secure_mode)
    
    vulnerable_code = command_injection.get_vulnerable_code()
    secure_code = command_injection.get_secure_code()
    
    return render_template('attacks/command_injection.html',
                          secure_mode=secure_mode,
                          output=output,
                          host=host,
                          vulnerable_code=vulnerable_code,
                          secure_code=secure_code)

# Directory Traversal Demo
@app.route('/directory-traversal')
def directory_traversal_demo():
    secure_mode = session.get('secure_mode', False)
    filename = request.args.get('filename', '')
    content = None
    
    if filename:
        content = directory_traversal.get_file_content(filename, secure=secure_mode)
    
    vulnerable_code = directory_traversal.get_vulnerable_code()
    secure_code = directory_traversal.get_secure_code()
    
    return render_template('attacks/directory_traversal.html',
                          secure_mode=secure_mode,
                          filename=filename,
                          content=content,
                          vulnerable_code=vulnerable_code,
                          secure_code=secure_code)

# Clickjacking Demo
@app.route('/clickjacking')
def clickjacking_demo():
    secure_mode = session.get('secure_mode', False)
    vulnerable_code = clickjacking.get_vulnerable_code()
    secure_code = clickjacking.get_secure_code()
    
    response = render_template('attacks/clickjacking.html',
                              secure_mode=secure_mode,
                              vulnerable_code=vulnerable_code,
                              secure_code=secure_code)
    
    # Apply clickjacking protection if in secure mode
    if secure_mode:
        response = Response(response)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response
    
    return response

@app.route('/clickjacking/victim')
def clickjacking_victim():
    """A page that could be framed for clickjacking."""
    return render_template('attacks/clickjacking_victim.html')

@app.route('/clickjacking/delete', methods=['POST'])
def clickjacking_delete():
    user_id = 1  # Demo user ID
    result = clickjacking.delete_account(user_id, confirm=True)
    return jsonify({"message": result})

# MITM Demo
@app.route('/mitm')
def mitm_demo():
    secure_mode = session.get('secure_mode', False)
    vulnerable_code = mitm.get_vulnerable_code()
    secure_code = mitm.get_secure_code()
    
    return render_template('attacks/mitm.html',
                          secure_mode=secure_mode,
                          vulnerable_code=vulnerable_code,
                          secure_code=secure_code)

@app.route('/mitm/checkout', methods=['POST'])
def mitm_checkout():
    secure_mode = session.get('secure_mode', False)
    
    credit_card = request.form.get('credit_card', '')
    amount = float(request.form.get('amount', 0))
    
    result = mitm.process_payment(credit_card, amount, secure=secure_mode)
    return jsonify(result)

# DoS Demo
@app.route('/dos')
def dos_demo():
    secure_mode = session.get('secure_mode', False)
    vulnerable_code = dos.get_vulnerable_code()
    secure_code = dos.get_secure_code()
    
    return render_template('attacks/dos.html',
                          secure_mode=secure_mode,
                          vulnerable_code=vulnerable_code,
                          secure_code=secure_code)

@app.route('/dos/regex', methods=['POST'])
def dos_regex():
    secure_mode = session.get('secure_mode', False)
    
    # Rate limiting in secure mode
    if secure_mode:
        client_ip = request.remote_addr
        if not dos.rate_limiter.is_allowed(client_ip):
            return jsonify({"error": "Rate limit exceeded. Please try again later."})
    
    pattern = request.form.get('pattern', '')
    text = request.form.get('text', '')
    
    matches = dos.process_regex(pattern, text, secure=secure_mode)
    return jsonify({"matches": matches})

# Documentation
@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

if __name__ == '__main__':
    app.run(debug=True)