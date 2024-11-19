import sqlite3

# データベース名
DATABASE = "game_data.db"

# データベースを作成
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# テーブル作成
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule TEXT,
    map_name TEXT,
    ally_tank TEXT,
    enemy_tank TEXT,
    role TEXT,
    character TEXT,
    time_period TEXT,
    result TEXT
)
""")

# 保存して閉じる
conn.commit()
conn.close()

print("データベースを作成しました！")
