from app import app, db
from backend.models.article import Article

with app.app_context():
    # Create sample articles
    sample_articles = [
        {
            'title': 'Getting Started with Flask',
            'content': 'Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.',
            'author': 'John Doe',
            'likes': 15,
            'bookmarks': 8
        },
        {
            'title': 'Python Best Practices 2024',
            'content': 'Learn the latest Python best practices including type hints, async programming, and modern testing strategies that will make your code more maintainable.',
            'author': 'Jane Smith',
            'likes': 23,
            'bookmarks': 12
        },
        {
            'title': 'Building RESTful APIs',
            'content': 'A comprehensive guide to building RESTful APIs with Flask. Learn about routing, request handling, authentication, and best practices for API design.',
            'author': 'Mike Johnson',
            'likes': 31,
            'bookmarks': 19
        },
        {
            'title': 'Database Design Fundamentals',
            'content': 'Understanding database design is crucial for building scalable applications. This article covers normalization, indexing, and query optimization.',
            'author': 'Sarah Williams',
            'likes': 18,
            'bookmarks': 10
        },
        {
            'title': 'Modern JavaScript Features',
            'content': 'Explore the latest JavaScript features including async/await, destructuring, spread operators, and arrow functions that make your code cleaner.',
            'author': 'Tom Brown',
            'likes': 27,
            'bookmarks': 15
        },
        {
            'title': 'CSS Grid Layout Mastery',
            'content': 'Master CSS Grid Layout with practical examples. Learn how to create complex responsive layouts with minimal code using this powerful CSS feature.',
            'author': 'Emily Davis',
            'likes': 20,
            'bookmarks': 11
        },
        {
            'title': 'Docker for Beginners',
            'content': 'Get started with Docker containerization. Learn how to create, deploy, and manage containers for your applications with this beginner-friendly guide.',
            'author': 'Chris Wilson',
            'likes': 35,
            'bookmarks': 22
        },
        {
            'title': 'Git Workflow Strategies',
            'content': 'Discover effective Git workflow strategies for team collaboration. Learn about branching models, pull requests, and code review best practices.',
            'author': 'Alex Martinez',
            'likes': 29,
            'bookmarks': 17
        },
        {
            'title': 'Web Security Essentials',
            'content': 'Protect your web applications from common security vulnerabilities. Learn about XSS, CSRF, SQL injection, and how to prevent them.',
            'author': 'Lisa Anderson',
            'likes': 42,
            'bookmarks': 28
        },
        {
            'title': 'Responsive Design Principles',
            'content': 'Create beautiful responsive websites that work on all devices. Learn about mobile-first design, breakpoints, and flexible layouts.',
            'author': 'David Taylor',
            'likes': 25,
            'bookmarks': 14
        },
        {
            'title': 'Testing Your Python Code',
            'content': 'Write better tests for your Python applications using pytest. Learn about fixtures, mocking, and test-driven development practices.',
            'author': 'Rachel Green',
            'likes': 19,
            'bookmarks': 9
        },
        {
            'title': 'Performance Optimization Tips',
            'content': 'Speed up your web applications with these performance optimization techniques. Learn about caching, lazy loading, and code splitting.',
            'author': 'Kevin White',
            'likes': 33,
            'bookmarks': 20
        }
    ]
    
    for article_data in sample_articles:
        article = Article(**article_data)
        db.session.add(article)
    
    db.session.commit()
    print(f'✅ Successfully created {len(sample_articles)} sample articles!')
