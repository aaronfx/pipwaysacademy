from flask import Blueprint, render_template
from app.models.user_model import User
from app.models.blog_model import BlogPost
from app.models.course_model import Course
from app.models.webinar_model import Webinar

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def admin_dashboard():

    users = User.query.count()
    posts = BlogPost.query.count()
    courses = Course.query.count()
    webinars = Webinar.query.count()

    return render_template(
        "admin/dashboard.html",
        users=users,
        posts=posts,
        courses=courses,
        webinars=webinars
    )
