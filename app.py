from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db():
    return sqlite3.connect("database.db")

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    conn = get_db()

    conn.execute("INSERT INTO applications VALUES (NULL,?,?,?,?,?,?,?,?)",
    (data['name'], data['age'], data['location'], data['role'],
     data['skills'], data['email'], data['phone'], data['portfolio']))

    conn.commit()
    conn.close()
    return jsonify({"msg": "ok"})

@app.route('/data')
def data():
    conn = get_db()
    cur = conn.execute("SELECT * FROM applications")
    rows = cur.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "name": r[1],
            "age": r[2],
            "location": r[3],
            "role": r[4],
            "skills": r[5]
        })

    return jsonify(result)

app.run(debug=True)