from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# データベース名
DATABASE = "game_data.db"

@app.route('/winrate', methods=['GET'])
def calculate_winrate():
    params = request.args
    rule = params.get("rule")
    map_name = params.get("map_name")
    ally_tank = params.get("ally_tank")
    enemy_tank = params.get("enemy_tank")

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # クエリ作成
        query = "SELECT result FROM matches WHERE 1=1"
        values = []
        if rule:
            query += " AND rule = ?"
            values.append(rule)
        if map_name:
            query += " AND map_name = ?"
            values.append(map_name)
        if ally_tank:
            query += " AND ally_tank = ?"
            values.append(ally_tank)
        if enemy_tank:
            query += " AND enemy_tank = ?"
            values.append(enemy_tank)

        cursor.execute(query, values)
        results = cursor.fetchall()
        conn.close()

        # 勝率計算
        if not results:
            return jsonify({"winrate": None, "message": "該当データがありませんでした。"})
        total_games = len(results)
        wins = sum(1 for result in results if result[0] == "win")
        winrate = (wins / total_games) * 100

        return jsonify({"winrate": winrate, "total_games": total_games}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
