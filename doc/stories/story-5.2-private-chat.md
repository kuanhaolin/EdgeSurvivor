# Story 5.2: 私人聊天室 - Brownfield Documentation

## User Story

作為一個用戶，
當我與他人媒合成功後 (Activity Match or Private Match)，
我希望能自動開啟一個私人聊天室，
以便進行私下協調和溝通旅行細節。

## Story Context

**Existing System Integration:**

- Integrates with: Matching System, Real-time Communication System
- Technology: Python/Flask, Socket.IO, PostgreSQL
- Follows pattern: WebSocket-based real-time messaging
- Touch points: ackend/socketio_events.py, ackend/models/chat_message.py, ackend/blueprints/chat.py

**Current Implementation Status:**  Completed (MVP)

## Acceptance Criteria

**Functional Requirements:**

1. 媒合成功時系統自動建立私人聊天室
2. 只有聊天室成員可以查看和發送訊息
3. 支援文字訊息的即時發送和接收
4. 顯示訊息歷史記錄（分頁載入）

**Integration Requirements:**

5. 聊天室需使用 Socket.IO 支援即時通訊
6. 系統需支援訊息歷史記錄、未讀計數和訊息狀態（已發送/已讀）
7. 訊息儲存於 chat_messages 資料表
8. WebSocket 連線需使用 JWT 認證

**Quality Requirements:**

9. 訊息延遲需 < 100ms
10. 斷線重連後需自動恢復聊天狀態
11. 訊息歷史需支援分頁（每頁 50 則）
12. 未讀計數需即時更新

## Technical Notes

- **Integration Approach:** 
  - Socket.IO rooms for private chat isolation
  - JWT token in Socket.IO handshake for authentication
  - Message persistence in PostgreSQL
- **Existing Pattern Reference:** 
  - Socket.IO Events:
    - Client  Server: 'send_message', 'join_room', 'mark_as_read'
    - Server  Client: 'new_message', 'message_read', 'user_typing'
  - REST API: GET /api/chat/rooms/<room_id>/messages
- **Key Constraints:** 
  - 只有房間成員可加入 Socket.IO room
  - 訊息無法編輯或刪除（MVP 限制）
  - 不支援檔案傳送（MVP 限制）

## API Specification

**REST API (Message History):**
\\\json
GET /api/chat/rooms/<room_id>/messages?page=1&limit=50
Headers:
  Authorization: Bearer <JWT_TOKEN>

Response:
{
  "messages": [
    {
      "id": 1001,
      "room_id": 111,
      "user_id": 123,
      "username": "johndoe",
      "content": "你好！什麼時候出發？",
      "created_at": "2025-11-03T10:30:00Z",
      "read": true
    },
    ...
  ],
  "total": 234,
  "page": 1,
  "pages": 5
}
\\\

**Socket.IO Events:**
\\\javascript
// Client sends message
socket.emit('send_message', {
  room_id: 111,
  content: "明天早上 8 點集合可以嗎？"
});

// Server broadcasts to room
socket.on('new_message', (data) => {
  // data: { id, room_id, user_id, username, content, created_at }
});

// Mark messages as read
socket.emit('mark_as_read', {
  room_id: 111,
  message_ids: [1001, 1002, 1003]
});
\\\

## Database Schema

\\\sql
chat_messages table:
- id (PRIMARY KEY)
- room_id (FOREIGN KEY -> chat_rooms.id)
- user_id (FOREIGN KEY -> users.id)
- content (TEXT, NOT NULL)
- read (BOOLEAN, DEFAULT false)
- created_at (TIMESTAMP)

chat_rooms table:
- id (PRIMARY KEY)
- activity_id (FOREIGN KEY -> activities.id, NULLABLE)
- type (ENUM: activity/private)
- created_at (TIMESTAMP)

chat_room_members table:
- id (PRIMARY KEY)
- room_id (FOREIGN KEY -> chat_rooms.id)
- user_id (FOREIGN KEY -> users.id)
- unread_count (INTEGER, DEFAULT 0)
- last_read_at (TIMESTAMP)
\\\

## Real-time Features

- **Typing Indicator:** 顯示對方正在輸入
- **Online Status:** 顯示成員在線狀態
- **Message Read Receipts:** 顯示訊息已讀狀態
- **Unread Badge:** 顯示未讀訊息數量

## Definition of Done

- [x] Functional requirements met
- [x] Socket.IO integration working
- [x] Message persistence implemented
- [x] Unread count tracking working
- [x] Message history pagination working
- [x] Real-time features (typing, online status) working
- [x] Tests pass (existing and new)
- [x] Frontend chat UI created

## Risk and Compatibility Check

**Primary Risk:** Socket.IO 連線數過多導致伺服器負載過高

**Mitigation:** 
- 實作連線數限制和 rate limiting
- 考慮使用 Redis 作為 Socket.IO adapter (水平擴展)
- 監控 WebSocket 連線數和訊息頻率

**Rollback:** 停用 Socket.IO，降級為輪詢式聊天（每 5 秒刷新）

## Performance Considerations

- 使用 Redis 快取活躍聊天室的最新訊息
- 舊訊息（> 30 天）考慮歸檔
- 圖片訊息（未來）需使用 CDN
- 大型群組（未來）需實作訊息分片

## Related Files

- ackend/socketio_events.py
- ackend/blueprints/chat.py
- ackend/models/chat_message.py
- rontend/src/services/socket.js
- rontend/src/views/Chat.vue
- rontend/src/components/chat/ChatRoom.vue

## Notes

此功能是媒合後的關鍵溝通管道，已於 MVP 階段完成。
未來可考慮新增：語音訊息、圖片傳送、位置分享、訊息搜尋等功能。
