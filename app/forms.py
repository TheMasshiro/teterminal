import re

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, NumberRange

from app.helpers import get_provinces
from app.models.users import User
from instance.config import Config


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


class CreateAdmin(FlaskForm):
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    admin_code = PasswordField("Admin Code", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Create")

    def validate_admin_code(self, admin_code):
        if admin_code.data != Config.CREATE_ADMIN:
            raise ValidationError("Admin Code is Incorrect.")

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


class CreateClient(FlaskForm):
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


class UpdateProfile(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Update")

    def validate_first_name(self, field):
        if current_user.user_type == "admin":
            field.data = "Administrator"

    def validate_new_password(self, new_password):
        if len(new_password.data) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search("[a-z]", new_password.data):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search("[A-Z]", new_password.data):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search("[0-9]", new_password.data):
            raise ValidationError("Password must contain at least one number.")
        if re.search(r"\s", new_password.data):
            raise ValidationError("Password cannot contain spaces.")
        if self.confirm_password.data != new_password.data:
            raise ValidationError("Passwords do not match.")
        if self.old_password.data == new_password.data:
            raise ValidationError(
                "New password must be different from the old password."
            )

    def validate_confirm_password(self, confirm_password):
        if self.new_password.data != confirm_password.data:
            raise ValidationError("Passwords do not match.")
        if self.old_password.data == confirm_password.data:
            raise ValidationError(
                "New password must be different from the old password."
            )

    def validate_old_password(self, old_password):
        if current_user.user_type == "admin":
            user = User(
                username=current_user.username, password_hash=old_password.data
            ).get_admin()
        else:
            user = User(
                username=current_user.username, password_hash=old_password.data
            ).get_specific_user()

        if user is None or not user.check_password(old_password.data):
            raise ValidationError("Old password is incorrect.")


class EditClient(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    new_password = PasswordField("Change Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Edit")

    def validate_new_password(self, new_password):
        if len(new_password.data) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search("[a-z]", new_password.data):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search("[A-Z]", new_password.data):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search("[0-9]", new_password.data):
            raise ValidationError("Password must contain at least one number.")
        if re.search(r"\s", new_password.data):
            raise ValidationError("Password cannot contain spaces.")
        if self.confirm_password.data != new_password.data:
            raise ValidationError("Passwords do not match.")

    def validate_confirm_password(self, confirm_password):
        if self.new_password.data != confirm_password.data:
            raise ValidationError("Passwords do not match.")


class AddBus(FlaskForm):
    vehicle_number = StringField("Bus Number", validators=[DataRequired()])
    plate_number = StringField("Plate Number", validators=[DataRequired()])
    from_province = SelectField(
        "Province",
        choices=[("", "Select a Province")]
        + [(province, province) for province in get_provinces()],
        validators=[DataRequired()],
    )
    from_city = SelectField(
        "City/Municipality", choices=[], validators=[DataRequired()]
    )
    to_province = SelectField(
        "Province",
        choices=[("", "Select a Province")]
        + [(province, province) for province in get_provinces()],
        validators=[DataRequired()],
    )
    to_city = SelectField("City/Municipality", choices=[], validators=[DataRequired()])
    avg_speed = IntegerField(
        "Average Speed",
        validators=[
            DataRequired(),
            NumberRange(
                min=20, max=120, message="Speed must be between 20 and 120 km/h"
            ),
        ],
    )
    status = SelectField(
        "Status",
        choices=[
            ("", "Available Status"),
            ("Arrived At Destination", "Arrived At Destination"),
            ("Available", "Available"),
            ("In Transit", "In Transit"),
            ("Maintenance", "Maintenance"),
            ("Shift Over", "Shift Over"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Add")


class AddCar(FlaskForm):
    vehicle_number = StringField("Car Number", validators=[DataRequired()])
    plate_number = StringField("Plate Number", validators=[DataRequired()])
    from_province = SelectField(
        "Province",
        choices=[("", "Select a Province")]
        + [(province, province) for province in get_provinces()],
        validators=[DataRequired()],
    )
    from_city = SelectField(
        "City/Municipality", choices=[], validators=[DataRequired()]
    )
    to_province = SelectField(
        "Province",
        choices=[("", "Select a Province")]
        + [(province, province) for province in get_provinces()],
        validators=[DataRequired()],
    )
    to_city = SelectField("City/Municipality", choices=[], validators=[DataRequired()])
    avg_speed = IntegerField(
        "Average Speed",
        validators=[
            DataRequired(),
            NumberRange(
                min=20, max=120, message="Speed must be between 20 and 120 km/h"
            ),
        ],
    )
    status = SelectField(
        "Status",
        choices=[
            ("", "Available Status"),
            ("Arrived At Destination", "Arrived At Destination"),
            ("Available", "Available"),
            ("In Transit", "In Transit"),
            ("Maintenance", "Maintenance"),
            ("Shift Over", "Shift Over"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Add")


class EditBus(FlaskForm):
    vehicle_number = StringField("Bus Number", validators=[DataRequired()])
    plate_number = StringField("Plate Number", validators=[DataRequired()])
    from_province = SelectField(
        "Province",
        choices=[("", "Select a Province")]
        + [(province, province) for province in get_provinces()],
        validators=[DataRequired()],
    )
    from_city = SelectField(
        "City/Municipality", choices=[], validators=[DataRequired()]
    )
    to_province = SelectField(
        "Province",
        choices=[("", "Select a Province")]
        + [(province, province) for province in get_provinces()],
        validators=[DataRequired()],
    )
    to_city = SelectField("City/Municipality", choices=[], validators=[DataRequired()])
    avg_speed = IntegerField(
        "Average Speed",
        validators=[
            DataRequired(),
            NumberRange(
                min=20, max=120, message="Speed must be between 20 and 120 km/h"
            ),
        ],
    )
    status = SelectField(
        "Status",
        choices=[
            ("", "Available Status"),
            ("Arrived At Destination", "Arrived At Destination"),
            ("Available", "Available"),
            ("In Transit", "In Transit"),
            ("Maintenance", "Maintenance"),
            ("Shift Over", "Shift Over"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Edit")


class EditCar(FlaskForm):
    vehicle_number = StringField("Car Number", validators=[DataRequired()])
    plate_number = StringField("Plate Number", validators=[DataRequired()])
    from_province = SelectField(
        "Province",
        choices=[("", "Select a Province")]
        + [(province, province) for province in get_provinces()],
        validators=[DataRequired()],
    )
    from_city = SelectField(
        "City/Municipality", choices=[], validators=[DataRequired()]
    )
    to_province = SelectField(
        "Province",
        choices=[("", "Select a Province")]
        + [(province, province) for province in get_provinces()],
        validators=[DataRequired()],
    )
    to_city = SelectField("City/Municipality", choices=[], validators=[DataRequired()])
    avg_speed = IntegerField(
        "Average Speed",
        validators=[
            DataRequired(),
            NumberRange(
                min=20, max=120, message="Speed must be between 20 and 120 km/h"
            ),
        ],
    )
    status = SelectField(
        "Status",
        choices=[
            ("", "Available Status"),
            ("Arrived At Destination", "Arrived At Destination"),
            ("Available", "Available"),
            ("In Transit", "In Transit"),
            ("Maintenance", "Maintenance"),
            ("Shift Over", "Shift Over"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Edit")
