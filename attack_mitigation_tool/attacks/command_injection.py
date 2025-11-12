import subprocess
import shlex
from utils.helpers import execute_command

def ping_host(host, secure=False):
    """
    Ping a host and return the result.
    
    Args:
        host (str): The hostname or IP to ping
        secure (bool): Whether to use secure practices
        
    Returns:
        str: Command output
    """
    if secure:
        # Validate input and use a sanitized command execution
        if not is_valid_hostname(host):
            return "Invalid hostname or IP address."
        
        # Use list form to avoid shell=True
        command = ["ping", "-c", "4", host]
        try:
            output = subprocess.check_output(command, text=True, stderr=subprocess.STDOUT)
            return output
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output}"
    else:
        # Vulnerable to command injection
        command = f"ping -c 4 {host}"
        return execute_command(command, secure=False)

def is_valid_hostname(hostname):
    """
    Validate a hostname or IP address.
    
    Args:
        hostname (str): The hostname to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    import re
    # Basic validation for hostnames and IP addresses
    hostname_pattern = re.compile(r'^[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$')
    ip_pattern = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    
    if hostname_pattern.match(hostname):
        return True
    
    if ip_pattern.match(hostname):
        # Validate each octet
        octets = hostname.split('.')
        for octet in octets:
            if int(octet) > 255:
                return False
        return True
    
    return False

def get_vulnerable_code():
    """Return the vulnerable command injection code sample."""
    return """
# Vulnerable Code - Command Injection
@app.route('/tools/ping', methods=['POST'])
def ping_route():
    host = request.form['host']
    # Directly inserting user input into a command string
    command = f"ping -c 4 {host}"
    output = execute_command(command, secure=False)
    return render_template('tools.html', output=output)
"""

def get_secure_code():
    """Return the secure command injection code sample."""
    return """
# Secure Code - Command Injection Prevention
@app.route('/tools/ping', methods=['POST'])
def ping_route():
    host = request.form['host']
    
    # Validate the hostname
    if not is_valid_hostname(host):
        return render_template('tools.html', output="Invalid hostname or IP address.")
    
    # Use subprocess with arguments as a list (no shell=True)
    command = ["ping", "-c", "4", host]
    try:
        output = subprocess.check_output(command, text=True, stderr=subprocess.STDOUT)
        return render_template('tools.html', output=output)
    except subprocess.CalledProcessError as e:
        return render_template('tools.html', output=f"Error: {e.output}")
"""