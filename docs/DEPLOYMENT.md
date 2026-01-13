# Deployment Guide

## Local Development
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Initialize database: Visit `/initdb` endpoint
6. Run application: `python app.py`

## Production Deployment
1. Set environment variables
2. Use production configuration
3. Set up reverse proxy (nginx)
4. Use WSGI server (gunicorn)
5. Configure SSL certificates
6. Set up monitoring and logging