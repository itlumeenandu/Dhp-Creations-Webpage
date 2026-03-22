from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)

# ✅ FIX CORS COMPLETELY
CORS(app, resources={r"/*": {"origins": "*"}})

# ✅ DATABASE CONNECTION
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL)

# ✅ HOME ROUTE (IMPORTANT for Render)
@app.route("/")
def home():
    return "Backend Running Successfully 🚀"

# ✅ SUBMIT ROUTE
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        role = data.get("role")
        message = data.get("message")

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (name, email, role, message) VALUES (%s, %s, %s, %s)",
            (name, email, role, message)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"msg": "Data inserted successfully"})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"msg": "Error inserting data"}), 500

# ✅ DATA ROUTE
@app.route("/data", methods=["GET"])
def data():
    try:
        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        result = []
        for row in rows:
            result.append({
                "Name": row[1],
                "Email": row[2],
                "Role": row[3],
                "Message": row[4]
            })

        cur.close()
        conn.close()

        return jsonify({"data": result})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"data": []})

# ✅ IMPORTANT FOR RENDER PORT
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)