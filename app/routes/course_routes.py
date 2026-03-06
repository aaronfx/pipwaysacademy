from flask import Blueprint, render_template
from flask_login import login_required
from ..models.course_model import Course

course = Blueprint("course", __name__)

@course.route("/courses")
@login_required
def courses():

    courses = Course.query.all()

    return render_template("courses.html", courses=courses)
