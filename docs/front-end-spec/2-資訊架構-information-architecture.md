# 2. 資訊架構 (Information Architecture)

## 2.1 網站地圖

\\\mermaid
graph TD
    A[首頁 Home] --> B[註冊/登入 Auth]
    A --> C[控制台 Dashboard]
    A --> D[活動 Activities]
    A --> E[交友 Matches]
    A --> F[聊天 Chat]
    A --> G[個人資料 Profile]
    
    B --> B1[註冊 Register]
    B --> B2[登入 Login]
    B --> B3[忘記密碼 Forgot Password]
    B --> B4[Google OAuth]
    
    C --> C1[統計資訊 Stats]
    C --> C2[最近活動 Recent Activities]
    C --> C3[最新好友 Recent Matches]
    C --> C4[快速操作 Quick Actions]
    
    D --> D1[探索活動 Discover]
    D --> D2[我的活動 My Activities]
    D --> D3[我創建的 Created]
    D --> D4[我參加的 Joined]
    D --> D5[活動詳情 Activity Detail]
    D --> D6[創建活動 Create Activity]
    
    D5 --> D5A[活動資訊 Info]
    D5 --> D5B[參與者 Participants]
    D5 --> D5C[討論串 Discussion]
    D5 --> D5D[費用管理 Expenses]
    D5 --> D5E[相簿 Gallery]
    D5 --> D5F[評價 Reviews]
    
    E --> E1[媒合申請 Match Requests]
    E --> E2[我的好友 My Matches]
    
    F --> F1[聊天列表 Chat List]
    F --> F2[聊天室 Chat Room]
    
    G --> G1[編輯資料 Edit Profile]
    G --> G2[帳號設定 Account Settings]
    G --> G3[隱私設定 Privacy]
\\\

## 2.2 導航結構

### 主導航 (Primary Navigation)
位於頂部導航欄，提供核心功能的快速訪問：
- **控制台** (Dashboard) - 個人化的儀表板首頁
- **活動** (Activities) - 瀏覽、創建、管理活動
- **交友** (Matches) - 媒合請求與好友列表
- **聊天** (Chat) - 即時訊息中心（顯示未讀數徽章）

### 次要導航 (Secondary Navigation)
- **使用者下拉選單** - 個人資料、帳號設定、登出
- **活動子導航** - 探索活動、我的活動、我創建的、我參加的

### 麵包屑導航 (Breadcrumb)
用於深層頁面（如活動詳情）：
\活動 > 探索活動 > 陽明山登山之旅\

---
