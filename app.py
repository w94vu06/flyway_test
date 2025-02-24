import os
import psycopg2
import subprocess
from flask import Flask, jsonify

app = Flask(__name__)

# 讀取環境變數
DATABASE_URL = os.getenv("DATABASE_URL")
FLYWAY_PATH = "/flyway/flyway"

# 顯示連線的資料庫 URL
print(f"🔥 目前連接的資料庫: {DATABASE_URL}")

# Flyway 需要 `jdbc:postgresql://` 而不是 `postgresql://`
FLYWAY_DATABASE_URL = DATABASE_URL.replace("postgresql://", "jdbc:postgresql://")

def run_flyway():
    """ 在 Flask 啟動前執行 Flyway 遷移 """
    try:
        print("🚀 執行 Flyway 資料庫遷移...")
        subprocess.run(
            [FLYWAY_PATH, "-url=" + FLYWAY_DATABASE_URL, "-user=" + os.getenv("POSTGRES_USER"), "-password=" + os.getenv("POSTGRES_PASSWORD"), "migrate"],
            check=True
        )
        print("✅ Flyway 遷移成功！")
    except Exception as e:
        print(f"❌ Flyway 遷移失敗: {e}")

# 先執行 Flyway 遷移
run_flyway()

@app.route('/')
def home():
    return f"Hello, World! Connected to: {DATABASE_URL}"

@app.route('/data')
def get_data():
    """ 查詢 example 資料表並回傳 JSON """
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM example;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{"id": row[0], "name": row[1], "email": row[2]} for row in rows])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
