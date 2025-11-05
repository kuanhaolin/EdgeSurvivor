@echo off
echo ============================================
echo  Docker Desktop 重啟腳本
echo ============================================
echo.

echo [步驟 1] 正在關閉 Docker Desktop...
taskkill /F /IM "Docker Desktop.exe" 2>nul
timeout /t 3 >nul

echo [步驟 2] 正在停止 Docker 服務...
net stop com.docker.service 2>nul
timeout /t 2 >nul

echo [步驟 3] 清理 Docker 鎖定檔案...
del /F /Q "%APPDATA%\Docker\*.lock" 2>nul
del /F /Q "%LOCALAPPDATA%\Docker\*.lock" 2>nul

echo [步驟 4] 等待服務完全停止...
timeout /t 5 >nul

echo [步驟 5] 啟動 Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"

echo.
echo ============================================
echo  請等待 Docker Desktop 完全啟動（約 30 秒）
echo  圖標變綠後，再執行：
echo  docker-compose up -d --build
echo ============================================
pause
