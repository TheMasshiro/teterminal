from flask_login import login_required

from app.main import main_bp as main
from app.main.main import Main


@main.route("/")
@main.route("/index")
def index():
    return Main().index()


@main.route("/dashboard/admin", methods=["GET", "POST"])
@login_required
def dashboard_admin():
    return Main().dashboard_admin()


@main.route("/dashboard/client", methods=["GET", "POST"])
def dashboard_client():
    return Main().dashboard_client()
