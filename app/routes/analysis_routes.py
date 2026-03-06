from flask import Blueprint, request, render_template
from app.models.trade_analysis_model import TradeAnalysis
from app.extensions import db

analysis = Blueprint("analysis", __name__)

@analysis.route("/analysis/upload", methods=["POST"])
def upload_trade():

    file = request.files.get("file")

    if not file:
        return "No file uploaded"

    result = TradeAnalysis(filename=file.filename)

    db.session.add(result)
    db.session.commit()

    return render_template("analysis_result.html", result=result)
