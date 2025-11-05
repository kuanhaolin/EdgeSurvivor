# Story 1.1: 使用者註冊 - Brownfield Documentation

## User Story

作為一個新用戶，
我希望能使用 Email 和密碼註冊帳號，
以便開始使用平台。

## Story Context

**Existing System Integration:**

- Integrates with: Flask-based authentication system
- Technology: Python/Flask, PostgreSQL, scrypt
- Follows pattern: RESTful API with JWT authentication
- Touch points: ackend/blueprints/auth.py, ackend/models/user.py

**Current Implementation Status:**  Completed (MVP)

## Acceptance Criteria

**Functional Requirements:**

1. 用戶可透過 Email 和密碼完成註冊
2. 系統驗證 Email 格式是否正確
3. 密碼長度需符合最低安全要求 (8 字元以上)

**Integration Requirements:**

4. 密碼需使用 scrypt 加密儲存
5. 註冊後需發送 Email 驗證信
6. 註冊成功後自動建立 User 記錄於資料庫

**Quality Requirements:**

7. 重複 Email 註冊應返回適當錯誤訊息
8. API 回應時間需 < 500ms
9. 密碼加密強度符合安全標準

## Technical Notes

- **Integration Approach:** 使用 Flask Blueprint 模組化路由處理
- **Existing Pattern Reference:** 
  - API Endpoint: POST /api/auth/register
  - Response: JSON with user data and JWT token
- **Key Constraints:** 
  - Email 必須唯一
  - 密碼儲存採用 scrypt (不可逆加密)
  - Email 驗證功能需配置 SMTP 設定

## API Specification

\\\json
POST /api/auth/register
Request Body:
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "username": "johndoe"
}

Response (Success):
{
  "message": "註冊成功，請查收驗證信",
  "user_id": 123,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Response (Error):
{
  "error": "Email 已被使用"
}
\\\

## Database Schema

\\\sql
users table:
- id (PRIMARY KEY)
- email (UNIQUE, NOT NULL)
- password_hash (NOT NULL)
- username (NOT NULL)
- email_verified (BOOLEAN, DEFAULT false)
- created_at (TIMESTAMP)
\\\

## Definition of Done

- [x] Functional requirements met
- [x] Integration requirements verified
- [x] Existing functionality regression tested
- [x] Code follows existing patterns and standards
- [x] Tests pass (existing and new)
- [x] Documentation updated if applicable

## Risk and Compatibility Check

**Primary Risk:** Email 服務設定錯誤導致驗證信無法發送

**Mitigation:** 
- 提供本地開發環境的 Email 測試工具
- 設定詳細的 Email 錯誤日誌
- 允許管理員手動驗證用戶

**Rollback:** 資料庫採用 migration，可回滾至前一版本

## Related Files

- ackend/blueprints/auth.py
- ackend/models/user.py
- ackend/utils/email.py
- ackend/config.py

## Notes

此功能已於 MVP 階段完成並通過測試。
