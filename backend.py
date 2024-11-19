from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# データベースの初期化
def init_db():
    connection = sqlite3.connect('game_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_mode TEXT,
            stage TEXT,
            team_tank TEXT,
            enemy_tank TEXT,
            role TEXT,
            character TEXT,
            time_of_day TEXT,
            result TEXT
        )
    ''')
    connection.commit()
    connection.close()

@app.route('/save', methods=['POST'])
def save_data():
    data = request.form
    game_mode = data.get('game_mode')
    stage = data.get('stage')
    team_tank = data.get('team_tank')
    enemy_tank = data.get('enemy_tank')
    role = data.get('role')
    character = data.get('character')
    time_of_day = data.get('time_of_day')
    result = data.get('result')

    if not all([game_mode, stage, team_tank, enemy_tank, role, character, time_of_day, result]):
        return jsonify({'error': 'Missing data'}), 400

    connection = sqlite3.connect('game_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO game_data (game_mode, stage, team_tank, enemy_tank, role, character, time_of_day, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (game_mode, stage, team_tank, enemy_tank, role, character, time_of_day, result))
    connection.commit()
    connection.close()

    return jsonify({'message': 'Data saved successfully'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

