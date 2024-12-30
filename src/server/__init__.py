from flask import Flask, render_template
from config import template_path, static_path
from src.server.routers.sobre import load_router_sobre


def create_app():
    app = Flask(__name__, template_folder=template_path, static_folder=static_path)
    app.config["SECRET_KEY"] = "secret-key-goes-here"
    load_router_sobre(app)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
