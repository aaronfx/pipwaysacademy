from flask import Flask
from .extensions import db, login_manager, bcrypt
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .routes.auth_routes import auth
    from .routes.dashboard_routes import dashboard
    from .routes.blog_routes import blog
    from .routes.course_routes import courses
    from .routes.webinar_routes import webinars
    from .routes.analysis_routes import analysis
    from .routes.admin_routes import admin

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(blog)
    app.register_blueprint(courses)
    app.register_blueprint(webinars)
    app.register_blueprint(analysis)
    app.register_blueprint(admin)

    return app
