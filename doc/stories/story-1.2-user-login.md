# Story 1.2: 使用者登入 - Brownfield Documentation

## User Story

作為一個已註冊用戶，
我希望能使用 Email 和密碼登入，
以便存取我的資料。

## Story Context

**Existing System Integration:**

- Integrates with: Flask-based authentication system with JWT
- Technology: Python/Flask, PostgreSQL, JWT, scrypt password verification
- Follows pattern: RESTful API with stateless authentication
- Touch points: ackend/blueprints/auth.py, ackend/models/user.py

**Current Implementation Status:**  Completed (MVP)

## Acceptance Criteria

**Functional Requirements:**

1. 用戶可使用註冊的 Email 和密碼登入
2. 系統驗證 Email 和密碼是否正確
3. 密碼錯誤超過 5 次應有暫時鎖定機制

**Integration Requirements:**

4. 登入成功後需返回 JWT Token
5. JWT Token 包含用戶 ID 和基本資訊
6. Token 有效期為 24 小時

**Quality Requirements:**

7. 錯誤的登入資訊應返回通用錯誤訊息（避免洩漏帳號存在性）
8. API 回應時間需 < 500ms
9. 密碼驗證使用安全的時間恆定比較

## Technical Notes

- **Integration Approach:** 使用 Flask-JWT-Extended 管理 Token
- **Existing Pattern Reference:** 
  - API Endpoint: POST /api/auth/login
  - Response: JSON with JWT token and user info
- **Key Constraints:** 
  - 不儲存明文密碼，使用 scrypt 驗證
  - JWT secret 需從環境變數讀取
  - 登入失敗記錄應寫入日誌

## API Specification

\\\json
POST /api/auth/login
Request Body:
{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response (Success):
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 123,
    "email": "user@example.com",
    "username": "johndoe",
    "email_verified": true
  }
}

Response (Error):
{
  "error": "登入失敗，請檢查您的帳號密碼"
}
\\\

## Security Considerations

- 密碼驗證失敗不應洩漏帳號是否存在
- 使用 timing-safe 比較避免 timing attack
- 登入失敗應有 rate limiting (待實作)
- JWT Token 應設定合理的過期時間

## Definition of Done

- [x] Functional requirements met
- [x] Integration requirements verified
- [x] JWT token 正確生成並可驗證
- [x] Code follows existing patterns and standards
- [x] Tests pass (existing and new)
- [x] Security review completed

## Risk and Compatibility Check

**Primary Risk:** JWT Secret 洩漏導致 Token 可被偽造

**Mitigation:** 
- Secret 儲存於環境變數，不提交至版控
- 定期輪替 JWT Secret
- 實作 Token 黑名單機制（登出功能）

**Rollback:** 簡單，僅需恢復 auth.py 即可

## Related Files

- ackend/blueprints/auth.py
- ackend/models/user.py
- ackend/config.py

## Notes

此功能已於 MVP 階段完成並通過測試。
JWT Token 管理是整個系統安全的核心，需特別注意 secret 的保護。
