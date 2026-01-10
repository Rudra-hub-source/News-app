from flask import jsonify

def ok(message='OK', data=None):
    resp = {'status': 'ok', 'message': message}
    if data is not None:
        resp['data'] = data
    return jsonify(resp), 200

def created(message='Created', data=None):
    resp = {'status': 'created', 'message': message}
    if data is not None:
        resp['data'] = data
    return jsonify(resp), 201

def error(message='Error', code=400):
    return jsonify({'status': 'error', 'message': message}), code

def not_found(message='Not found'):
    return jsonify({'status': 'error', 'message': message}), 404
