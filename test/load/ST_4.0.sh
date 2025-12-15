#!/bin/bash

# 活動列表 API 壓力測試腳本
# 測試 GET /api/activities

# 顏色定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 預設參數
HOST="${HOST:-localhost}"
PORT="${PORT:-8080}"
PROTOCOL="${PROTOCOL:-http}"
TOKEN="${TOKEN:-eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2NTgwMTE2NSwianRpIjoiZmYwY2Q5MzQtOTExNy00YjcxLWFmMmMtYmRmNjJiYWY0YzNhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjgiLCJuYmYiOjE3NjU4MDExNjUsImV4cCI6MTc2NTg4NzU2NX0.MMrSx3jGWrULXVO0FEl_YJCZCR0x1Y_2omd76brGhyo}"

# 測試參數
START_USERS="${START_USERS:-600}"           # 起始用戶數
INCREMENT="${INCREMENT:-100}"               # 每次增加用戶數
TEST_DURATION="${TEST_DURATION:-30}"        # 每輪測試持續時間（秒）
RAMPUP="${RAMPUP:-15}"                      # 啟動時間（秒）
MAX_ERROR_RATE="${MAX_ERROR_RATE:-5}"      # 最大錯誤率（%）
MAX_USERS="${MAX_USERS:-5000}"             # 最大用戶數限制
BREAKTIME="${BREAKTIME:-60}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  活動列表 API 壓力測試${NC}"
echo -e "${BLUE}  GET /api/activities${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}測試配置：${NC}"
echo "  主機: $PROTOCOL://$HOST:$PORT"
echo "  起始用戶數: $START_USERS"
echo "  每次增加: $INCREMENT 用戶"
echo "  最大用戶數: $MAX_USERS"
echo "  每輪持續: $TEST_DURATION 秒"
echo "  啟動時間: $RAMPUP 秒"
echo "  錯誤率門檻: $MAX_ERROR_RATE%"
echo ""

# 檢查 JMeter 是否安裝
if ! command -v jmeter &> /dev/null; then
    echo -e "${RED}錯誤：找不到 JMeter 指令${NC}"
    echo "請先安裝 JMeter:"
    echo "  macOS: brew install jmeter"
    exit 1
fi

# 建立結果目錄
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULT_DIR="results/activities-list-stress-$TIMESTAMP"
mkdir -p "$RESULT_DIR"

# 建立統計檔案
STATS_FILE="$RESULT_DIR/test-summary.txt"
echo "活動列表 API 壓力測試報告" > "$STATS_FILE"
echo "測試時間: $(date)" >> "$STATS_FILE"
echo "主機: $PROTOCOL://$HOST:$PORT" >> "$STATS_FILE"
echo "========================================" >> "$STATS_FILE"
echo "" >> "$STATS_FILE"

CURRENT_USERS=$START_USERS
ROUND=1

# 顯示表頭
echo -e "${CYAN}========================================================================================================${NC}"
printf "${CYAN}%-8s %-10s %-10s %-12s %-20s %-18s %-10s${NC}\n" "輪次" "用戶數" "請求數" "失敗率%" "平均回應時間ms" "吞吐量req/s" "狀態"
echo -e "${CYAN}========================================================================================================${NC}"

while [ $CURRENT_USERS -le $MAX_USERS ]; do
    ROUND_DIR="$RESULT_DIR/round-$ROUND-users-$CURRENT_USERS"
    mkdir -p "$ROUND_DIR"
    
    # 執行 JMeter 測試
    jmeter -n \
      -t ST_4.0.jmx \
      -Jhost="$HOST" \
      -Jport="$PORT" \
      -Jprotocol="$PROTOCOL" \
      -Jusers="$CURRENT_USERS" \
      -Jrampup="$RAMPUP" \
      -Jduration="$TEST_DURATION" \
      -Jtoken="$TOKEN" \
      -l "$ROUND_DIR/results.jtl" \
      > "$ROUND_DIR/ST_4.0.log" 2>&1
    
    # 檢查測試是否成功執行
    if [ ! -f "$ROUND_DIR/results.jtl" ]; then
        printf "${RED}%-8s %-10s %-10s %-12s %-20s %-18s %-10s${NC}\n" \
            "$ROUND" "$CURRENT_USERS" "-" "-" "-" "-" "測試失敗"
        break
    fi
    
    # 計算統計資料
    TOTAL=$(grep -c "^[0-9]" "$ROUND_DIR/results.jtl" 2>/dev/null || echo "0")
    
    if [ "$TOTAL" -eq 0 ]; then
        printf "${RED}%-8s %-10s %-10s %-12s %-20s %-18s %-10s${NC}\n" \
            "$ROUND" "$CURRENT_USERS" "0" "-" "-" "-" "無數據"
        break
    fi
    
    SUCCESS=$(grep ",200," "$ROUND_DIR/results.jtl" | wc -l | tr -d ' ')
    ERRORS=$((TOTAL - SUCCESS))
    ERROR_RATE=$(awk "BEGIN {printf \"%.2f\", ($ERRORS/$TOTAL)*100}" | tr -d '\n')
    
    # 計算平均回應時間
    AVG_TIME=$(awk -F',' 'NR>1 {sum+=$2; count++} END {if(count>0) printf "%.0f", sum/count; else print "0"}' "$ROUND_DIR/results.jtl")
    
    # 計算測試總時間和吞吐量
    START_TIME=$(awk -F',' 'NR==2 {print $1; exit}' "$ROUND_DIR/results.jtl")
    END_TIME=$(awk -F',' '$1 ~ /^[0-9]+$/ && $2 ~ /^[0-9]+$/ {timestamp=$1; elapsed=$2} END {print timestamp+elapsed}' "$ROUND_DIR/results.jtl")
    
    if [ -z "$START_TIME" ] || [ -z "$END_TIME" ] || [ "$START_TIME" = "0" ] || [ "$END_TIME" = "0" ]; then
        DURATION="0"
        THROUGHPUT="0.00"
    else
        DURATION=$(awk "BEGIN {printf \"%.2f\", ($END_TIME - $START_TIME)/1000}")
        if [ -n "$DURATION" ] && (( $(echo "$DURATION > 0" | bc -l) )); then
            THROUGHPUT=$(awk "BEGIN {printf \"%.2f\", $TOTAL/$DURATION}")
        else
            THROUGHPUT="0.00"
        fi
    fi
    
    # 判斷狀態
    STATUS="${GREEN}通過${NC}"
    if (( $(echo "$ERROR_RATE > $MAX_ERROR_RATE" | bc -l) )); then
        STATUS="${RED}失敗${NC}"
    fi
    
    # 顯示結果
    printf "%-8s %-10s %-10s %-12s %-20s %-18s " \
        "$ROUND" "$CURRENT_USERS" "$TOTAL" "$ERROR_RATE" "$AVG_TIME" "$THROUGHPUT"
    echo -e "$STATUS"
    
    # 記錄到統計檔案
    echo "第 $ROUND 輪 - $CURRENT_USERS 用戶:" >> "$STATS_FILE"
    echo "  總請求數: $TOTAL" >> "$STATS_FILE"
    echo "  成功: $SUCCESS" >> "$STATS_FILE"
    echo "  失敗: $ERRORS" >> "$STATS_FILE"
    echo "  錯誤率: $ERROR_RATE%" >> "$STATS_FILE"
    echo "  平均回應時間: ${AVG_TIME}ms" >> "$STATS_FILE"
    echo "  吞吐量: ${THROUGHPUT} req/s" >> "$STATS_FILE"
    echo "  測試時長: ${DURATION}s" >> "$STATS_FILE"
    echo "" >> "$STATS_FILE"
    
    # 檢查是否超過錯誤率門檻
    if (( $(echo "$ERROR_RATE > $MAX_ERROR_RATE" | bc -l) )); then
        echo ""
        echo -e "${RED}========================================${NC}"
        echo -e "${RED}錯誤率超過 ${MAX_ERROR_RATE}% (當前: ${ERROR_RATE}%)${NC}"
        echo -e "${RED}系統已達負載極限${NC}"
        echo -e "${RED}========================================${NC}"
        
        echo "" >> "$STATS_FILE"
        echo "系統已達負載極限！" >> "$STATS_FILE"
        echo "失敗原因: 錯誤率超過 ${MAX_ERROR_RATE}% (當前: ${ERROR_RATE}%)" >> "$STATS_FILE"
        echo "系統極限: $((CURRENT_USERS - INCREMENT)) 併發用戶 (錯誤率 < ${MAX_ERROR_RATE}%)" >> "$STATS_FILE"
        break
    fi
    
    # 增加用戶數，繼續下一輪
    CURRENT_USERS=$((CURRENT_USERS + INCREMENT))
    ROUND=$((ROUND + 1))
    
    # 等待系統恢復
    if [ $CURRENT_USERS -le $MAX_USERS ]; then
        echo -e "${BLUE}等待 ${BREAKTIME} 秒讓系統恢復...${NC}"
        sleep $BREAKTIME
    fi
done

echo -e "${CYAN}========================================================================================================${NC}"
echo ""

# 最終報告
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  測試完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}最終統計：${NC}"
echo "  測試輪數: $ROUND"
echo "  起始用戶數: $START_USERS"
echo "  最高測試用戶數: $CURRENT_USERS"
if [ $ROUND -gt 1 ]; then
    echo "  系統極限: $((CURRENT_USERS - INCREMENT)) 併發用戶 (錯誤率 < ${MAX_ERROR_RATE}%)"
else
    echo "  系統極限: 未達到"
fi
echo ""
echo -e "${YELLOW}報告位置：${NC}"
echo "  統計摘要: $STATS_FILE"
echo "  詳細結果: $RESULT_DIR/round-*/results.jtl"
echo ""

# 寫入最終統計
echo "" >> "$STATS_FILE"
echo "========================================" >> "$STATS_FILE"
echo "最終統計：" >> "$STATS_FILE"
echo "  測試輪數: $ROUND" >> "$STATS_FILE"
echo "  起始用戶數: $START_USERS" >> "$STATS_FILE"
echo "  最高測試用戶數: $CURRENT_USERS" >> "$STATS_FILE"
if [ $ROUND -gt 1 ]; then
    echo "  系統極限: $((CURRENT_USERS - INCREMENT)) 併發用戶 (錯誤率 < ${MAX_ERROR_RATE}%)" >> "$STATS_FILE"
else
    echo "  系統極限: 未達到" >> "$STATS_FILE"
fi
echo "========================================" >> "$STATS_FILE"
