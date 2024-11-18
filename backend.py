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

        # データベース接続
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # クエリを動的に構築
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

        # クエリを実行して結果を取得
        cursor.execute(query, values)
        results = cursor.fetchall()

        # 勝率を計算
        if results:
            total_matches = len(results)
            wins = sum(1 for result in results if result[0] == "win")
            winrate = (wins / total_matches) * 100
            return jsonify({"winrate": f"{winrate:.2f}%", "total_matches": total_matches})
        else:
            return jsonify({"message": "該当するデータがありません"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
