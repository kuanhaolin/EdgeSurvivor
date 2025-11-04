# Story 4.2: 審核媒合申請 - Brownfield Documentation

## User Story

作為一個活動組織者，
我希望能查看所有申請列表，並對申請進行「批准」或「拒絕」，
以便篩選合適的旅伴並控制活動品質。

## Story Context

**Existing System Integration:**

- Integrates with: Matching System, Chat System
- Technology: Python/Flask, PostgreSQL, Socket.IO
- Follows pattern: RESTful API with WebSocket notification
- Touch points: ackend/blueprints/matches.py, ackend/models/match.py, ackend/socketio_events.py

**Current Implementation Status:**  Completed (MVP)

## Acceptance Criteria

**Functional Requirements:**

1. 組織者可查看特定活動的所有待審核申請列表
2. 每個申請顯示申請者的基本資料和附帶訊息
3. 組織者可對申請執行「批准」或「拒絕」操作
4. 申請狀態更新後，申請者應收到即時通知

**Integration Requirements:**

5. 雙方確認（媒合成功）後，系統應自動開啟私人聊天室
6. 批准的參與者自動加入 activity_participants 表
7. 媒合狀態變更需透過 Socket.IO 即時通知申請者
8. 達到人數上限時，活動狀態自動變為「進行中 (ongoing)」

**Quality Requirements:**

9. 只有活動組織者可審核申請
10. 已拒絕的申請不可再次批准（需重新申請）
11. 批准操作需檢查是否已達人數上限
12. API 回應時間需 < 500ms

## Technical Notes

- **Integration Approach:** 
  - Match status flow: pending  approved/rejected
  - Auto-create chat room on approval
  - WebSocket event: 'match_status_updated'
- **Existing Pattern Reference:** 
  - API Endpoint: PATCH /api/matches/<match_id>/status
  - Requires JWT authentication and creator verification
- **Key Constraints:** 
  - 只有 creator_id 等於當前用戶的活動可審核
  - 批准後無法撤銷（只能移除參與者）
  - 聊天室建立失敗不應影響媒合狀態

## API Specification

\\\json
PATCH /api/matches/<match_id>/status
Headers:
  Authorization: Bearer <JWT_TOKEN>

Request Body:
{
  "status": "approved"  // or "rejected"
}

Response (Success):
{
  "id": 789,
  "activity_id": 456,
  "user_id": 123,
  "status": "approved",
  "chat_room_id": 111,  // only if approved
  "updated_at": "2025-11-03T10:30:00Z"
}

WebSocket Event (to applicant):
{
  "event": "match_status_updated",
  "data": {
    "match_id": 789,
    "activity_title": "陽明山賞花一日遊",
    "status": "approved",
    "chat_room_id": 111
  }
}
\\\

## Database Schema

\\\sql
matches table:
- id (PRIMARY KEY)
- activity_id (FOREIGN KEY -> activities.id)
- user_id (FOREIGN KEY -> users.id)
- status (ENUM: pending/approved/rejected)
- message (TEXT) -- applicant's message
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

activity_participants table:
- id (PRIMARY KEY)
- activity_id (FOREIGN KEY -> activities.id)
- user_id (FOREIGN KEY -> users.id)
- joined_at (TIMESTAMP)

chat_rooms table:
- id (PRIMARY KEY)
- activity_id (FOREIGN KEY -> activities.id)
- type (ENUM: activity/private)
- created_at (TIMESTAMP)
\\\

## Business Logic

**Approval Flow:**
1. Verify requester is activity creator
2. Check if activity has reached max_participants
3. Update match status to 'approved'
4. Insert record into activity_participants
5. Create private chat room
6. Send WebSocket notification to applicant
7. Update activity status if max reached

**Rejection Flow:**
1. Verify requester is activity creator
2. Update match status to 'rejected'
3. Send WebSocket notification to applicant

## Definition of Done

- [x] Functional requirements met
- [x] Integration with chat system verified
- [x] WebSocket notifications working
- [x] Participant limit enforcement working
- [x] Authorization checks implemented
- [x] Tests pass (existing and new)
- [x] Frontend UI for approval/rejection created

## Risk and Compatibility Check

**Primary Risk:** 聊天室建立失敗導致媒合狀態不一致

**Mitigation:** 
- 使用資料庫 transaction 確保原子性
- 聊天室建立失敗時回滾媒合狀態
- 實作重試機制或手動修復工具

**Rollback:** 需同時回滾 matches, activity_participants, chat_rooms 三個表

## Related Files

- ackend/blueprints/matches.py
- ackend/models/match.py
- ackend/models/activity_participant.py
- ackend/socketio_events.py
- rontend/src/views/matches/MatchRequests.vue

## Notes

此功能是平台的核心價值所在，實現了雙向確認的安全媒合機制。
未來可考慮新增：自動批准機制、批量審核、申請評分系統等功能。
