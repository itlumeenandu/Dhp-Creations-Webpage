from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set!")

def get_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    email = data.get("email")
    MY_EMAIL = "dhpcreations15@gmail.com"

    conn = get_db()
    cur = conn.cursor()

    if email != MY_EMAIL:
        cur.execute("SELECT * FROM applications WHERE email = %s", (email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": "You have already submitted an application!"}), 400

    cur.execute("""
        INSERT INTO applications
        (name, age, location, role, skills, email, phone, portfolio)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data.get("name"), data.get("age"), data.get("location"), data.get("role"),
        data.get("skills"), data.get("email"), data.get("phone"), data.get("portfolio")
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Application submitted successfully!"})

@app.route("/data")
def data():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, age, location, role, skills, email, phone, portfolio FROM applications")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("data.html", rows=rows)

@app.route("/clear", methods=["POST"])
def clear_entries():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM applications")
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "All entries cleared!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)