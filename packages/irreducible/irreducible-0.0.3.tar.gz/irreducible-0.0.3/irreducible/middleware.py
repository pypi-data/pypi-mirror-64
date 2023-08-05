from webob import Request

class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        req = Request(environ)
        res = self.app.handle_request(req)
        return res(environ, start_response)

    def add(self, middleware_cls):
        self.app = middleware_cls(self.app)

    def process_request(self, req):
        pass

    def process_response(self, req, res):
        pass

    def handle_request(self, req):
        self.process_request(req)
        res = self.app.handle_request(req)
        self.process_response(req, res)
        return res
