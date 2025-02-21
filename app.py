from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# 從環境變數讀取 PostgreSQL 連線資訊
DB_HOST = "db"  # 在 Docker Compose 裡，服務名稱就是 Host
DB_NAME = os.getenv("POSTGRES_DB", "testdb")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "root")
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """ 建立資料庫連線 """
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/data')
def get_data():
    """ 查詢 example 資料表並回傳 JSON """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM example;")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        # 轉換成 JSON 格式輸出
        data = [{"id": row[0], "name": row[1]} for row in rows]
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
