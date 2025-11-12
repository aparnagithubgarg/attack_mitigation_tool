import re
import html
import subprocess
import os
from flask import session

def is_secure_mode():
    """Check if secure mode is enabled."""
    return session.get('secure_mode', False)

def sanitize_html(content):
    """
    Sanitize HTML content to prevent XSS.
    
    Args:
        content (str): The HTML content to sanitize
        
    Returns:
        str: Sanitized HTML content
    """
    return html.escape(content)

def sanitize_sql_input(input_str):
    """
    Sanitize SQL input to prevent SQL injection.
    
    Args:
        input_str (str): The input string to sanitize
        
    Returns:
        str: Sanitized input string
    """
    # Remove SQL injection patterns
    sanitized = re.sub(r"['\"\\;--]", "", input_str)
    return sanitized

def validate_file_path(path):
    """
    Validate file path to prevent directory traversal.
    
    Args:
        path (str): The file path to validate
        
    Returns:
        bool: True if path is valid, False otherwise
    """
    # Check for directory traversal attempts
    if '..' in path or path.startswith('/') or '~' in path:
        return False
    return True

def execute_command(command, secure=False):
    """
    Execute a system command.
    
    Args:
        command (str): The command to execute
        secure (bool): Whether to use secure command execution
        
    Returns:
        str: Command output
    """
    if secure:
        # Whitelist approach - only allow specific commands
        allowed_commands = ['ls', 'dir', 'date', 'time', 'echo']
        command_parts = command.split()
        if not command_parts or command_parts[0] not in allowed_commands:
            return "Command not allowed in secure mode."
    
    try:
        # WARNING: This is intentionally vulnerable for demonstration
        # shell=True is used to demonstrate command injection vulnerability
        output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.output}"