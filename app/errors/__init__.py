from flask import Blueprint, render_template

errors_bp = Blueprint("errors", __name__, template_folder="templates/errors")

from app.errors import error_handlers  # noqa: E402, F401


def return_401():
    return render_template("errors/401.html"), 401


def return_404():
    return render_template("errors/404.html"), 404


def return_500():
    return render_template("errors/500.html"), 500
