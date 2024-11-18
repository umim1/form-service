import sqlite3

# データベースを作成
def create_database():
    conn = sqlite3.connect('game_data.db')  # データベース名
    cursor = conn.cursor()

    # テーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule TEXT,
            map TEXT,
            ally_tank TEXT,
            enemy_tank TEXT,
            role TEXT,
            character TEXT,
            time_period TEXT,
            result TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("データベースを作成しました！")
