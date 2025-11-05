# Story 3.1: 建立活動 - Brownfield Documentation

## User Story

作為一個活動組織者，
我希望能建立一項新活動，包含標題、日期、地點、描述、類別、人數上限、費用和封面圖，
以便招募志同道合的旅伴。

## Story Context

**Existing System Integration:**

- Integrates with: Activity Management System
- Technology: Python/Flask, PostgreSQL, Image Upload Service
- Follows pattern: RESTful API with multipart form data for image upload
- Touch points: ackend/blueprints/activities.py, ackend/models/activity.py, ackend/blueprints/upload.py

**Current Implementation Status:**  Completed (MVP)

## Acceptance Criteria

**Functional Requirements:**

1. 組織者可填寫活動表單並提交建立新活動
2. 必填欄位包含：標題、日期、地點、描述
3. 可選欄位包含：類別、人數上限、預估費用、封面圖
4. 活動建立後預設狀態為「開放 (open)」

**Integration Requirements:**

5. 活動建立者自動成為該活動的組織者 (creator_id)
6. 封面圖上傳需使用統一的 upload service
7. 活動資料儲存於 activities 資料表
8. 建立成功後返回完整的活動資訊和活動 ID

**Quality Requirements:**

9. 圖片大小限制為 16MB
10. 支援的圖片格式：jpg, jpeg, png, gif
11. 活動日期不得早於當前日期
12. API 回應時間需 < 1000ms (含圖片上傳)

## Technical Notes

- **Integration Approach:** 
  - 使用 Flask multipart/form-data 處理圖片上傳
  - 圖片儲存於 ackend/uploads/activities/ 目錄
- **Existing Pattern Reference:** 
  - API Endpoint: POST /api/activities
  - Requires JWT authentication
  - Response: JSON with activity data
- **Key Constraints:** 
  - 需要 JWT 認證才能建立活動
  - creator_id 從 JWT token 中提取
  - 封面圖為可選，但建議上傳以提升曝光

## API Specification

\\\json
POST /api/activities
Headers:
  Authorization: Bearer <JWT_TOKEN>
  Content-Type: multipart/form-data

Request Body (form-data):
{
  "title": "陽明山賞花一日遊",
  "description": "春天到陽明山看海芋...",
  "location": "台北市陽明山",
  "activity_date": "2025-04-15",
  "category": "nature",
  "max_participants": 6,
  "estimated_cost": 500,
  "cover_image": <file>
}

Response (Success):
{
  "id": 456,
  "title": "陽明山賞花一日遊",
  "creator_id": 123,
  "status": "open",
  "cover_image_url": "/uploads/activities/456_cover.jpg",
  "created_at": "2025-11-03T10:30:00Z"
  ...
}
\\\

## Database Schema

\\\sql
activities table:
- id (PRIMARY KEY)
- title (VARCHAR, NOT NULL)
- description (TEXT)
- location (VARCHAR, NOT NULL)
- activity_date (DATE, NOT NULL)
- category (VARCHAR)
- max_participants (INTEGER)
- estimated_cost (DECIMAL)
- cover_image (VARCHAR)
- creator_id (FOREIGN KEY -> users.id)
- status (ENUM: open/ongoing/completed/cancelled)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
\\\

## UI/UX Considerations

- 表單應提供日期選擇器
- 封面圖上傳應有預覽功能
- 費用欄位應允許輸入小數點
- 人數上限建議預設為 4-8 人
- 提交前應有表單驗證

## Definition of Done

- [x] Functional requirements met
- [x] Integration requirements verified
- [x] Image upload service integration tested
- [x] Form validation implemented
- [x] Database constraints properly set
- [x] Tests pass (existing and new)
- [x] Frontend form created and tested

## Risk and Compatibility Check

**Primary Risk:** 大量圖片上傳可能導致儲存空間不足

**Mitigation:** 
- 實作圖片壓縮和縮圖功能
- 設定儲存容量監控
- 考慮未來移至雲端儲存 (S3, GCS)

**Rollback:** 刪除上傳的圖片檔案，回滾資料庫記錄

## Related Files

- ackend/blueprints/activities.py
- ackend/models/activity.py
- ackend/blueprints/upload.py
- rontend/src/views/activities/CreateActivity.vue

## Notes

此功能是平台的核心功能之一，已於 MVP 階段完成。
未來可考慮新增：多張圖片上傳、活動模板、重複活動等功能。
