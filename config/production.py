# Production Configuration
import os

DEBUG = False
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/news_app')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'production-secret-key-change-this')
UPLOAD_FOLDER = 'instance/uploads'