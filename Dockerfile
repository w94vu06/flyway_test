# 使用 Python 3.9 Slim 版本
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 安裝必要的工具 (`curl`, `unzip`)
RUN apt-get update && apt-get install -y curl unzip

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有應用程式代碼
COPY . /app

# 下載並安裝 Flyway
RUN curl -L "https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/9.22.3/flyway-commandline-9.22.3-linux-x64.tar.gz" -o flyway.tar.gz && \
    tar -xzf flyway.tar.gz && \
    mv flyway-9.22.3 /flyway

# 執行 Flyway 遷移
RUN /flyway/flyway -url=$DATABASE_URL -user=$POSTGRES_USER -password=$POSTGRES_PASSWORD -locations=filesystem:/app/sql/migrations migrate

# 啟動 Flask 應用
CMD ["python", "app.py"]
