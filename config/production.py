# Production Configuration
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///database/instance/news.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'production-secret-key-change-this'
UPLOAD_FOLDER = 'database/instance/uploads'