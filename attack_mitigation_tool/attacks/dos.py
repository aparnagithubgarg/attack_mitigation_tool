import time
import re
from flask import request, session

# Simple rate limiter implementation
class RateLimiter:
    def __init__(self, max_requests=10, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window  # in seconds
        self.request_log = {}  # IP -> [timestamp1, timestamp2, ...]
    
    def is_allowed(self, ip_address):
        """Check if a request from the IP is allowed."""
        current_time = time.time()
        
        # Initialize if IP not seen before
        if ip_address not in self.request_log:
            self.request_log[ip_address] = []
        
        # Remove old timestamps
        self.request_log[ip_address] = [
            timestamp for timestamp in self.request_log[ip_address]
            if current_time - timestamp < self.time_window
        ]
        
        # Check if under the limit
        if len(self.request_log[ip_address]) < self.max_requests:
            self.request_log[ip_address].append(current_time)
            return True
        
        return False

# Global rate limiter instance
rate_limiter = RateLimiter()

def process_regex(pattern, text, secure=False):
    """
    Process a regular expression pattern against text.
    
    Args:
        pattern (str): Regular expression pattern
        text (str): Text to match against
        secure (bool): Whether to use secure practices
        
    Returns:
        list: Matches found
    """
    if secure:
        # Limit regex processing time to prevent ReDoS
        # (In a real implementation, you would use a more robust approach)
        start_time = time.time()
        timeout = 0.5  # seconds
        
        # Validate regex pattern complexity
        if is_complex_regex(pattern):
            return ["Error: Complex regex pattern rejected for security reasons."]
        
        try:
            regex = re.compile(pattern)
            matches = []
            
            # Process with timeout
            for match in regex.finditer(text):
                if time.time() - start_time > timeout:
                    return ["Timeout: Regex processing took too long."]
                matches.append(match.group())
            
            return matches
        except re.error as e:
            return [f"Regex error: {str(e)}"]
    else:
        # Vulnerable to ReDoS
        try:
            regex = re.compile(pattern)
            return [match.group() for match in regex.finditer(text)]
        except re.error as e:
            return [f"Regex error: {str(e)}"]

def is_complex_regex(pattern):
    """
    Check if a regex pattern is potentially vulnerable to ReDoS.
    
    Args:
        pattern (str): The regex pattern to check
        
    Returns:
        bool: True if pattern is complex, False otherwise
    """
    # Check for nested repetition (a common ReDoS vulnerability)
    if re.search(r'\([^()]*[+*][^()]*\)[+*]', pattern):
        return True
    
    # Check for multiple nested groups with repetition
    if re.search(r'\([^()]*\([^()]*\)[^()]*\)[+*]', pattern):
        return True
    
    # Check for backreferences within repetition
    if re.search(r'\(.*\\[0-9].*\)[+*]', pattern):
        return True
    
    return False

def get_vulnerable_code():
    """Return the vulnerable DoS code sample."""
    return """
# Vulnerable Code - Denial of Service (DoS)
@app.route('/regex/test', methods=['POST'])
def regex_test():
    pattern = request.form['pattern']
    text = request.form['text']
    
    # No rate limiting
    # No input validation
    # Vulnerable to ReDoS (Regular Expression Denial of Service)
    matches = process_regex(pattern, text, secure=False)
    
    return render_template('regex.html', matches=matches)
"""

def get_secure_code():
    """Return the secure DoS code sample."""
    return """
# Secure Code - DoS Prevention
@app.route('/regex/test', methods=['POST'])
def regex_test():
    # Implement rate limiting
    client_ip = request.remote_addr
    if not rate_limiter.is_allowed(client_ip):
        return render_template('regex.html', 
                               error="Rate limit exceeded. Please try again later.")
    
    pattern = request.form['pattern']
    text = request.form['text']
    
    # Validate regex complexity to prevent ReDoS
    if is_complex_regex(pattern):
        return render_template('regex.html', 
                               error="Complex regex patterns are not allowed for security reasons.")
    
    # Process with timeout
    matches = process_regex(pattern, text, secure=True)
    
    return render_template('regex.html', matches=matches)
"""