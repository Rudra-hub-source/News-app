# Development Configuration
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/news_app'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'dev-secret-key'
UPLOAD_FOLDER = 'instance/uploads'