# Story 6.3: 費用自動結算 - Brownfield Documentation

## User Story

作為一個活動參與者，
我希望能點擊「結算」，系統應自動計算出最佳分攤方案（最少轉帳次數），
以便清楚知道誰該付給誰多少錢，避免金錢糾紛。

## Story Context

**Existing System Integration:**

- Integrates with: Expense Management System
- Technology: Python/Flask, PostgreSQL, Greedy Algorithm
- Follows pattern: RESTful API with complex calculation logic
- Touch points: ackend/blueprints/expenses.py, ackend/models/expense.py

**Current Implementation Status:**  Completed (MVP)

## Acceptance Criteria

**Functional Requirements:**

1. 參與者可點擊「結算」按鈕觸發自動計算
2. 系統計算每個人應付和應收的金額
3. 使用貪婪演算法找出最少轉帳次數的結算方案
4. 顯示清楚的結算報告（誰該付給誰多少錢）

**Integration Requirements:**

5. 結算基於該活動的所有費用記錄
6. 只有活動參與者可查看結算結果
7. 結算結果儲存於資料庫供後續查詢
8. 支援多次結算（新增費用後重新計算）

**Quality Requirements:**

9. 計算準確度需達到分（小數點後兩位）
10. 轉帳次數應為最少（使用最佳化演算法）
11. API 回應時間需 < 1000ms（即使有 100 筆費用）
12. 結算報告需易讀且清楚

## Technical Notes

- **Integration Approach:** 
  - 使用 Greedy Algorithm 進行債務簡化
  - 計算每人淨額（應收 - 應付）
  - 配對債權人和債務人以最小化轉帳次數
- **Existing Pattern Reference:** 
  - API Endpoint: POST /api/expenses/activities/<activity_id>/settle
  - Response: Settlement transactions list
- **Key Constraints:** 
  - 只計算狀態為 'approved' 的費用
  - 結算不會刪除或修改原始費用記錄
  - 結算結果為建議，實際轉帳由用戶自行執行

## API Specification

\\\json
POST /api/expenses/activities/<activity_id>/settle
Headers:
  Authorization: Bearer <JWT_TOKEN>

Response (Success):
{
  "activity_id": 456,
  "total_expenses": 5000.00,
  "participants": [
    {
      "user_id": 123,
      "username": "johndoe",
      "paid": 2000.00,
      "should_pay": 1666.67,
      "balance": 333.33  // positive: should receive
    },
    {
      "user_id": 124,
      "username": "jane",
      "paid": 1500.00,
      "should_pay": 1666.67,
      "balance": -166.67  // negative: should pay
    },
    {
      "user_id": 125,
      "username": "bob",
      "paid": 1500.00,
      "should_pay": 1666.67,
      "balance": -166.67
    }
  ],
  "transactions": [
    {
      "from": "jane",
      "to": "johndoe",
      "amount": 166.67
    },
    {
      "from": "bob",
      "to": "johndoe",
      "amount": 166.67
    }
  ],
  "settled_at": "2025-11-03T10:30:00Z"
}
\\\

## Algorithm Explanation

**Debt Simplification Algorithm:**

1. 計算每個參與者的淨額（paid - should_pay）
2. 將參與者分為債權人（balance > 0）和債務人（balance < 0）
3. 貪婪配對：
   - 找出最大債權人和最大債務人
   - 計算可抵消金額 = min(債權金額, 債務金額)
   - 生成一筆轉帳記錄
   - 更新雙方餘額
   - 重複直到所有債務抵消

**時間複雜度:** O(n) where n = 參與者人數
**空間複雜度:** O(n)

## Database Schema

\\\sql
expenses table:
- id (PRIMARY KEY)
- activity_id (FOREIGN KEY -> activities.id)
- payer_id (FOREIGN KEY -> users.id)
- amount (DECIMAL, NOT NULL)
- category (VARCHAR)
- description (TEXT)
- status (ENUM: pending/approved)
- created_at (TIMESTAMP)

settlements table:
- id (PRIMARY KEY)
- activity_id (FOREIGN KEY -> activities.id)
- settlement_data (JSON)  -- stores full settlement result
- created_at (TIMESTAMP)
\\\

## Business Logic

**Settlement Rules:**
- 平均分攤：每人應付 = 總費用 / 參與人數
- 只計算已批准的費用（status = 'approved'）
- 組織者可選擇是否將自己計入分攤
- 小數點四捨五入至分（0.01）

**Edge Cases:**
- 無費用記錄：返回空結算
- 單一參與者：無需結算
- 費用已完全平衡：返回零轉帳

## Definition of Done

- [x] Functional requirements met
- [x] Settlement algorithm implemented and tested
- [x] Calculation accuracy verified
- [x] Edge cases handled
- [x] Frontend settlement report UI created
- [x] Tests pass (unit tests for algorithm)
- [x] Performance benchmarks met

## Risk and Compatibility Check

**Primary Risk:** 浮點數計算精度問題導致結算不平衡

**Mitigation:** 
- 使用 Python Decimal 類型確保精度
- 在資料庫層級使用 DECIMAL 而非 FLOAT
- 四捨五入策略統一處理
- 單元測試覆蓋各種金額組合

**Rollback:** 簡單，刪除 settlements 表記錄即可

## Testing Scenarios

\\\python
# Test Case 1: 三人均攤
Alice paid: 300, Bob paid: 0, Charlie paid: 0
Expected: Bob  Alice: 100, Charlie  Alice: 100

# Test Case 2: 複雜分攤
Alice paid: 500, Bob paid: 300, Charlie paid: 200
Total: 1000, Each should pay: 333.33
Expected: Charlie  Alice: 133.33

# Test Case 3: 已平衡
Alice paid: 100, Bob paid: 100, Charlie paid: 100
Expected: No transactions needed
\\\

## Related Files

- ackend/blueprints/expenses.py
- ackend/models/expense.py
- rontend/src/views/expenses/ExpenseSettlement.vue
- rontend/src/components/ExpenseManager.vue

## Notes

此功能是平台的獨特價值之一，解決旅途中最容易產生摩擦的金錢問題。
已於 MVP 階段完成並通過測試。
未來可考慮新增：匯出結算報告 PDF、整合支付平台、分類統計等功能。
