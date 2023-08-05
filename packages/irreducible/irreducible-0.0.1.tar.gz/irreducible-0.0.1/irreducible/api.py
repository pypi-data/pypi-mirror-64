import os
import inspect

from jinja2 import Environment, FileSystemLoader
from parse import parse
from requests import Session as RequestsSession
from webob import Request
from whitenoise import WhiteNoise
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from .middleware import Middleware
from .response import Response

class API:
    def __init__(self, template_dir="templates", static_dir="static"):
        self.routes = {}
        self.templates_env = Environment(loader=FileSystemLoader(os.path.abspath(template_dir)))
        self.exception_handler = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response):
        # distinguish static file request from other requests
        path_info = environ["PATH_INFO"]

        if path_info.startswith("/static"):
            environ["PATH_INFO"] = path_info[len("/static"):]
            return self.whitenoise(environ, start_response)

        return self.middleware(environ, start_response)

    def wsgi_app(self, environ, start_response):
        req = Request(environ)
        res = self.handle_request(req)
        return res(environ, start_response)

    def handle_request(self, req):
        res = Response()

        handler_data, params = self.find_handler(request_path=req.path)

        try:
            if handler_data:
                handler = handler_data["handler"]
                allowed_methods = handler_data["allowed_methods"]
                if inspect.isclass(handler):
                    handler = getattr(handler(), req.method.lower(), None)
                    if not handler:
                        raise AttributeError("Method not allowed", req.method)
                else:
                    if req.method.lower() not in allowed_methods:
                        raise AttributeError("Method not allowed", req.method)
                handler(req, res, **params)
            else:
                self.default_handler(req, res)
        except Exception as e:
            if self.exception_handler:
                self.exception_handler(req, res, e)
            else:
                raise e

        return res

    def find_handler(self, request_path):
        for path, handler_data in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result:
                return handler_data, parse_result.named
        return None, None

    def add_route(self, path, handler, allowed_methods=None):
        assert path not in self.routes, f"Route {path} already exists."

        if allowed_methods is None:
            allowed_methods = ['get', 'post', 'put', 'patch', 'delete', 'options']

        self.routes[path] = {
                "handler": handler,
                "allowed_methods": allowed_methods
                }

    def route(self, path, allowed_methods=None):
        def wrapper(handler):
            self.add_route(path, handler, allowed_methods)
            return handler

        return wrapper

    def default_handler(self, req, res):
        res.status_code = 404
        res.text = "Not found."

    def template(self, template_name, context=None):
        if not context:
            context = {}

        return self.templates_env.get_template(template_name).render(**context)
    
    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

