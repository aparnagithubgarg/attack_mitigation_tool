import os
from utils.helpers import validate_file_path

def get_file_content(filename, secure=False):
    """
    Get the content of a file.
    
    Args:
        filename (str): The name of the file to retrieve
        secure (bool): Whether to use secure practices
        
    Returns:
        str: File content or error message
    """
    base_dir = "static/files"
    
    if secure:
        # Validate the file path to prevent directory traversal
        if not validate_file_path(filename):
            return "Invalid file path."
        
        # Normalize path and ensure it's within the base directory
        full_path = os.path.normpath(os.path.join(base_dir, filename))
        if not full_path.startswith(os.path.normpath(base_dir)):
            return "Access denied: Path traversal attempt detected."
    else:
        # Vulnerable to directory traversal
        full_path = os.path.join(base_dir, filename)
    
    try:
        with open(full_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {filename}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_vulnerable_code():
    """Return the vulnerable directory traversal code sample."""
    return """
# Vulnerable Code - Directory Traversal
@app.route('/files/<path:filename>')
def get_file(filename):
    base_dir = "static/files"
    # Directly joining paths without validation
    full_path = os.path.join(base_dir, filename)
    
    try:
        with open(full_path, 'r') as f:
            content = f.read()
        return render_template('file_viewer.html', filename=filename, content=content)
    except FileNotFoundError:
        return render_template('file_viewer.html', filename=filename, 
                              error=f"File not found: {filename}")
    except Exception as e:
        return render_template('file_viewer.html', filename=filename, 
                              error=f"Error reading file: {str(e)}")
"""

def get_secure_code():
    """Return the secure directory traversal code sample."""
    return """
# Secure Code - Directory Traversal Prevention
@app.route('/files/<path:filename>')
def get_file(filename):
    base_dir = "static/files"
    
    # Validate file path
    if '..' in filename or filename.startswith('/') or '~' in filename:
        return render_template('file_viewer.html', filename=filename, 
                              error="Invalid file path.")
    
    # Normalize path and ensure it's within the base directory
    full_path = os.path.normpath(os.path.join(base_dir, filename))
    if not full_path.startswith(os.path.normpath(base_dir)):
        return render_template('file_viewer.html', filename=filename, 
                              error="Access denied: Path traversal attempt detected.")
    
    try:
        with open(full_path, 'r') as f:
            content = f.read()
        return render_template('file_viewer.html', filename=filename, content=content)
    except FileNotFoundError:
        return render_template('file_viewer.html', filename=filename, 
                              error=f"File not found: {filename}")
    except Exception as e:
        return render_template('file_viewer.html', filename=filename, 
                              error=f"Error reading file: {str(e)}")
"""