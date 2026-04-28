print("起動しました")

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()

    # テーブル作成
    c.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            leaf TEXT,
            flower TEXT
        )
    ''')

    # データ削除（重複防止）
    c.execute("DELETE FROM plants")

    # データ追加
    c.execute("INSERT INTO plants (name, leaf, flower) VALUES ('タンポポ', '丸い', 'あり')")
    c.execute("INSERT INTO plants (name, leaf, flower) VALUES ('ススキ', '細い', 'なし')")
    c.execute("INSERT INTO plants (name, leaf, flower) VALUES ('バラ', '丸い', 'あり')")

    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    if request.method == 'POST':
        leaf = request.form.get('leaf')
        flower = request.form.get('flower')

        conn = sqlite3.connect('plants.db')
        c = conn.cursor()
        c.execute("SELECT name FROM plants WHERE leaf=? AND flower=?", (leaf, flower))
        result = c.fetchall()
        conn.close()

    return render_template('index.html', result=result)

import os

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)