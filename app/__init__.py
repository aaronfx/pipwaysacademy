from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "supersecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import models
    from .models.user_model import User
    from .models.blog_model import Post
    from .models.course_model import Course

    # Import routes
    from .routes.auth_routes import auth
    from .routes.dashboard_routes import dashboard
    from .routes.blog_routes import blog
    from .routes.course_routes import courses
    from .routes.webinar_routes import webinars

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(blog)
    app.register_blueprint(courses)
    app.register_blueprint(webinars)

    with app.app_context():
        db.create_all()

    return app
