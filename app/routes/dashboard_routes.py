from flask import Blueprint, render_template
from flask_login import login_required

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
def home():
    return render_template("index.html")


@dashboard.route("/dashboard")
@login_required
def dashboard_page():
    return render_template("dashboard.html")
