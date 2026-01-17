from flask import Flask, render_template, request
import os
from pathlib import Path

# Create Flask app first
app = Flask(__name__, 
           template_folder='frontend/templates',
           static_folder='frontend/static')

# Database configuration
def get_database_uri():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        return database_url
    return 'postgresql://postgres:password@localhost:5432/news_app'

app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')

# Ensure upload directory exists
upload_dir = Path('instance/uploads')
upload_dir.mkdir(parents=True, exist_ok=True)

# Initialize database
from backend.state import db
db.init_app(app)

# Import and register blueprints
try:
    from backend.router import main_bp
    app.register_blueprint(main_bp)
except ImportError:
    pass

# Create tables
with app.app_context():
    try:
        from backend.models.article import Article
        from backend.models.media import Media
        db.create_all()
    except Exception as e:
        print(f"Database setup error: {e}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/articles')
def articles_redirect():
    try:
        from backend.services.article_service import ArticleService
        q = request.args.get('q', '')
        articles = ArticleService.get_articles(q)
        return render_template('articles.html', articles=articles, q=q)
    except Exception as e:
        return f"Articles error: {e}"

@app.route('/initdb')
def init_db():
    try:
        db.create_all()
        from backend.services.article_service import ArticleService
        if len(ArticleService.get_articles()) == 0:
            ArticleService.create_article('Test Article', 'This is a test article content.', 'Test Author')
        return 'Database initialized with test data!'
    except Exception as e:
        return f"Init DB error: {e}"

@app.route('/debug')
def debug():
    try:
        from backend.services.article_service import ArticleService
        articles = ArticleService.get_articles()
        return f'Found {len(articles)} articles in database'
    except Exception as e:
        return f"Debug error: {e}"

if __name__ == '__main__':
    # Run on development port
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')
