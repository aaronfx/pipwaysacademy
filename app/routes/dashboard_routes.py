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


@dashboard.route("/journal")
@login_required
def journal():
    return render_template("journal.html")


@dashboard.route("/analysis")
@login_required
def analysis():
    return render_template("analysis.html")


@dashboard.route("/mentor")
@login_required
def mentor():
    return render_template("mentor.html")


@dashboard.route("/blog")
def blog():
    return render_template("blog.html")


@dashboard.route("/webinars")
def webinars():
    return render_template("webinars.html")


@dashboard.route("/courses")
def courses():
    return render_template("courses.html")
