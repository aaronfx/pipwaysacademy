import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///trading_academy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    ALLOWED_EXTENSIONS = {
        'pdf', 'csv', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'txt', 'xlsx'
    }
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY') or 'your-openrouter-api-key'
    OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'
    
    # AI Model Configuration
    AI_MODEL = 'anthropic/claude-3.5-sonnet'
    
    # Application Settings
    APP_NAME = 'Trading Academy Pro'
    APP_VERSION = '1.0.0'
