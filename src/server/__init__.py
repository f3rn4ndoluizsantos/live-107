from flask import Flask, render_template, request, Response
from config import template_path, static_path
from src.server.routers.sobre import load_router_sobre
from src.server.routers.posts import load_router_posts
from src.server.routers.pdf_reader import load_router_pdf_reader


class Validator:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, response):
        # print("Validator")
        # print(environ)
        # res = Response("Hello, World!", mimetype="text/plain", status=200)
        # return res(environ, response)
        return self.app(environ, response)


def create_app():
    app = Flask(__name__, template_folder=template_path, static_folder=static_path)
    app.config["SECRET_KEY"] = "secret-key-goes-here"
    load_router_posts(app)
    load_router_sobre(app)
    load_router_pdf_reader(app)
    app.wsgi_app = Validator(app.wsgi_app)

    # # Before request middleware
    # @app.before_request
    # def before_request_func():
    #     print(request)
    #     print("Before Request: Processing request for", request.path)

    # # After request middleware
    # @app.after_request
    # def after_request_func(response):
    #     print("After Request: Processing response for", request.path)
    #     return response

    @app.route("/")
    def home():
        # return "home"
        return render_template("index.html")

    @app.route("/contacts")
    def contacts():
        # return "home"
        return render_template("contacts.html")

    return app
