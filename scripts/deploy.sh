#!/bin/bash
# Athena 部署脚本
echo "🚀 开始部署 Athena..."
docker-compose -f docker/docker-compose.yml pull
docker-compose -f docker/docker-compose.yml up -d --build
echo "✅ 部署完成"