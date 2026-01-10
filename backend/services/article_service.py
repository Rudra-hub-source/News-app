from typing import Optional, List
from app import db
from app import Article

def list_articles(query: Optional[str] = None) -> List[Article]:
    q = Article.query
    if query:
        q = q.filter(Article.title.contains(query) | Article.content.contains(query))
    return q.order_by(Article.created_at.desc()).all()

def get_article(article_id: int) -> Optional[Article]:
    return Article.query.get(article_id)

def create_article(title: str, content: str, author: str = None) -> Article:
    a = Article(title=title, content=content, author=author)
    db.session.add(a)
    db.session.commit()
    return a

def update_article(article_id: int, title: str, content: str, author: str = None) -> Optional[Article]:
    a = Article.query.get(article_id)
    if not a:
        return None
    a.title = title
    a.content = content
    a.author = author
    db.session.commit()
    return a

def delete_article(article_id: int) -> bool:
    a = Article.query.get(article_id)
    if not a:
        return False
    db.session.delete(a)
    db.session.commit()
    return True
