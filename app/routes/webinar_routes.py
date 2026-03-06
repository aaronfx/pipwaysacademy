from flask import Blueprint, render_template
from app.models.webinar_model import Webinar

webinars = Blueprint("webinars", __name__)

@webinars.route("/webinars")
def webinar_list():

    all_webinars = Webinar.query.all()

    return render_template("webinars.html", webinars=all_webinars)
