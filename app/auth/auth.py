from abc import ABC, abstractmethod
from typing import Any

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app.forms import AdminForm, CreateAdmin, CreateClient
from app.models.users import User


class AuthInterface(ABC):
    @abstractmethod
    def login_admin(self) -> Any:
        pass

    @abstractmethod
    def login_client(self) -> Any:
        pass

    @abstractmethod
    def create_admin(self) -> Any:
        pass

    @abstractmethod
    def signup_client(self) -> Any:
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

    def create_admin(self):
        if current_user.is_authenticated:
            if current_user.user_type == "admin":
                return redirect(url_for("main.dashboard_admin"))
            return redirect(url_for("main.dashboard_client"))
        form = CreateAdmin()
        if form.validate_on_submit():
            admin = User(
                username=form.username.data,
                email=form.email.data,
                last_name=form.last_name.data,
            )
            admin.set_password(form.password.data)
            if not admin.create_admin():
                flash("An error has occurred", "danger")
                return redirect(url_for("auth.create_admin"))
            flash("Created", "success")
            try:
                login_user(admin.get_admin())
            except Exception as e:
                print(f"Error: {e}")

            return redirect(url_for("main.dashboard_admin"))

        return render_template(
            "auth/register.html",
            title="Admin Creation",
            page="Create Admin",
            page_type="Admin",
            form=form,
            back="/login/admin",
        )

    def signup_client(self):
        if current_user.is_authenticated:
            if current_user.user_type == "admin":
                return redirect(url_for("main.dashboard_admin"))
            return redirect(url_for("main.dashboard_client"))
        form = CreateClient()
        if form.validate_on_submit():
            if form.username.data is None or form.username.data.lower() == "admin":
                flash("An error has occurred", "danger")
                return redirect(url_for("auth.signup_client"))

            client = User(
                username=form.username.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
            )
            client.set_password(form.password.data)
            if not client.create_user():
                flash("An error has occurred", "danger")
                return redirect(url_for("auth.signup_client"))
            flash("Created", "success")
            try:
                login_user(client.get_specific_user())
            except Exception as e:
                print(f"Error: {e}")

            return redirect(url_for("main.dashboard_client"))

        return render_template(
            "auth/register.html",
            title="Sign Up Client",
            page="Sign Up",
            page_type="Client",
            form=form,
            back="/login/client",
        )

    def logout(self):
        """Logout User"""
        logout_user()
        return redirect(url_for("main.index"))
