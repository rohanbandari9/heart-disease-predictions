from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
import pickle

# Initialize Flask app
app = Flask(__name__)

#we import random_forest_model.pkl and knn_model.pkl
# Paths to the database and model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app/database/predictions.db")
RF_MODEL_PATH = os.path.join(BASE_DIR, "app/models/models/knn_model.pkl")

# Load the Random Forest model
with open(RF_MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        dob = request.form.get("dob")

        if not dob:
            return render_template("signup.html", error="Date of Birth is required.")

        # Generate a unique patient ID
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM patients")
        count = cursor.fetchone()[0]
        patient_id = f"P{str(count + 1).zfill(4)}"

        # Save patient ID and DOB
        cursor.execute("INSERT INTO patients (patient_id, dob) VALUES (?, ?)", (patient_id, dob))
        conn.commit()
        conn.close()

        return render_template("signup_success.html", patient_id=patient_id, dob=dob)

    return render_template("signup.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        dob = request.form.get("dob")

        if not patient_id or not dob:
            return render_template("login.html", error="Patient ID and Date of Birth are required.")

        # Verify patient ID and DOB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id = ? AND dob = ?", (patient_id, dob))
        patient = cursor.fetchone()
        conn.close()

        if not patient:
            return render_template("login.html", error="Invalid Patient ID or DOB.")

        # Redirect to Prediction and History options
        return render_template("dashboard.html", patient_id=patient_id, dob=dob)

    return render_template("login.html")

# Prediction route
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        patient_id = request.form.get("patient_id")
        dob = request.form.get("dob")

        if not patient_id or not dob:
            return render_template("predict.html", error="Patient ID and Date of Birth are required.")

        # Check if patient exists
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id = ? AND dob = ?", (patient_id, dob))
        patient = cursor.fetchone()

        if not patient:
            return render_template("predict.html", error="Invalid Patient ID or DOB.")

        try:
            # Collect prediction inputs
            age = float(request.form.get("age"))
            cholesterol = float(request.form.get("cholesterol"))
            blood_pressure = float(request.form.get("blood_pressure"))
            heart_rate = float(request.form.get("heart_rate"))
            exercise_angina = int(request.form.get("exercise_angina"))
        except (TypeError, ValueError):
            return render_template("predict.html", error="Invalid input values.")

        # Add default values for other features
        input_data = [[
            age, 1, 0, blood_pressure, cholesterol, 0, 1,
            heart_rate, exercise_angina, 0.0, 1, 0, 2
        ]]

        # Generate prediction
        prediction = model.predict(input_data)[0]
        result = "Heart Disease" if prediction == 1 else "No Heart Disease"

        # Save prediction in history
        cursor.execute(
            """INSERT INTO history (date, age, cholesterol, prediction, patient_id, dob)
               VALUES (datetime('now'), ?, ?, ?, ?, ?)""",
            (age, cholesterol, result, patient_id, dob),
        )
        conn.commit()
        conn.close()

        return render_template("result.html", result=result)

    return render_template("predict.html")

# History route
@app.route("/history/<patient_id>/<dob>")
def history(patient_id, dob):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date, age, cholesterol, prediction FROM history WHERE patient_id = ? AND dob = ?",
        (patient_id, dob),
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return render_template("history.html", error="No history found.")

    return render_template("history.html", history=rows)

if __name__ == "__main__":
    app.run(debug=True)


# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)