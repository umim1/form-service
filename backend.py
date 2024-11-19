from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("game_data.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/submit", methods=["POST"])
def submit_data():
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()

    required_fields = [
        "game_mode",
        "stage",
        "team_tank",
        "enemy_tank",
        "role",
        "character",
        "time_of_day",
        "result",
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

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

if __name__ == "__main__":
    app.run(debug=True)
