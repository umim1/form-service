import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 保存処理を行うエンドポイント
@app.route('/save_data', methods=['POST'])
def save_data():
    # フォームから送信されたデータを取得
    data = request.form.to_dict()
    
    # データを仮に出力（実際にはデータベース保存などの処理を記述）
    print("受信データ:", data)
    
    # レスポンスを返す
    return jsonify({"message": "データが保存されました！", "data": data})

if __name__ == '__main__':
    # 環境変数からポートを取得し、指定がなければデフォルトで5000番を使用
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

