# 附錄 C：組件層級結構

```
App.vue
├── NavBar.vue (布局)
├── Router View
    ├── Dashboard.vue (頁面)
    │   ├── StatCard.vue (組件)
    │   ├── ActivityCard.vue (組件)
    │   └── MatchCard.vue (組件)
    ├── Activities.vue (頁面)
    │   ├── ActivityFilters.vue (組件)
    │   └── ActivityCard.vue (組件)
    ├── ActivityDetail.vue (頁面)
    │   ├── ParticipantList.vue (組件)
    │   ├── ActivityDiscussion.vue (組件)
    │   ├── ExpenseManager.vue (組件)
    │   └── ActivityReviews.vue (組件)
    └── Chat.vue (頁面)
        ├── ChatList.vue (組件)
        └── ChatWindow.vue (組件)
            ├── MessageBubble.vue (組件)
            └── MessageInput.vue (組件)
```

---

**文檔結尾**

此前端技術架構文件由 Winston (Architect) 建立，基於 EdgeSurvivor PRD v1.0 和 UI/UX 規格 v1.0。如有任何問題或建議，請聯繫專案團隊。

**版本**：1.0  
**最後更新**：2025-11-03  
**狀態**：Active

---

**下一步行動**：

1. **前端開發團隊**：檢閱此架構文件，確認技術選型與實現方案
2. **DevOps 團隊**：根據部署章節設置 CI/CD Pipeline
3. **QA 團隊**：根據測試策略章節準備測試計畫
4. **PM 團隊**：驗證架構是否滿足 PRD 中的所有需求

**相關文件**：
- [產品需求文件 (PRD)](./prd.md)
- [UI/UX 規格文檔](./front-end-spec.md)
- [後端架構文檔](./backend-architecture.md) *(待建立)*


由於文件較長，我將分批繼續生成。接下來會包含路由配置、樣式指南、環境配置等內容。

