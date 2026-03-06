from flask import Flask
from .extensions import db, login_manager


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "supersecret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    # IMPORT MODELS BEFORE create_all
    from .models.user_model import User
    from .models.course_model import Course, CourseEnrollment
    from .models.blog_model import Post

    # IMPORT ROUTES
    from .routes.auth_routes import auth
    from .routes.dashboard_routes import dashboard
    from .routes.blog_routes import blog
    from .routes.course_routes import courses

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(blog)
    app.register_blueprint(courses)

    with app.app_context():
        db.create_all()

    return app
