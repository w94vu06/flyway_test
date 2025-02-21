import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# 讀取 Render 提供的 PostgreSQL 連線資訊
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """ 建立資料庫連線 """
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"資料庫連線錯誤: {e}")
        return None

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/data')
def get_data():
    """ 查詢 example 資料表並回傳 JSON """
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "無法連接資料庫"}), 500

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM example;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = [{"id": row[0], "name": row[1], "email": row[2] if len(row) > 2 else None} for row in rows]
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
