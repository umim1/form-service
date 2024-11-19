from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# データベース名
DATABASE = "game_data.db"

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.json  # フロントエンドからのJSONデータを受け取る

    # 必要なデータを取得
    rule = data.get("rule")
    map_name = data.get("map_name")
    ally_tank = data.get("ally_tank")
    enemy_tank = data.get("enemy_tank")
    role = data.get("role")
    character = data.get("character")
    time_period = data.get("time_period")
    result = data.get("result")

    # データベースに保存
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO matches (rule, map_name, ally_tank, enemy_tank, role, character, time_period, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (rule, map_name, ally_tank, enemy_tank, role, character, time_period, result))
        conn.commit()
        conn.close()
        return jsonify({"message": "データを保存しました！"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
