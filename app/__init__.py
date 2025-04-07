from flask import Flask
from flask_login import LoginManager

from instance.config import Config

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)


def start_db():
    from app.models.models import create_tables

    return create_tables()


start_db()

from app.auth import auth_bp  # noqa: E402
from app.main import main_bp  # noqa: E402

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
