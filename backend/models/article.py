from backend.state import db
from datetime import datetime, timezone, timedelta

# IST timezone (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_time():
    return datetime.now(IST)

# Article categories
ARTICLE_CATEGORIES = [
    ('business', 'Business'),
    ('entertainment', 'Entertainment'),
    ('general', 'General'),
    ('health', 'Health'),
    ('science', 'Science'),
    ('sports', 'Sports'),
    ('technology', 'Technology'),
    ('india', 'India'),
]

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default='Anonymous')
    category = db.Column(db.String(50), default='general')
    view_count = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    bookmarks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=get_ist_time)


class Category(db.Model):
    """Model to store custom categories created by users"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=get_ist_time)
