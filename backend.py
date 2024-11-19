import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DATABASE = "game_data.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return "Welcome to the Match Data API!"

@app.route("/submit", methods=["POST"])
def submit_data():
    data = request.json
    required_fields = [
        "game_mode",
        "stage",
        "team_tank",
        "enemy_tank",
        "role",
        "character",
        "time_of_day",
        "result"
    ]

    # 必須フィールドが揃っているかチェック
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # データベースに保存
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO matches (game_mode, stage, team_tank, enemy_tank, role, character, time_of_day, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["game_mode"],
            data["stage"],
            data["team_tank"],
            data["enemy_tank"],
            data["role"],
            data["character"],
            data["time_of_day"],
            data["result"],
        ),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Match data saved successfully!"}), 200

@app.route("/data", methods=["GET"])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matches")
    rows = cursor.fetchall()
    conn.close()

    # データをJSON形式で返す
    results = [dict(row) for row in rows]
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
