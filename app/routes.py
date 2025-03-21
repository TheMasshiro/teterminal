from flask import render_template, request

from app import app


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        user = {"username": "Vicente"}
        return render_template("index.html", title="Home", user=user)
    return "This is a POST request"
