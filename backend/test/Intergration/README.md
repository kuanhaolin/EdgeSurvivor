# EdgeSurvivor 整合測試執行指南

## 📋 測試檔案結構

```
backend/test/Intergration/
├── __init__.py
├── conftest.py                    # 測試 fixtures
├── test_auth_flow.py              # 身份認證測試
├── test_activity_flow.py          # 活動管理測試
├── test_match_flow.py             # 配對系統測試
└── test_e2e_scenarios.py          # 端到端測試
```

## 🚀 快速開始

### 1. 安裝測試依賴

```bash
cd backend
pip install -r requirements-test.txt
```

### 2. 執行測試

#### 執行單一測試
```bash
# 執行特定測試
python -m pytest test/Intergration/test_auth_flow.py::TestAuthenticationFlow::test_login_with_invalid_credentials -v

# 執行整個測試類別
python -m pytest test/Intergration/test_auth_flow.py::TestAuthenticationFlow -v

# 執行整個測試檔案
python -m pytest test/Intergration/test_auth_flow.py -v
```

#### 執行所有整合測試
```bash
python -m pytest test/Intergration/ -v
```

## 📊 產生測試報告

### 方法 1: 使用 pytest 直接產生報告

```bash
# 產生 HTML 報告
python -m pytest test/Intergration/ -v \
    --html=test/reports/integration_report.html \
    --self-contained-html

# 產生 HTML 報告 + 覆蓋率報告
python -m pytest test/Intergration/ -v \
    --html=test/reports/integration_report.html \
    --self-contained-html \
    --cov=. \
    --cov-report=html:test/reports/coverage

# 產生 XML 報告 (用於 CI/CD)
python -m pytest test/Intergration/ -v \
    --junitxml=test/reports/junit.xml
```

### 方法 2: 使用測試報告腳本

```bash
# 執行所有模組並分別產生報告
python run_integration_tests.py

# 執行特定模組
python run_integration_tests.py test/Intergration/test_auth_flow.py auth_flow

# 執行特定模組並指定報告名稱
python run_integration_tests.py test/Intergration/test_activity_flow.py activity_test
```

## 📁 報告位置

執行測試後,報告會儲存在:

- **HTML 測試報告**: `test/reports/integration_report.html`
- **覆蓋率報告**: `test/reports/coverage/index.html`
- **JUnit XML**: `test/reports/junit.xml`
- **測試日誌**: `test/reports/test.log`

## 🎯 測試模組說明

### 1. test_auth_flow.py - 身份認證測試
- ✅ 完整註冊與登入流程
- ✅ 錯誤憑證登入
- ✅ 重複 email 註冊
- ✅ Token 刷新流程
- ✅ 個人資料更新
- ✅ 社群帳號連結
- ✅ 社群隱私設定
- ✅ 帳號刪除

### 2. test_activity_flow.py - 活動管理測試
- ✅ 建立活動
- ✅ 更新活動
- ✅ 刪除活動
- ✅ 權限控制
- ✅ 參與流程(申請、審核、拒絕)
- ✅ 移除參與者
- ✅ 人數上限控制
- ✅ 討論區管理
- ✅ 費用管理與分攤

### 3. test_match_flow.py - 配對系統測試
- ✅ 完整好友申請流程
- ✅ 拒絕好友請求
- ✅ 刪除好友
- ✅ 用戶篩選與搜尋
- ✅ 好友間聊天
- ✅ 聊天記錄查詢
- ✅ 非好友訊息限制
- ✅ 推薦系統

### 4. test_e2e_scenarios.py - 端到端測試
- ✅ 完整活動生命週期
- ✅ 好友與活動互動流程

## 🔧 常用測試選項

```bash
# 顯示詳細輸出
-v, --verbose

# 顯示測試中的 print 輸出
-s

# 只執行失敗的測試
--lf, --last-failed

# 執行到第一個失敗就停止
-x, --exitfirst

# 顯示最慢的 N 個測試
--durations=N

# 並行執行測試 (需要 pytest-xdist)
-n auto

# 執行特定標記的測試
-m auth          # 只執行 auth 標記的測試
-m "not slow"    # 排除 slow 標記的測試
```

## 📈 測試覆蓋率目標

- **整體覆蓋率**: ≥ 80%
- **關鍵模組覆蓋率**: ≥ 90%
  - blueprints/auth.py
  - blueprints/activities.py
  - blueprints/matches.py
  - blueprints/chat.py

## 🐛 常見問題

### 1. ModuleNotFoundError
```bash
# 確保已安裝所有依賴
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 2. 資料庫連線錯誤
測試使用 SQLite 記憶體資料庫,不需要 MySQL 連線。

### 3. Fixture 錯誤
確保 `test/conftest.py` 和 `test/Intergration/conftest.py` 都存在且正確。

## 💡 最佳實踐

1. **執行測試前**:確保所有依賴已安裝
2. **測試隔離**:每個測試應該獨立,不依賴其他測試
3. **清理資料**:使用 fixtures 的 yield 來清理測試資料
4. **有意義的斷言**:使用清楚的斷言訊息
5. **定期執行**:在每次 commit 前執行測試

## 🔄 CI/CD 整合

在 GitHub Actions 中使用:

```yaml
- name: Run Integration Tests
  run: |
    cd backend
    pytest test/Intergration/ -v \
      --html=test/reports/integration_report.html \
      --self-contained-html \
      --junitxml=test/reports/junit.xml \
      --cov=. \
      --cov-report=xml
```

## 📞 需要幫助?

如果遇到問題:
1. 查看測試日誌: `test/reports/test.log`
2. 查看 HTML 報告中的詳細錯誤訊息
3. 使用 `-v -s` 選項查看詳細輸出
