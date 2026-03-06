from flask import Blueprint, render_template
from flask_login import login_required

courses = Blueprint("courses", __name__, url_prefix="/courses")


@courses.route("/")
@login_required
def course_list():
    return render_template("courses.html")
