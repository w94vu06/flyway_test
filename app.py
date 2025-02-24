import os
import psycopg2
import subprocess
import urllib.parse
from flask import Flask, jsonify

app = Flask(__name__)

# 讀取環境變數
DATABASE_URL = os.getenv("DATABASE_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
FLYWAY_PATH = "/flyway/flyway"

# 確保 `DATABASE_URL` 存在
if not DATABASE_URL:
    raise ValueError("❌ `DATABASE_URL` 未設定，請確保 Render 設定正確！")

# 修正 `DATABASE_URL`，處理特殊字符
def format_flyway_url(database_url):
    parsed_url = urllib.parse.urlparse(database_url)
    clean_url = f"jdbc:postgresql://{parsed_url.hostname}:{parsed_url.port}{parsed_url.path}"
    return clean_url

FLYWAY_DATABASE_URL = format_flyway_url(DATABASE_URL)

def run_flyway():
    """ 在 Flask 啟動前執行 Flyway 遷移 """
    try:
        print(f"🚀 使用 Flyway 連接: {FLYWAY_DATABASE_URL}")
        subprocess.run(
            [FLYWAY_PATH, "-url=" + FLYWAY_DATABASE_URL, "-user=" + POSTGRES_USER, "-password=" + POSTGRES_PASSWORD, "migrate"],
            check=True
        )
        print("✅ Flyway 資料庫遷移成功！")
    except Exception as e:
        print(f"❌ Flyway 資料庫遷移失敗: {e}")

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
