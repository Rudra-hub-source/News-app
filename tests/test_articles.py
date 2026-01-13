# Test cases for article functionality
import pytest
from backend.services.article_service import ArticleService

def test_create_article():
    \"\"\"Test article creation\"\"\"
    article = ArticleService.create_article(\"Test Title\", \"Test Content\", \"Test Author\")\n    assert article.title == \"Test Title\"\n    assert article.content == \"Test Content\"\n    assert article.author == \"Test Author\"\n\ndef test_get_articles():\n    \"\"\"Test getting all articles\"\"\"\n    articles = ArticleService.get_articles()\n    assert isinstance(articles, list)