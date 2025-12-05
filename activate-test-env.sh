#!/bin/bash
# EdgeSurvivor 測試環境啟動腳本

# 顏色定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  EdgeSurvivor 測試環境${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 啟動虛擬環境
echo -e "${GREEN}✓${NC} 啟動虛擬環境..."
source test-env/bin/activate

# 顯示環境信息
echo -e "${GREEN}✓${NC} Python: $(python --version)"
echo -e "${GREEN}✓${NC} pytest: $(pytest --version)"
echo ""

echo -e "${YELLOW}可用的測試命令:${NC}"
echo "  pytest -v                          # 執行所有測試"
echo "  pytest test/unit/test_auth.py -v   # 只執行認證測試"
echo "  pytest test/unit/test_users.py -v  # 只執行使用者測試"
echo "  pytest test/unit/test_activities.py -v # 只執行活動測試"
echo "  pytest -m auth                      # 只執行標記為 auth 的測試"
echo "  pytest --cov=backend                # 查看測試覆蓋率"
echo "  pytest --cov=backend --cov-report=html # 生成 HTML 覆蓋率報告"
echo ""

# 保持在虛擬環境中
exec $SHELL
