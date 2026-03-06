from flask import Blueprint, render_template
from app.models.blog_model import BlogPost

blog = Blueprint("blog", __name__)

@blog.route("/blog")
def blog_list():

    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()

    return render_template("blog.html", posts=posts)


@blog.route("/blog/<slug>")
def blog_post(slug):

    post = BlogPost.query.filter_by(slug=slug).first_or_404()

    return render_template("blog_post.html", post=post)
