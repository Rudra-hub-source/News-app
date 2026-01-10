from flask import request
import time

def request_logger(app):
    @app.before_request
    def _log():
        request._start_time = time.time()

    @app.after_request
    def _after(resp):
        dur = (time.time() - getattr(request, '_start_time', time.time()))
        app.logger.debug(f"{request.method} {request.path} {resp.status_code} {dur:.3f}s")
        return resp
