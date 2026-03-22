import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DATABASE_URL = os.environ.get("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL, sslmode='require')


@app.route("/")
def home():
    return "Backend Running 🚀"


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    conn = connect_db()
    cur = conn.cursor()

    # prevent duplicates
    cur.execute("""
        SELECT * FROM talents 
        WHERE email=%s AND message=%s
    """, (data["email"], data["message"]))

    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"msg": "Already exists"})

    cur.execute("""
        INSERT INTO talents (name, email, talent, message)
        VALUES (%s, %s, %s, %s)
    """, (
        data["name"],
        data["email"],
        data["role"],
        data["message"]
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"msg": "Saved"})


@app.route("/data")
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
            "role": r[3],
            "message": r[4]
        })

    return jsonify(result)


# ❗ THIS IS CRITICAL
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)