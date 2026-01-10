from flask import Request
def parse_article_form(req: Request):
    """Parse and validate article data from JSON or form data.

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

    return True, {'title': title, 'content': content, 'author': author}
