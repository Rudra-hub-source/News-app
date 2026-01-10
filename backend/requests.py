from flask import Request

def parse_article_form(req: Request):
    # Support JSON or form data
    if req.is_json:
        data = req.get_json()
    else:
        data = {
            'title': req.form.get('title'),
            'content': req.form.get('content'),
            'author': req.form.get('author')
        }
    title = (data.get('title') or '').strip()
    content = (data.get('content') or '').strip()
    if not title or not content:
        return False, 'title and content are required'
    return True, {'title': title, 'content': content, 'author': data.get('author')}
