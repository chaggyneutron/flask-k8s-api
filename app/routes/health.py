from flask import Blueprint, jsonify
from app import db

health_bp = Blueprint("health", __name__)

@health_bp.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@health_bp.route("/ready")
def ready():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"status": "ready", "db": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "db": str(e)}), 503
