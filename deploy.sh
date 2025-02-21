#!/bin/bash

# 確認環境變數
ENV=${1:-qa}
if [ "$ENV" != "qa" ] && [ "$ENV" != "prod" ]; then
  echo "Usage: deploy.sh [qa|prod]"
  exit 1
fi

# 使用對應的環境變數文件
ENV_FILE=".env.$ENV"

echo "部署環境: $ENV"
echo "使用環境配置文件: $ENV_FILE"

# 停止現有容器
docker-compose --env-file $ENV_FILE down

# 更新代碼
git pull origin main

# 只啟動應用程式（Render 已提供 DB）
docker-compose --env-file $ENV_FILE up --build -d app

# 等待應用啟動
echo "等待應用啟動..."
sleep 5  # 避免 Flyway 連線時找不到環境變數

# 執行 Flyway 遷移
echo "執行 Flyway 資料庫遷移..."
docker-compose --env-file $ENV_FILE up flyway

# 確保所有服務正常運行
docker-compose ps
