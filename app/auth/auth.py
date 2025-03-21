from abc import ABC, abstractmethod
from typing import Any

from flask import redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app.forms import AdminForm
from app.models.users import Admin


class AuthInterface(ABC):
    @abstractmethod
    def login_admin(self) -> Any:
        pass

    @abstractmethod
    def login_client(self) -> Any:
        pass

    @abstractmethod
    def register_client(self) -> Any:
        pass

    @abstractmethod
    def logout(self) -> Any:
        pass


class Auth(AuthInterface):
    def login_admin(self):
        if current_user.is_authenticated:
            return redirect(url_for("dashboard_admin"))
        form = AdminForm()
        if form.validate_on_submit():
            admin = Admin(
                username=form.username.data, password_hash=form.password.data
            ).get_admin()

            if admin is None or not admin.check_password(form.password.data):
                print("Login Failed")
            try:
                login_user(admin)
            except Exception as e:
                print(f"Error: {e}")
            return redirect(url_for("dashboard_admin"))

        return render_template("auth/admin.html", title="Admin Sign In", form=form)

    def login_client(self):
        pass

    def register_client(self):
        pass

    def logout(self):
        """Logout User"""
        logout_user()
        return redirect(url_for("auth.login"))
