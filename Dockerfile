# 使用 Python 作為基底映像檔
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製依賴文件和應用代碼
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

# 暴露 Flask 預設的埠
EXPOSE 5000

# 啟動 Flask 應用程式
CMD ["python", "app.py"]