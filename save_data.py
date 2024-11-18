import sqlite3

# データを保存
def save_data(rule, map_name, ally_tank, enemy_tank, role, character, time_period, result):
    conn = sqlite3.connect('game_data.db')  # データベース名
    cursor = conn.cursor()

    # データを挿入
    cursor.execute('''
        INSERT INTO matches (rule, map, ally_tank, enemy_tank, role, character, time_period, result)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (rule, map_name, ally_tank, enemy_tank, role, character, time_period, result))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # テスト用データ
    save_data(
        rule='コントロール',
        map_name='ANTARCTIC PENINSULA',
        ally_tank='D.VA',
        enemy_tank='ラインハルト',
        role='タンク',
        character='D.VA',
        time_period='朝',
        result='勝ち'
    )
    print("データを保存しました！")
