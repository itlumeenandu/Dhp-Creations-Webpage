import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)

# ✅ FIXED CORS (important)
CORS(app, resources={r"/*": {"origins": "*"}})

DATABASE_URL = os.environ.get("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def home():
    return "Backend Running Successfully 🚀"


# ✅ INSERT DATA (with duplicate protection)
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.json
        print("🔥 Received:", data)

        conn = connect_db()
        cur = conn.cursor()

        # 🚫 Prevent duplicate (same email + message)
        cur.execute("""
            SELECT * FROM talents
            WHERE email = %s AND message = %s
        """, (data.get("email"), data.get("message")))

        if cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"msg": "Already submitted"}), 200

        # ✅ Insert
        cur.execute("""
            INSERT INTO talents (name, email, talent, message)
            VALUES (%s, %s, %s, %s)
        """, (
            data.get("name"),
            data.get("email"),
            data.get("role"),
            data.get("message")
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"msg": "Saved successfully"}), 200

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"msg": "Server error"}), 500


# ✅ FETCH DATA
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
            "ID": r[0],
            "Name": r[1],
            "Email": r[2],
            "Role": r[3] if r[3] else "Not Provided",
            "Message": r[4]
        })

    return jsonify({
        "total_applications": len(result),
        "data": result
    })


if __name__ == "__main__":
    app.run(debug=True)