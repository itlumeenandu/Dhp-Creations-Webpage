import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

# HOME
@app.route("/")
def home():
    return "Backend Running Successfully on Render 🚀"


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
        data.get("role"),
        data.get("message")
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"msg": "Saved!"})


# FETCH DATA (FORMATTED JSON)
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


# VIEW DATA (TABLE FORMAT)
@app.route("/view", methods=["GET"])
def view_data():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM talents ORDER BY id DESC")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    html = """
    <html>
    <head>
        <title>Submitted Applications</title>
        <style>
            body {
                background: linear-gradient(135deg, #0f0f0f, #1c1c1c);
                color: #fff;
                font-family: Arial, sans-serif;
                text-align: center;
            }
            h1 {
                margin-top: 30px;
                color: #00ffcc;
                letter-spacing: 2px;
            }
            table {
                margin: 40px auto;
                border-collapse: collapse;
                width: 90%;
                background: #1a1a1a;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 0 25px rgba(0,255,204,0.2);
            }
            th, td {
                padding: 14px;
                border-bottom: 1px solid #333;
            }
            th {
                background: #222;
                color: #00ffcc;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            tr:hover {
                background: #2a2a2a;
                transition: 0.3s;
            }
        </style>
    </head>
    <body>
        <h1>🎬 Submitted Applications</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Message</th>
            </tr>
    """

    for r in rows:
        html += f"""
            <tr>
                <td>{r[0]}</td>
                <td>{r[1]}</td>
                <td>{r[2]}</td>
                <td>{r[3] if r[3] else 'Not Provided'}</td>
                <td>{r[4]}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(debug=True)