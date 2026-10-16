import json
import sqlite3
from functools import wraps

from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)
DATABASE = 'users.db'
app.DATABASE = DATABASE

def get_db():
    conn = sqlite3.connect(app.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        db.commit()

# Initialize database on startup
init_db()

# Define the route for the home page
@app.route("/")
def home():
    return json.dumps({})

@app.route("/test")
def test_api():
    return json.dumps({"message": "success"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()
    
    if user:
        return jsonify({"message": "Login successful", "user_id": user["id"], "username": user["username"]}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    db = get_db()
    try:
        db.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, password)
        )
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409

# Run the app locally if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")