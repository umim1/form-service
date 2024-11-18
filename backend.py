from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/analyze', methods=['GET'])
def analyze():
    # フロントエンドから送られてきた条件を取得
    enemy_tank = request.args.get('enemy_tank')  # 相手タンク
    rule = request.args.get('rule')             # ルール
    map_name = request.args.get('map')          # マップ名

    # データベース接続
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()

    # ベースとなるSQLクエリ
    query = "SELECT result FROM matches WHERE 1=1"
    params = []

    # 条件を動的に追加
    if enemy_tank:
        query += " AND enemy_tank = ?"
        params.append(enemy_tank)
    if rule:
        query += " AND rule = ?"
        params.append(rule)
    if map_name:
        query += " AND map = ?"
        params.append(map_name)

    # クエリを実行
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    # データがない場合
    if not results:
        return jsonify({"message": "まだデータがありません"}), 200

    # 勝率計算
    total_games = len(results)
    wins = sum(1 for result in results if result[0] == '勝ち')
    winrate = (wins / total_games) * 100

    return jsonify({
        "conditions": {
            "enemy_tank": enemy_tank or "指定なし",
            "rule": rule or "指定なし",
            "map": map_name or "指定なし"
        },
        "winrate": f"{winrate:.2f}%",
        "wins": wins,
        "total_games": total_games
    })

if __name__ == '__main__':
    app.run(debug=True)





