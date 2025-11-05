@echo off
echo ============================================
echo  EdgeSurvivor Docker 一鍵啟動
echo ============================================
echo.

echo [1/4] 啟動 Docker 服務...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ❌ Docker 啟動失敗！
    echo 請確認 Docker Desktop 是否正在運行
    pause
    exit /b 1
)

echo [2/4] 等待資料庫啟動（15秒）...
timeout /t 15 /nobreak >nul

echo [3/4] 初始化資料庫表格...
docker exec -it edgesurvivor_backend python init_docker_db.py
if %errorlevel% neq 0 (
    echo ⚠️  資料庫初始化失敗，可能是容器還未完全啟動
    echo 請稍後手動執行：
    echo docker exec -it edgesurvivor_backend python init_docker_db.py
)

echo.
echo [4/4] 檢查服務狀態...
docker-compose ps

echo.
echo ============================================
echo  ✅ 啟動完成！
echo ============================================
echo.
echo 📍 訪問應用：
echo   前端: http://localhost:8080
echo   後端: http://localhost:5001
echo   資料庫: localhost:3306
echo.
echo 📝 測試帳號：
echo   Email: ming@example.com  ^| 密碼: password123
echo   Email: hua@example.com   ^| 密碼: password123
echo   Email: jay@example.com   ^| 密碼: password123
echo.
echo 📖 常用命令：
echo   查看日誌: docker-compose logs -f
echo   停止服務: docker-compose down
echo   重啟服務: docker-compose restart
echo.
pause
