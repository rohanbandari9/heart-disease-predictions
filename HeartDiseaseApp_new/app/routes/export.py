from flask import Blueprint, Response
from app.utils.database import get_db_connection
import csv
import io

export_bp = Blueprint("export", __name__)

@export_bp.route("/", methods=["GET"])
def export_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Date", "Age", "Cholesterol", "Prediction"])
    writer.writerows(rows)
    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=history.csv"},
    )
