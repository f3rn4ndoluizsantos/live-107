from flask import Flask, jsonify, render_template


def load_router_sobre(app: Flask) -> Flask:
    @app.route("/sobre")
    def sobre():
        return render_template("sobre.html")

    # @app.route("/sobre")
    # def sobre():
    #     return jsonify({"mensagem": "Exemplo de rota"}), 200
