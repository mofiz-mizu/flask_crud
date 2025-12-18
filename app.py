from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, User
import time

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        for _ in range(10):
            try:
                db.create_all()
                break
            except Exception:
                time.sleep(2)

    @app.route("/")
    def index():
        users = User.query.all()
        return render_template("index.html", users=users)

    @app.route("/create", methods=["GET", "POST"])
    def create():
        if request.method == "POST":
            user = User(
                name=request.form["name"],
                email=request.form["email"]
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("create.html")

    @app.route("/edit/<int:user_id>", methods=["GET", "POST"])
    def edit(user_id):
        user = User.query.get_or_404(user_id)
        if request.method == "POST":
            user.name = request.form["name"]
            user.email = request.form["email"]
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("edit.html", user=user)

    @app.route("/delete/<int:user_id>")
    def delete(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("index"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
