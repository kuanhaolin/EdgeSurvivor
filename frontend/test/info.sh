#!/bin/bash

echo "測試"
echo "========================================="
echo ""

cd frontend

# 檢查是否安裝依賴
if [ ! -d "node_modules/vitest" ]; then
  echo "⚠️  未安裝 vitest，正在安裝測試依賴..."
  npm install --save-dev vitest @vue/test-utils jsdom @vitest/ui
  echo ""
fi