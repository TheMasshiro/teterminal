from abc import ABC, abstractmethod
from typing import Any

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app.forms import AdminForm, RegisterClient
from app.models.users import User


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
            if current_user.user_type == "admin":
                return redirect(url_for("main.dashboard_admin"))
            return redirect(url_for("main.dashboard_client"))
        form = AdminForm()
        if form.validate_on_submit():
            admin = User(
                username=form.username.data, password_hash=form.password.data
            ).get_admin()

            if admin is None or not admin.check_password(form.password.data):
                flash("Invalid username or password.", "danger")
                return redirect(url_for("auth.login_admin"))
            try:
                login_user(admin, remember=form.remember_me.data)
            except Exception as e:
                print(f"Error: {e}")
            return redirect(url_for("main.dashboard_admin"))

        return render_template(
            "auth/login.html",
            title="Admin Sign In",
            page_title="Admin",
            form=form,
            home="/dashboard/admin/",
        )

    def login_client(self):
        if current_user.is_authenticated:
            if current_user.user_type == "admin":
                return redirect(url_for("main.dashboard_admin"))
            return redirect(url_for("main.dashboard_client"))
        form = AdminForm()
        if form.validate_on_submit():
            client = User(
                username=form.username.data, password_hash=form.password.data
            ).get_specific_user()

            if client is None or not client.check_password(form.password.data):
                flash("Invalid username or password.", "danger")
                return redirect(url_for("auth.login_client"))
            try:
                login_user(client, remember=form.remember_me.data)
            except Exception as e:
                print(f"Error: {e}")
            return redirect(url_for("main.dashboard_client"))

        return render_template(
            "auth/login.html",
            title="Client Sign In",
            page_title="Client",
            form=form,
            home="/dashboard/client/",
        )

    def register_client(self):
        if current_user.is_authenticated:
            if current_user.user_type == "admin":
                return redirect(url_for("main.dashboard_admin"))
            return redirect(url_for("main.dashboard_client"))
        form = RegisterClient()
        if form.validate_on_submit():
            if form.username.data is None or form.username.data.lower() == "admin":
                flash("An error has occurred", "danger")
                return redirect(url_for("auth.register_client"))

            client_name = ""
            if form.first_name.data is not None and form.last_name.data is not None:
                client_name = (
                    f"{form.first_name.data.title()} {form.last_name.data.title()}"
                )

            client = User(
                username=form.username.data, email=form.email.data, name=client_name
            )
            client.set_password(form.password.data)
            if not client.create_user():
                flash("An error has occurred", "danger")
                return redirect(url_for("auth.register_client"))
            flash("Created", "success")
            try:
                login_user(client.get_specific_user())
            except Exception as e:
                print(f"Error: {e}")

            return redirect(url_for("main.dashboard_client"))

        return render_template("auth/register.html", title="Register Client", form=form)

    def logout(self):
        """Logout User"""
        logout_user()
        return redirect(url_for("main.index"))
