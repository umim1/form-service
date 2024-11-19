from flask import Flask, request, jsonify

app = Flask(__name__)

# 仮の保存用リスト
data_storage = []

# ルートエンドポイント
@app.route("/")
def home():
    return "バックエンドは正常に動作しています！"

# データ保存用エンドポイント
@app.route("/save", methods=["POST"])
def save_data():
    try:
        # JSON形式でデータを受け取る
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # データをリストに保存
        data_storage.append(data)
        return jsonify({"message": "データを保存しました！", "data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# データ確認用エンドポイント
@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(data_storage), 200

# メイン関数
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # ここが重要！ポートとホストを設定
