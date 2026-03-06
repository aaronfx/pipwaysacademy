from flask import Blueprint, render_template
from app.models.course_model import Course

courses = Blueprint("courses", __name__)

@courses.route("/courses")
def course_list():

    all_courses = Course.query.all()

    return render_template("courses.html", courses=all_courses)
