from flask import Blueprint, render_template
from flask_login import login_required
from ..models.blog_model import Post

blog = Blueprint("blog", __name__)

@blog.route("/blog")
@login_required
def blog_page():

    posts = Post.query.all()

    return render_template("blog.html", posts=posts)
