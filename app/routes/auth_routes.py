from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from ..models.user_model import User
from ..extensions import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard.dashboard_page"))

    return render_template("login.html")


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
