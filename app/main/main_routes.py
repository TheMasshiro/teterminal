from flask import jsonify, redirect, request, url_for
from flask_login import current_user, login_required

from app.helpers import get_municipalities
from app.main import main_bp as main
from app.main.main import Main
from app.main.main_managers import Manager


@main.route("/")
@main.route("/index")
def index():
    if not current_user.is_authenticated:
        return Main().index()
    if current_user.user_type == "admin":
        return redirect(url_for("main.dashboard_admin"))
    else:
        return redirect(url_for("main.dashboard_client"))


@main.route("/<string:username>/profile")
@login_required
def profile(username):
    return Main().profile(username)


@main.route("/dashboard/admin", methods=["GET", "POST"])
@login_required
def dashboard_admin():
    if current_user.user_type == "admin":
        return Main().dashboard_admin()
    return redirect(url_for("main.dashboard_client"))


@main.route("/dashboard/client", methods=["GET", "POST"])
@login_required
def dashboard_client():
    if current_user.user_type == "client":
        return Main().dashboard_client()
    return redirect(url_for("main.dashboard_admin"))


@main.route("/available", methods=["GET"])
@login_required
def availability():
    return Main().availability()


@main.route("/reports/admin", methods=["GET"])
@login_required
def reports():
    return Main().reports()


@main.route("/available/cars", methods=["GET"])
@login_required
def available_cars():
    return Main().available_cars()


@main.route("/available/buses", methods=["GET"])
@login_required
def available_buses():
    return Main().available_buses()


@main.route("/schedules", methods=["GET", "POST"])
@login_required
def schedules():
    return Main().schedules()


@main.route("/schedules//cars", methods=["GET"])
@login_required
def schedule_cars():
    return Main().schedules_cars()


@main.route("/schedules/buses", methods=["GET"])
@login_required
def schedule_buses():
    return Main().schedules_buses()


@main.route("/dashboard/clients/admin", methods=["GET", "POST"])
@login_required
def manage_clients():
    return Main().manage_clients()


@main.route("/dashboard/buses/admin", methods=["GET", "POST"])
@login_required
def manage_buses():
    return Main().manage_buses()


@main.route("/dashboard/cars/admin", methods=["GET", "POST"])
@login_required
def manage_cars():
    return Main().manage_cars()


@main.route("/<string:username>/profile/update", methods=["GET", "POST"])
@login_required
def update_profile(username):
    return Manager().update_profile(username)


@main.route(
    "/dashboard/manage/clients/<string:client_username>/edit", methods=["GET", "POST"]
)
@login_required
def edit_client(client_username):
    return Manager().edit_client(client_username)


@main.route(
    "/dashboard/manage/clients/<string:client_username>/delete", methods=["POST"]
)
@login_required
def delete_client(client_username):
    return Manager().delete_client(client_username)


@main.route("/dashboard/manage/fleet/<string:type>/add", methods=["GET", "POST"])
@login_required
def add_vehicle(type):
    return Manager().add_vehicle(type=type)


@main.route(
    "/dashboard/manage/fleet/edit/<string:type>/<string:plate_number>/<string:bus_number>/<string:car_number>",
    methods=["GET", "POST"],
)
@login_required
def edit_vehicle(type, plate_number, bus_number, car_number):
    return Manager().edit_vehicle(
        type=type,
        plate_number=plate_number,
        bus_number=bus_number,
        car_number=car_number,
    )


@main.route(
    "/dashboard/manage/fleet/delete/<string:type>/<string:plate_number>/<string:bus_number>/<string:car_number>",
    methods=["POST"],
)
@login_required
def delete_vehicle(type, plate_number, bus_number, car_number):
    return Manager().delete_vehicle(
        type=type,
        plate_number=plate_number,
        bus_number=bus_number,
        car_number=car_number,
    )


@main.route("/fetch_municipalities", methods=["GET"])
@login_required
def fetch_municipalities():
    province = request.args.get("province")
    municipalities = get_municipalities(province)
    return jsonify(municipalities)
