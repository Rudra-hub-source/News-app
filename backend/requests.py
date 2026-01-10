from flask import Request
import bleach


def parse_article_form(req: Request):
    """Parse, validate and sanitize article data from JSON or form data.

    Returns (True, payload) on success or (False, error_message) on failure.
    """
    # Support JSON or form data
    if req.is_json:
        data = req.get_json() or {}
    else:
        data = {
            'title': req.form.get('title'),
            'content': req.form.get('content'),
            'author': req.form.get('author')
        }

    title = (data.get('title') or '').strip()
    content = (data.get('content') or '').strip()
    author = (data.get('author') or '').strip() if data.get('author') else None

    # Basic validation rules
    if not title:
        return False, 'title is required'
    if not content:
        return False, 'content is required'
    if len(title) > 200:
        return False, 'title must be at most 200 characters'
    if len(content) > 10000:
        return False, 'content too long'
    if author and len(author) > 100:
        return False, 'author name too long'

    # Sanitize HTML content: allow a small set of tags and attributes
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre'
    ]
    allowed_attrs = {
        'a': ['href', 'title', 'rel', 'target']
    }
    cleaned = bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        protocols=['http', 'https', 'mailto'],
        strip=True
    )

    return True, {'title': title, 'content': cleaned, 'author': author}
