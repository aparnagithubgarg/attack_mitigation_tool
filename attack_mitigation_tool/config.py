import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration for the application."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-demonstration-only'
    
    # Database configuration
    DB_HOST = os.environ.get('DB_HOST') or '127.0.0.1'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'Aparna_2024'
    DB_NAME = os.environ.get('DB_NAME') or 'attack_mitigation_tool'
    
    # Toggle between secure and insecure versions
    DEFAULT_SECURE = False