from flask import Flask, render_template, request, redirect
import psycopg2
import os
from urllib.parse import urlparse

app = Flask(__name__)

# Get DATABASE_URL from Render environment
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable not set!")

# Parse DATABASE_URL
result = urlparse(database_url)
username = result.username
password = result.password
database = result.path[1:]  # remove leading '/'
hostname = result.hostname
port = result.port

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=database,
    user=username,
    password=password,
    host=hostname,
    port=port
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    device_id VARCHAR(255) NOT NULL,
    UNIQUE(username, device_id)
)
""")
conn.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        message = request.form.get("message")
        device_id = request.form.get("device_id")

        try:
            cursor.execute("""
            INSERT INTO entries (username, message, device_id)
            VALUES (%s, %s, %s)
            """, (username, message, device_id))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()  # entry already exists
            pass

        return redirect("/")

    cursor.execute("SELECT username, message FROM entries ORDER BY id DESC")
    all_entries = cursor.fetchall()
    return render_template("index.html", entries=all_entries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
