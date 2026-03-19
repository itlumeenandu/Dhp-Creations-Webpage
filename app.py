from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Connect DB
def get_db():
    conn = sqlite3.connect("database.db", timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

# Create table
def init_db():
    conn = get_db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        location TEXT,
        role TEXT,
        skills TEXT,
        email TEXT,
        phone TEXT,
        portfolio TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Submit API
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    try:
        conn = get_db()
        conn.execute("""
        INSERT INTO applications (name, age, location, role, skills, email, phone, portfolio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('name'),
            data.get('age'),
            data.get('location'),
            data.get('role'),
            data.get('skills'),
            data.get('email'),
            data.get('phone'),
            data.get('portfolio')
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Submitted successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get Data API
@app.route('/data', methods=['GET'])
def get_data():
    try:
        conn = get_db()
        cur = conn.execute("SELECT * FROM applications")
        rows = cur.fetchall()
        conn.close()

        result = []
        for r in rows:
            result.append({
                "name": r["name"],
                "age": r["age"],
                "location": r["location"],
                "role": r["role"],
                "skills": r["skills"]
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)