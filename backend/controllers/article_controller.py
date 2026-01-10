from flask import Blueprint, jsonify, request
from backend.responses import ok, created, error, not_found
from backend.requests import parse_article_form
from backend.services.article_service import (
    list_articles, get_article, create_article, update_article, delete_article
)

bp = Blueprint('articles_api', __name__)


@bp.route('/articles', methods=['GET'])
def api_list_articles():
    q = request.args.get('q')
    items = list_articles(q)
    data = [
        {"id": a.id, "title": a.title, "author": a.author, "created_at": a.created_at.isoformat()}
        for a in items
    ]
    return ok(data=data)


@bp.route('/articles/<int:article_id>', methods=['GET'])
def api_get_article(article_id):
    a = get_article(article_id)
    if not a:
        return not_found('Article not found')
    return ok(data={"id": a.id, "title": a.title, "content": a.content, "author": a.author, "created_at": a.created_at.isoformat()})


@bp.route('/articles', methods=['POST'])
def api_create_article():
    valid, payload = parse_article_form(request)
    if not valid:
        return error(payload)
    a = create_article(payload['title'], payload['content'], payload.get('author'))
    return created(data={"id": a.id})


@bp.route('/articles/<int:article_id>', methods=['PUT', 'PATCH'])
def api_update_article(article_id):
    valid, payload = parse_article_form(request)
    if not valid:
        return error(payload)
    a = update_article(article_id, payload['title'], payload['content'], payload.get('author'))
    if not a:
        return not_found('Article not found')
    return ok(data={"id": a.id})


@bp.route('/articles/<int:article_id>', methods=['DELETE'])
def api_delete_article(article_id):
    ok_del = delete_article(article_id)
    if not ok_del:
        return not_found('Article not found')
    return ok(data={"deleted": True})
