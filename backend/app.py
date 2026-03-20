import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return "Backend Running 🚀"

# INSERT DATA
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO talents (name, email, talent, message)
        VALUES (%s, %s, %s, %s)
    """, (
        data.get("name"),
        data.get("email"),
        data.get("role"),   # keep role from frontend
        data.get("message")
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"msg": "Saved!"})

# FETCH DATA
@app.route("/data", methods=["GET"])
def get_data():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM talents ORDER BY id DESC")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "role": r[3],   # still send as role (frontend expects this)
            "message": r[4]
        })

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)