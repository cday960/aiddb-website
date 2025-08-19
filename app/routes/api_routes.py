from flask import Blueprint, jsonify


api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/version")
def version():
    return jsonify({"version": "1.0.0"})


@api_bp.route("/status")
def status():
    return jsonify({"status": "ok"})
