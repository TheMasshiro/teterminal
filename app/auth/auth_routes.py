from flask_login import login_required

from app.auth import auth_bp as auth

from .auth import Auth


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    return Auth().logout()


@auth.route("/login/admin", methods=["GET", "POST"])
def login_admin():
    return Auth().login_admin()


@auth.route("/login/client", methods=["GET", "POST"])
def login_client():
    return Auth().login_client()


@auth.route("/register/client", methods=["GET", "POST"])
def register_client():
    return Auth().register_client()
