from backend.state import db
from backend.models.article import Article

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
        return Article.query.get_or_404(article_id)

    @staticmethod
    def create_article(title, content, author):
        a = Article(title=title, content=content, author=author)
        db.session.add(a)
        db.session.commit()

    @staticmethod
    def update_article(article_id, title, content, author):
        a = Article.query.get_or_404(article_id)
        a.title = title
        a.content = content
        a.author = author
        db.session.commit()

    @staticmethod
    def delete_article(article_id):
        a = Article.query.get_or_404(article_id)
        db.session.delete(a)
        db.session.commit()
