from flask import render_template

from app.errors import errors_bp as errors


@errors.app_errorhandler(401)
def unauthorized_error(error):
    return render_template("errors/401.html", title="Unauthorized Access"), 401


@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html", title="Page Not Found"), 404


@errors.app_errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html", title="Internal Server Error"), 500
