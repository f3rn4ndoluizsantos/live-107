from flask import Flask, jsonify, render_template
import requests


def load_router_sobre(app: Flask) -> Flask:
    @app.route("/sobre")
    def sobre():
        return render_template("sobre.html")

    @app.route("/posts")
    def posts():
        with app.test_client() as client:
            response = client.get("/api/posts")
            data = response.json
            if response.status_code == 200 and len(data) > 0:
                return render_template("posts.html", posts=data)
            else:
                return render_template("posts.html", posts=[])
