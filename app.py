from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# DATABASE_URL comes from Render environment variable for production
# Fallback is your full Postgres URL
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://dhp_creations_webpage_user:zpvA6GOp6ZZwq8z9jP7H124NhxpFfYnz@dpg-d6te41f5r7bs73abruv0-a.oregon-postgres.render.com/dhp_creations_webpage"
)

def get_db():
    return psycopg2.connect(DATABASE_URL)

# Root route with simple HTML linking to /data
@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Flask App on Render</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
                a.button { 
                    display: inline-block; padding: 10px 20px; background-color: #4CAF50; 
                    color: white; text-decoration: none; border-radius: 5px; font-weight: bold; 
                }
                a.button:hover { background-color: #45a049; }
            </style>
        </head>
        <body>
            <h1>Welcome! Your Flask app is running on Render.</h1>
            <p>Click below to see submitted data:</p>
            <a class="button" href="/data">View Data</a>
        </body>
    </html>
    """

# Submit endpoint
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

# Data endpoint
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
    # Use Render's port if available, fallback to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)