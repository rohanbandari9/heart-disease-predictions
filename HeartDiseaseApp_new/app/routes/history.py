from flask import Blueprint, jsonify
from app.utils.database import get_db_connection

history_bp = Blueprint("history", __name__)

@history_bp.route("/", methods=["GET"])
def get_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)
