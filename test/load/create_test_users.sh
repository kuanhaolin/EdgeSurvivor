#!/bin/bash

# 批量建立測試用戶
# 用於登入壓力測試，避免 row-level lock 競爭

API_URL="http://localhost:5001/api/auth/register"
TOTAL_USERS=1200
PASSWORD="Test123456"

echo "開始建立 $TOTAL_USERS 個測試用戶..."
echo "API: $API_URL"
echo ""

SUCCESS=0
FAILED=0

for i in $(seq 1 $TOTAL_USERS); do
    EMAIL="loadtest${i}@test.com"
    NAME="LoadTest${i}"
    
    RESPONSE=$(curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"name\": \"$NAME\",
            \"email\": \"$EMAIL\",
            \"password\": \"$PASSWORD\",
            \"age\": 25,
            \"gender\": \"M\"
        }")
    
    if echo "$RESPONSE" | grep -q "註冊成功"; then
        ((SUCCESS++))
        if [ $((i % 50)) -eq 0 ]; then
            echo "已建立 $i 個用戶..."
        fi
    else
        ((FAILED++))
        if [ $FAILED -le 5 ]; then
            echo "失敗: $EMAIL - $RESPONSE"
        fi
    fi
    
    # 避免過快導致系統負載過高
    if [ $((i % 10)) -eq 0 ]; then
        sleep 0.5
    fi
done

echo ""
echo "=========================================="
echo "測試用戶建立完成"
echo "=========================================="
echo "成功: $SUCCESS"
echo "失敗: $FAILED"
echo ""
echo "現在可以執行登入壓測："
echo "  ./login_stress.sh"
echo ""
echo "清理測試用戶："
echo "  docker exec edgesurvivor_db mysql -uroot -proot edgesurvivor -e \"DELETE FROM users WHERE email LIKE 'loadtest%@test.com';\""
