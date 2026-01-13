import requests
BASE = 'http://127.0.0.1:3000'

def test_list_articles():
    r = requests.get(BASE + '/api/articles')
    assert r.status_code == 200
    j = r.json()
    assert 'data' in j

def test_create_and_delete_article():
    payload = {'title':'Test from pytest','content':'body','author':'tester'}
    r = requests.post(BASE + '/api/articles', json=payload)
    assert r.status_code in (200,201)
    j = r.json()
    aid = j.get('data', {}).get('id') if isinstance(j.get('data'), dict) else None
    assert aid is not None
    # delete
    r2 = requests.delete(BASE + f'/api/articles/{aid}')
    assert r2.status_code == 200


def test_validation_failures():
    # missing title
    payload = {'title':'','content':'x','author':'t'}
    r = requests.post(BASE + '/api/articles', json=payload)
    assert r.status_code == 400
    # too long title
    payload = {'title':'x'*300,'content':'x','author':'t'}
    r2 = requests.post(BASE + '/api/articles', json=payload)
    assert r2.status_code == 400
