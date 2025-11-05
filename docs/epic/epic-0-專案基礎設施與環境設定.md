# Epic 0: 專案基礎設施與環境設定

**Epic 目標：** 建立完整的開發環境、測試基礎設施和部署管道，為所有後續功能開發提供穩固的技術基礎。

**優先級：** P0 (最高優先級 - 必須在任何功能開發前完成)

**前置條件：** 無

**Epic 價值：**
- 確保所有開發者能快速搭建一致的開發環境
- 建立自動化測試能力，保證代碼品質
- 設定 CI/CD 管道，實現快速部署
- 降低新成員加入的學習曲線

---

## Story 0.1: 本地開發環境設定與驗證

**User Story:**
作為一個新加入的開發者，我希望能按照明確的步驟快速設定本地開發環境，以便開始進行開發工作。

**Acceptance Criteria:**

**功能需求：**
1. 能夠按照文件安裝所有必要工具（Python 3.10+, Node.js 18+, MariaDB/MySQL）
2. 能夠複製 `.env.example` 並正確配置環境變數
3. 能夠成功連接到本地 MariaDB/MySQL 資料庫
4. 能夠驗證所有工具版本符合要求

**技術需求：**
5. 提供自動化驗證腳本檢查環境配置
6. 環境變數包含所有必要的配置項（資料庫、JWT、SMTP）
7. 資料庫連線測試成功
8. 提供常見問題排除指南

**品質需求：**
9. 環境設定時間 < 30 分鐘（有經驗的開發者）
10. 文件清晰易懂，適合初級開發者
11. 錯誤訊息明確指出問題所在

**實作檢查清單：**
- [ ] 建立或更新 `.env.example` 包含所有必要變數
- [ ] 撰寫環境驗證腳本 `scripts/verify_environment.py`
- [ ] 更新 README.md 包含詳細的環境設定步驟
- [ ] 測試在乾淨的環境中完整走過設定流程
- [ ] 建立故障排除文件 `docs/TROUBLESHOOTING.md`

**Definition of Done:**
- [ ] 新開發者能在 30 分鐘內完成環境設定
- [ ] 環境驗證腳本通過所有檢查
- [ ] 文件經過至少一位新成員實際驗證
- [ ] Code Review 通過

---

## Story 0.2: 後端依賴安裝與資料庫初始化

**User Story:**
作為一個開發者，我希望能一鍵安裝所有後端依賴並初始化資料庫結構，以便快速開始後端開發。

**Acceptance Criteria:**

**功能需求：**
1. 能夠透過 `pip install -r requirements.txt` 安裝所有依賴
2. 能夠執行資料庫初始化腳本建立所有表格
3. 能夠選擇性載入測試資料
4. 能夠驗證資料庫 Schema 正確性

**技術需求：**
5. requirements.txt 包含所有核心依賴和測試框架
6. 資料庫初始化腳本支援建立/重置/刪除操作
7. 提供測試資料種子檔案（seed data）
8. 資料庫遷移使用 Flask-Migrate 管理

**品質需求：**
9. 依賴安裝時間 < 5 分鐘
10. 資料庫初始化成功率 100%
11. 提供清晰的錯誤處理和回滾機制

**實作檢查清單：**
- [ ] 確認 requirements.txt 包含測試框架（pytest, pytest-flask, pytest-cov）
- [ ] 驗證 `backend/init_db.py` 腳本功能完整
- [ ] **初始化 Flask-Migrate：執行 `python backend/init_migrations.py`**
- [ ] **驗證 migrations 目錄結構已建立**
- [ ] 建立測試資料種子檔案 `backend/seeds/test_data.py`
- [ ] 測試資料庫建立/重置/刪除流程
- [ ] 測試資料庫遷移 upgrade/downgrade 流程
- [ ] 建立資料庫 Schema 文件 `docs/database-schema.md`
- [ ] 建立資料庫遷移策略文件 `docs/database-migration-strategy.md`

**Definition of Done:**
- [ ] 所有依賴成功安裝且無衝突
- [ ] 資料庫初始化腳本通過測試
- [ ] **Flask-Migrate 已初始化且 migrations 目錄存在**
- [ ] **至少一個遷移腳本生成並測試成功**
- [ ] 測試資料載入正常
- [ ] 資料庫 Schema 文件完整
- [ ] 資料庫遷移策略文件完整
- [ ] Code Review 通過

---

## Story 0.3: 前端專案初始化與建置配置

**User Story:**
作為一個前端開發者，我希望能快速安裝前端依賴並啟動開發伺服器，以便開始前端開發。

**Acceptance Criteria:**

**功能需求：**
1. 能夠透過 `npm install` 安裝所有依賴
2. 能夠透過 `npm run dev` 啟動開發伺服器
3. 開發伺服器支援熱重載（HMR）
4. 能夠成功連接到後端 API

**技術需求：**
5. package.json 包含所有必要依賴和測試框架
6. Vite 配置支援代理後端 API 請求
7. Vue Router 和 Pinia 正確配置
8. Element Plus 主題配置完成

**品質需求：**
9. 依賴安裝時間 < 3 分鐘
10. 開發伺服器啟動時間 < 5 秒
11. 熱重載響應時間 < 1 秒

**實作檢查清單：**
- [ ] 確認 package.json 包含測試框架（vitest, @vue/test-utils）
- [ ] 驗證 vite.config.js 代理配置正確
- [ ] 測試 Vue Router 路由配置
- [ ] 測試 Pinia Store 功能
- [ ] 驗證 Element Plus 組件可用

**Definition of Done:**
- [ ] 所有依賴成功安裝
- [ ] 開發伺服器正常啟動
- [ ] 熱重載功能正常
- [ ] API 代理連接成功
- [ ] Code Review 通過

---

## Story 0.4: 測試框架設定與範例測試

**User Story:**
作為一個開發者，我希望專案有完整的測試框架設定和範例測試，以便我能為新功能編寫測試。

**Acceptance Criteria:**

**功能需求：**
1. 後端測試框架（pytest）安裝並配置完成
2. 前端測試框架（vitest）安裝並配置完成
3. 提供至少 3 個範例測試（單元測試、整合測試、E2E 測試）
4. 能夠執行測試並查看覆蓋率報告

**技術需求：**
5. 後端測試配置檔 `pytest.ini` 或 `pyproject.toml`
6. 前端測試配置檔 `vitest.config.js`
7. 測試資料庫配置（使用 SQLite in-memory）
8. Mock 服務和資料範例

**品質需求：**
9. 範例測試覆蓋率 > 80%
10. 測試執行時間 < 10 秒
11. 提供清晰的測試撰寫指南

**實作檢查清單：**
- [ ] 建立後端測試目錄結構 `backend/tests/`
- [ ] 建立前端測試目錄結構 `frontend/tests/`
- [ ] 撰寫後端範例測試（test_auth.py, test_users.py）
- [ ] 撰寫前端範例測試（Login.test.js, ActivityCard.test.js）
- [ ] 建立測試撰寫指南 `docs/testing-guide.md`
- [ ] 配置測試覆蓋率報告

**Definition of Done:**
- [ ] 測試框架安裝完成
- [ ] 範例測試全部通過
- [ ] 覆蓋率報告正常生成
- [ ] 測試指南文件完整
- [ ] Code Review 通過

---

## Story 0.5: CI/CD 管道與部署配置

**User Story:**
作為一個開發團隊，我希望有自動化的 CI/CD 管道，以便每次代碼提交都能自動測試和部署。

**Acceptance Criteria:**

**功能需求：**
1. GitHub Actions 工作流程配置完成
2. 每次 Pull Request 自動執行測試
3. main 分支合併後自動部署到測試環境
4. Docker 容器化部署配置完成

**技術需求：**
5. `.github/workflows/test.yml` 執行所有測試
6. `.github/workflows/deploy.yml` 自動部署
7. Docker Compose 配置包含所有服務
8. 環境變數安全管理（使用 GitHub Secrets）

**品質需求：**
9. CI 管道執行時間 < 5 分鐘
10. 部署成功率 > 95%
11. 提供部署失敗時的回滾機制

**實作檢查清單：**
- [ ] 建立 `.github/workflows/test.yml`
- [ ] 建立 `.github/workflows/deploy.yml`
- [ ] 驗證 docker-compose.yml 配置
- [ ] 測試 Docker 容器建置和啟動
- [ ] 建立部署文件 `docs/DEPLOYMENT.md`
- [ ] 配置 GitHub Secrets

**Definition of Done:**
- [ ] CI/CD 管道正常運作
- [ ] 測試自動化執行
- [ ] Docker 部署成功
- [ ] 部署文件完整
- [ ] Code Review 通過

---

## Story 0.6: 現有系統分析與整合點識別（Brownfield 專用）

**User Story:**
作為一個新加入團隊的開發者，我希望有完整的現有系統分析文件，以便快速了解系統架構和整合點。

**Acceptance Criteria:**

**功能需求：**
1. 系統架構圖清楚展示前後端關係
2. API 端點完整列表（從程式碼提取）
3. 資料庫 Schema 圖表和說明
4. 整合點清單（Blueprint、Socket.IO、外部服務）

**技術需求：**
5. 使用 Mermaid 繪製架構圖
6. API 端點自動化提取工具
7. 資料庫 Schema 從 models 生成
8. 整合點風險評估

**品質需求：**
9. 文件準確性 100%（與實際程式碼一致）
10. 更新頻率：每次重大變更後更新
11. 可讀性：適合新成員閱讀

**實作檢查清單：**
- [ ] 建立 `docs/existing-system-analysis.md`
- [ ] 繪製系統架構圖（Mermaid）
- [ ] 提取並記錄所有 API 端點
- [ ] 生成資料庫 Schema 文件
- [ ] 識別並記錄所有整合點
- [ ] 評估整合風險並記錄緩解措施

**Definition of Done:**
- [ ] 分析文件完整且準確
- [ ] 架構圖清晰易懂
- [ ] API 端點列表完整
- [ ] Schema 文件詳細
- [ ] 整合點風險評估完成
- [ ] Code Review 通過

---

## Epic 0 完成標準 (Epic Definition of Done)

- [ ] 所有 Story (0.1-0.6) 的 DoD 達成
- [ ] 新開發者能在 1 小時內完成環境設定並執行測試
- [ ] 所有測試通過（後端和前端）
- [ ] CI/CD 管道正常運作
- [ ] Docker 部署成功
- [ ] 現有系統分析文件完整
- [ ] 所有文件經過 Code Review
- [ ] Epic 0 的完成經過團隊 Demo 並獲得 PO 認可

---

## Epic 0 依賴關係

**Epic 0 是所有其他 Epic 的前置條件：**
- Epic 1 (使用者認證) 依賴於 Epic 0 的完成
- Epic 2 (個人資料管理) 依賴於 Epic 0 的完成
- Epic 3-7 依賴於 Epic 0 的完成

**Epic 0 內部依賴：**
- Story 0.2 依賴於 Story 0.1（需要環境設定完成）
- Story 0.3 依賴於 Story 0.1（需要環境設定完成）
- Story 0.4 依賴於 Story 0.2 和 0.3（需要依賴安裝完成）
- Story 0.5 依賴於 Story 0.4（需要測試框架完成）
- Story 0.6 可並行執行（文件工作）

---

## Epic 0 風險與緩解措施

| 風險 | 機率 | 影響 | 緩解措施 |
|------|------|------|----------|
| 依賴版本衝突 | 中 | 高 | 使用精確版本號，提供降級方案 |
| 資料庫遷移失敗 | 低 | 高 | 提供完整的回滾腳本和測試 |
| CI/CD 配置錯誤 | 中 | 中 | 在本地環境先測試所有腳本 |
| Docker 容器啟動失敗 | 低 | 中 | 提供詳細的故障排除指南 |
| 新成員學習曲線陡峭 | 中 | 中 | 提供視頻教程和一對一指導 |

---

## Epic 0 估算

**Story Points:** 21 points
- Story 0.1: 3 points
- Story 0.2: 3 points
- Story 0.3: 3 points
- Story 0.4: 5 points
- Story 0.5: 5 points
- Story 0.6: 2 points

**預估時間：** 1-2 個 Sprint（2-4 週）

**建議團隊配置：**
- 後端工程師 1 名（Story 0.2, 0.4）
- 前端工程師 1 名（Story 0.3, 0.4）
- DevOps 工程師 1 名（Story 0.5）
- 技術作家 1 名（Story 0.1, 0.6）
