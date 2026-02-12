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
    print(f"DATABASE_URL found: {database_url is not None}")
    if database_url:
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        print(f"Using PostgreSQL: {database_url[:50]}...")
        return database_url
    print("Using SQLite fallback")
    # Use /tmp for SQLite on Render (ephemeral but works for session)
    return 'sqlite:////tmp/news.db'

app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')

# PostgreSQL connection pool settings for Render
if 'postgresql' in get_database_uri():
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'connect_timeout': 10,
            'application_name': 'news_app',
            'sslmode': 'require'
        }
    }

# Ensure upload directory exists
upload_dir = Path('instance/uploads')
upload_dir.mkdir(parents=True, exist_ok=True)

# Initialize database
try:
    from backend.state import db
    db.init_app(app)
except Exception as e:
    print(f"Database init error: {e}")
    db = None

# Import and register blueprints
try:
    from backend.router import main_bp
    app.register_blueprint(main_bp)
except ImportError:
    pass

# Create tables
if db:
    with app.app_context():
        try:
            from backend.models.article import Article, Category
            from backend.models.media import Media
            db.create_all()
            print("Database tables created successfully")
            
            # Add missing columns to existing tables (for PostgreSQL)
            try:
                from sqlalchemy import text
                # Add view_count column if missing
                try:
                    db.session.execute(text("ALTER TABLE article ADD COLUMN IF NOT EXISTS view_count INTEGER DEFAULT 0"))
                    db.session.commit()
                except:
                    pass
                
                # Add category column if missing
                try:
                    db.session.execute(text("ALTER TABLE article ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'general'"))
                    db.session.commit()
                except:
                    pass
                
                # Update existing articles to have default category
                try:
                    db.session.execute(text("UPDATE article SET category = 'general' WHERE category IS NULL"))
                    db.session.commit()
                except:
                    pass
                    
                print("Columns added/verified successfully")
            except Exception as col_error:
                print(f"Column update: {col_error}")
            
            # Check if we can query the database
            article_count = Article.query.count()
            print(f"Current article count: {article_count}")
        except Exception as e:
            print(f"Database setup error: {e}")
            import traceback
            traceback.print_exc()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/articles')
def articles_redirect():
    try:
        from backend.services.article_service import ArticleService
        q = request.args.get('q', '')
        articles = ArticleService.get_articles(q)
        categories = ArticleService.get_all_categories()
        return render_template('articles.html', articles=articles, q=q, categories=categories)
    except Exception as e:
        return f"Articles error: {e}"

@app.route('/initdb')
def init_db():
    try:
        if db:
            db.create_all()
            from backend.services.article_service import ArticleService
            existing_articles = ArticleService.get_articles()
            if len(existing_articles) == 0:
                ArticleService.create_article('Welcome to News App', 'This is your first article in the news management system.', 'Admin')
                ArticleService.create_article('Getting Started', 'Learn how to use this application.', 'Editor')
            return f'Database initialized! Found {len(ArticleService.get_articles())} articles.'
        else:
            return 'Database not available'
    except Exception as e:
        import traceback
        return f"Init DB error: {e}\n\nTraceback:\n{traceback.format_exc()}"

@app.route('/debug')
def debug():
    try:
        from backend.services.article_service import ArticleService
        articles = ArticleService.get_articles()
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')
        return f'''Debug Info:
        Database URI: {db_uri[:50]}...
        Articles found: {len(articles)}
        Database URL env: {os.environ.get('DATABASE_URL', 'Not set')[:50]}...
        '''
    except Exception as e:
        import traceback
        return f"Debug error: {e}\n\nTraceback:\n{traceback.format_exc()}"

@app.route('/setup-categories')
def setup_categories():
    """Setup route to add missing columns and create category table"""
    try:
        if db:
            from sqlalchemy import text
            db.create_all()
            
            # Add view_count column if missing
            try:
                db.session.execute(text("ALTER TABLE article ADD COLUMN IF NOT EXISTS view_count INTEGER DEFAULT 0"))
                db.session.commit()
            except:
                pass
            
            # Add category column if missing
            try:
                db.session.execute(text("ALTER TABLE article ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'general'"))
                db.session.commit()
            except:
                pass
            
            # Update existing articles to have default category
            try:
                db.session.execute(text("UPDATE article SET category = 'general' WHERE category IS NULL"))
                db.session.commit()
            except:
                pass
            
            return "Database setup completed! Columns added successfully."
        else:
            return "Database not available"
    except Exception as e:
        import traceback
        return f"Setup error: {e}\n\nTraceback:\n{traceback.format_exc()}"

if __name__ == '__main__':
    # Run on development port
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')

