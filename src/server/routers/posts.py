from flask import Flask, jsonify, render_template


def load_router_posts(app: Flask) -> Flask:
    @app.route("/api/posts", methods=["GET"])
    def api_posts():
        list_posts = [
            {
                "id": 1,
                "title": "Post 1",
                "content": "Conteúdo do post 1",
            },
            {
                "id": 2,
                "title": "Post 2",
                "content": "Conteúdo do post 2",
            },
            {
                "id": 3,
                "title": "Post 3",
                "content": "Conteúdo do post 3",
            },
        ]
        return jsonify(list_posts), 200
