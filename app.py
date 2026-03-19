from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Make sure to set this environment variable on Render
DATABASE_URL = os.environ.get("DATABASE_URL", "PASTE_YOUR_LOCAL_DB_URL_HERE")

def get_db():
    return psycopg2.connect(DATABASE_URL)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO applications 
        (name, age, location, role, skills, email, phone, portfolio)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data.get('name'), data.get('age'), data.get('location'), data.get('role'),
        data.get('skills'), data.get('email'), data.get('phone'), data.get('portfolio')
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Saved"})

@app.route('/data')
def data():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT name, age, location, role, skills FROM applications")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "name": r[0],
            "age": r[1],
            "location": r[2],
            "role": r[3],
            "skills": r[4]
        })

    return jsonify(result)

if __name__ == "__main__":
    # Use Render's port or default 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)