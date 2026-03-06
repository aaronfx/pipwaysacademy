from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.course_model import Course, CourseEnrollment

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
@login_required
def dashboard_home():

    courses = Course.query.all()

    enrollments = CourseEnrollment.query.filter_by(user_id=current_user.id).all()

    return render_template(
        "dashboard.html",
        courses=courses,
        enrollments=enrollments
    )
