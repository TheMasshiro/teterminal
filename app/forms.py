import re

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired

from app.models.users import User


class AdminForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")
    remember_me = BooleanField("Remember Me")


class ClientForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")
    remember_me = BooleanField("Remember Me")


class RegisterClient(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        client = User.get_user_username(username.data)
        if client is not None:
            raise ValidationError("Username is already taken")

    def validate_email(self, email):
        client = User.get_user_email(email.data)
        if client is not None:
            raise ValidationError("Email is already taken")

    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search("[a-z]", password.data):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search("[A-Z]", password.data):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search("[0-9]", password.data):
            raise ValidationError("Password must contain at least one number.")
        if re.search(r"\s", password.data):
            raise ValidationError("Password cannot contain spaces.")
