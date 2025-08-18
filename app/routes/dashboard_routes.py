from flask import Blueprint
from app.lib.decorators import requires_login


dash_bp = Blueprint("dash", __name__)
