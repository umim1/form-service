from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# データベースのパス
DATABASE = "game_data.db"

# ホームエンドポイント
@app.route('/')
def home():
    return "デプロイ成功！バックエンドは動作しています！"

# 勝率を計算するエンドポイント
@app.route('/winrate', methods=['GET'])
def calculate_winrate():
    try:
        # クエリパラメータを取得
        params = request.args
        rule = params.get('rule')
        map_name = params.get('map')
        enemy_tank = params.get('enemy_tank')
        ally_tank = params.get('ally_tank')
        role = params.get('role')
        character = params.get('character')
        time_of_day = params.get('time_of_day')

        # データベース接続
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # クエリと動的に組み換え
        query = "SELECT result FROM matches WHERE 1=1"
        values = []
        
        if rule:
            query += " AND rule = ?"
            values.append(rule)
        if map_name:
            query += " AND map = ?"
            values.append(map_name)
        if enemy_tank:
            query += " AND enemy_tank = ?"
            values.append(enemy_tank)
        if ally_tank:
            query += " AND ally_tank = ?"
            values.append(ally_tank)
        if role:
            query += " AND role = ?"
            values.append(role)
        if character:
            query += " AND character = ?"
            values.append(character)
        if time_of_day:
            query += " AND time_of_day = ?"
            values.append(time_of_day)

        # クエリ実行
        cursor.execute(query, values)
        results = cursor.fetchall()

        # 試合結果を計算
        total_matches = len(results)
        if total_matches == 0:
            return jsonify({"error": "No matches found"}), 404

        wins = sum(1 for result in results if result[0] == 'win')
        winrate = (wins / total_matches) * 100

        return jsonify({
            "winrate": round(winrate, 2),
            "total_matches": total_matches,
            "wins": wins
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()

# アプリ実行
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)





