from backend.state import db
from backend.models.article import Article
from datetime import datetime, timedelta

class ArticleService:
    @staticmethod
    def get_articles(q=''):
        if q:
            articles = Article.query.filter(
                Article.title.contains(q) | Article.content.contains(q)
            ).order_by(Article.created_at.desc()).all()
        else:
            articles = Article.query.order_by(Article.created_at.desc()).all()
        return articles

    @staticmethod
    def get_article(article_id):
        article = Article.query.get_or_404(article_id)
        article.view_count = (article.view_count or 0) + 1
        db.session.commit()
        return article

    @staticmethod
    def get_trending_articles(limit=10):
        return Article.query.order_by(Article.view_count.desc()).limit(limit).all()
    
    @staticmethod
    def get_latest_articles(limit=10):
        return Article.query.order_by(Article.created_at.desc()).limit(limit).all()

    @staticmethod
    def create_article(title, content, author='Anonymous'):
        a = Article(title=title, content=content, author=author or 'Anonymous')
        db.session.add(a)
        db.session.commit()
        return a

    @staticmethod
    def update_article(article_id, title, content, author):
        a = Article.query.get_or_404(article_id)
        a.title = title
        a.content = content
        a.author = author or 'Anonymous'
        db.session.commit()
        return a

    @staticmethod
    def delete_article(article_id):
        a = Article.query.get_or_404(article_id)
        db.session.delete(a)
        db.session.commit()
    
    @staticmethod
    def get_articles_paginated(q='', page=1, per_page=9):
        query = Article.query
        if q:
            query = query.filter(
                Article.title.contains(q) | Article.content.contains(q)
            )
        query = query.order_by(Article.created_at.desc())
        
        total = query.count()
        articles = query.limit(per_page).offset((page - 1) * per_page).all()
        has_more = total > (page * per_page)
        
        return articles, total, has_more