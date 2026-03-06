from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from ..models.user_model import User
from ..extensions import db, bcrypt

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("dashboard.home"))

        flash("Invalid email or password")

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(email=email, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/logout")
def logout():

    logout_user()

    return redirect(url_for("auth.login"))
