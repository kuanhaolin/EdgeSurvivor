# EdgeSurvivor UI/UX 規格文檔
# 邊緣人神器 - 旅伴媒合平台前端規範

**Version:** 1.0  
**Status:** Draft  
**Date:** 2025-11-03  
**Owner:** UX Expert (Sally)

---

## 1. 簡介 (Introduction)

此文檔定義 EdgeSurvivor（邊緣人神器）的使用者體驗目標、資訊架構、使用者流程和視覺設計規範。它作為視覺設計和前端開發的基礎，確保一致且以使用者為中心的體驗。

EdgeSurvivor 採用 **Vue 3 + Element Plus** 技術棧，搭配 **玻璃擬態（Glassmorphism）** 設計風格，提供現代、優雅且易用的旅伴媒合平台。

### 1.1 整體 UX 目標與原則

#### 目標用戶群

1. **獨自旅行者 (Solo Travelers)**
   - 年齡：22-35 歲
   - 特徵：活躍於社群媒體，重視旅行品質
   - 痛點：找不到合適的同行者、安全顧慮、費用分攤困難
   - 需求：安全可靠的平台、志趣相投的旅伴、清楚的費用管理

2. **活動組織者 (Activity Organizers)**
   - 年齡：25-40 歲
   - 特徵：熱愛規劃，樂於分享，有組團經驗
   - 痛點：招募效率低、行程討論分散、費用收款麻煩
   - 需求：結構化的發布工具、參與者篩選功能、統一的討論平台

#### 核心可用性目標

- **易於上手**：新用戶能在 3 分鐘內完成註冊並瀏覽活動
- **高效媒合**：用戶能在 5 分鐘內找到並申請感興趣的活動
- **安全信任**：透過個人資料、評價系統建立信任機制，降低安全顧慮
- **即時互動**：即時聊天和討論串提供流暢的溝通體驗
- **錯誤預防**：關鍵操作（刪除、取消）需要二次確認

#### 設計原則

1. **信任優先 (Trust First)**  
   透過透明的個人資料、評價和驗證機制建立信任感。每個用戶資料頁都清楚顯示參與活動數、評價星級、社群連結等。

2. **簡化決策 (Simplify Choices)**  
   用清晰的篩選和資訊呈現幫助用戶快速做決定。活動卡片顯示關鍵資訊（日期、地點、人數、類型），避免資訊過載。

3. **即時回饋 (Immediate Feedback)**  
   每個操作都有明確的視覺和訊息回饋。按鈕點擊有動畫效果，操作結果有 Toast 通知，加載狀態有骨架屏或 Spinner。

4. **漸進式揭露 (Progressive Disclosure)**  
   優先顯示核心資訊，進階功能透過點擊展開。活動列表顯示摘要，詳細頁面展開完整資訊。

5. **情感連結 (Emotional Connection)**  
   使用溫暖的視覺語言和文案，營造友善的社群氛圍。藍紫漸變色傳遞夢幻與冒險感，微動畫增加愉悅感。

### 1.2 變更日誌

| 日期 | 版本 | 描述 | 作者 |
|------|------|------|------|
| 2025-11-03 | 1.0 | 初始 UI/UX 規格文檔 | Sally (UX Expert) |

---

## 2. 資訊架構 (Information Architecture)

### 2.1 網站地圖

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

### 2.2 導航結構

#### 主導航 (Primary Navigation)
位於頂部導航欄，提供核心功能的快速訪問：
- **控制台** (Dashboard) - 個人化的儀表板首頁
- **活動** (Activities) - 瀏覽、創建、管理活動
- **交友** (Matches) - 媒合請求與好友列表
- **聊天** (Chat) - 即時訊息中心（顯示未讀數徽章）

#### 次要導航 (Secondary Navigation)
- **使用者下拉選單** - 個人資料、帳號設定、登出
- **活動子導航** - 探索活動、我的活動、我創建的、我參加的

#### 麵包屑導航 (Breadcrumb)
用於深層頁面（如活動詳情）：
\活動 > 探索活動 > 陽明山登山之旅\

---

## 3. 使用者流程 (User Flows)

### 3.1 新用戶註冊流程

**使用者目標**：快速註冊帳號，開始使用平台

**入口點**：首頁、活動列表（未登入狀態）

**成功標準**：完成註冊並驗證 Email

\\\mermaid
graph TD
    Start[訪客進入網站] --> Choice{選擇註冊方式}
    Choice -->|Email註冊| Form[填寫註冊表單]
    Choice -->|Google登入| OAuth[Google OAuth流程]
    
    Form --> Validate{表單驗證}
    Validate -->|失敗| Error[顯示錯誤訊息]
    Error --> Form
    Validate -->|成功| Submit[送出註冊]
    
    Submit --> EmailSent[顯示驗證信已發送]
    EmailSent --> CheckEmail[用戶檢查Email]
    CheckEmail --> VerifyLink[點擊驗證連結]
    VerifyLink --> Verified[帳號驗證成功]
    
    OAuth --> GoogleAuth[Google授權]
    GoogleAuth --> AutoCreate[自動建立帳號]
    
    AutoCreate --> Dashboard[進入控制台]
    Verified --> Dashboard
    
    Dashboard --> Complete[註冊完成]
\\\

**邊界案例與錯誤處理**：
- Email 已被註冊  提示「此 Email 已被使用，請使用其他 Email 或嘗試登入」
- 密碼強度不足  即時顯示密碼強度指示器，要求至少 8 字元
- Email 驗證連結過期  提供「重新發送驗證信」按鈕
- Google OAuth 失敗  提示「Google 登入失敗，請稍後再試或使用 Email 註冊」

**註釋**：Google OAuth 可跳過 Email 驗證步驟，提供更快速的註冊體驗。

### 3.2 發布活動流程

**使用者目標**：創建一個新活動來招募旅伴

**入口點**：控制台快速操作、活動頁面頂部按鈕

**成功標準**：活動成功創建並顯示在活動列表

\\\mermaid
graph TD
    Start[點擊創建活動按鈕] --> Dialog[開啟創建活動對話框]
    Dialog --> FillForm[填寫活動表單]
    
    FillForm --> Required{必填欄位檢查}
    Required -->|缺少必填| ShowError[標示缺少的欄位]
    ShowError --> FillForm
    
    Required -->|完整| Preview{預覽?}
    Preview -->|是| ShowPreview[顯示活動預覽]
    ShowPreview --> Confirm{確認發布?}
    
    Preview -->|否| Confirm
    Confirm -->|取消| Cancel[關閉對話框]
    Confirm -->|確認| Submit[送出活動]
    
    Submit --> Creating[顯示載入動畫]
    Creating --> Success{創建成功?}
    
    Success -->|失敗| ErrorMsg[顯示錯誤訊息]
    ErrorMsg --> FillForm
    
    Success -->|成功| Toast[顯示成功訊息]
    Toast --> Redirect[跳轉到活動詳情頁]
    Redirect --> Complete[流程完成]
\\\

**邊界案例與錯誤處理**：
- 日期選擇過去的日期  提示「活動日期不能早於今天」
- 人數上限小於 2  提示「至少需要 2 人參加」
- 圖片上傳超過 16MB  提示「圖片大小不能超過 16MB，請壓縮後上傳」
- 網路連線失敗  保留表單資料，提示「網路連線失敗，請稍後再試」

**註釋**：表單支援自動儲存草稿（localStorage），避免用戶意外關閉時資料遺失。

---

### 3.3 申請加入活動流程

**使用者目標**：申請加入感興趣的活動

**入口點**：活動詳情頁、探索活動列表

**成功標準**：申請成功送出，等待組織者審核

\\\mermaid
graph TD
    Start[瀏覽活動詳情] --> Check{檢查條件}
    Check -->|未登入| Login[提示登入]
    Check -->|已滿額| Disabled[申請按鈕禁用]
    Check -->|已申請| ShowStatus[顯示申請狀態]
    Check -->|可申請| Enable[啟用申請按鈕]
    
    Login --> LoginPage[跳轉登入頁]
    LoginPage --> Back[登入後返回]
    Back --> Enable
    
    Enable --> ClickApply[點擊申請按鈕]
    ClickApply --> MessagePrompt[彈出訊息輸入框]
    MessagePrompt --> EnterMessage{輸入訊息?}
    
    EnterMessage -->|跳過| Send[直接送出]
    EnterMessage -->|輸入| WriteMsg[撰寫申請訊息]
    WriteMsg --> Send
    
    Send --> Submitting[送出申請]
    Submitting --> Result{結果}
    
    Result -->|成功| SuccessToast[顯示成功訊息]
    Result -->|失敗| ErrorToast[顯示錯誤訊息]
    
    SuccessToast --> UpdateUI[更新按鈕狀態為待審核]
    UpdateUI --> Complete[流程完成]
\\\

**邊界案例與錯誤處理**：
- 活動已滿額  按鈕禁用，顯示「名額已滿」標籤
- 活動已取消  按鈕禁用，顯示「活動已取消」
- 重複申請  提示「您已申請此活動，請等待組織者審核」
- 組織者即為用戶本人  不顯示申請按鈕

---

### 3.4 審核參與者申請流程

**使用者目標**：審核並批准/拒絕參與者申請

**入口點**：活動詳情頁「待審核」徽章、活動管理頁面

**成功標準**：完成審核決定，申請者收到通知

\\\mermaid
graph TD
    Start[點擊待審核徽章] --> Dialog[開啟待審核對話框]
    Dialog --> List[顯示申請者列表]
    
    List --> ViewProfile{查看資料?}
    ViewProfile -->|是| OpenProfile[開啟申請者個人資料]
    OpenProfile --> CheckReview[查看評價與歷史]
    CheckReview --> Decision
    
    ViewProfile -->|否| Decision{做出決定}
    
    Decision -->|批准| ConfirmApprove[確認批准]
    Decision -->|拒絕| RejectPrompt[輸入拒絕理由可選]
    Decision -->|稍後處理| Close[關閉對話框]
    
    ConfirmApprove --> ApproveAPI[送出批准請求]
    RejectPrompt --> RejectAPI[送出拒絕請求]
    
    ApproveAPI --> ApproveResult{結果}
    RejectAPI --> RejectResult{結果}
    
    ApproveResult -->|成功| ApproveToast[顯示批准成功]
    ApproveResult -->|失敗| ErrorMsg[顯示錯誤]
    
    RejectResult -->|成功| RejectToast[顯示拒絕成功]
    RejectResult -->|失敗| ErrorMsg
    
    ApproveToast --> UpdateList[更新列表]
    RejectToast --> UpdateList
    ErrorMsg --> UpdateList
    
    UpdateList --> CheckMore{還有待審核?}
    CheckMore -->|是| List
    CheckMore -->|否| AllDone[顯示全部處理完成]
    AllDone --> Complete[流程完成]
\\\

**邊界案例與錯誤處理**：
- 活動已滿額但仍批准  警告「人數已達上限，確定要批准嗎？」
- 批准後自動開啟聊天室  顯示「已批准！您可以在聊天室與他們聯繫」
- 申請者已取消申請  顯示「此申請已被取消」
- 網路中斷  保留決定，待網路恢復後自動重試

---

### 3.5 即時聊天流程

**使用者目標**：與其他參與者或媒合對象即時溝通

**入口點**：聊天列表、活動詳情頁、用戶資料頁

**成功標準**：訊息成功發送並接收

\\\mermaid
graph TD
    Start[進入聊天頁面] --> LoadList[載入聊天列表]
    LoadList --> ShowList[顯示所有聊天室]
    
    ShowList --> Select[選擇聊天室]
    Select --> Connect[建立 Socket.IO 連線]
    
    Connect --> LoadHistory[載入歷史訊息]
    LoadHistory --> ShowChat[顯示聊天介面]
    
    ShowChat --> TypeMsg[輸入訊息]
    TypeMsg --> CheckContent{訊息內容?}
    
    CheckContent -->|空白| Disabled[發送按鈕禁用]
    CheckContent -->|有內容| Enabled[發送按鈕啟用]
    
    Enabled --> ClickSend[點擊發送]
    ClickSend --> SendMsg[透過 Socket 發送]
    
    SendMsg --> Sending[顯示發送中狀態]
    Sending --> Result{結果}
    
    Result -->|成功| ShowSent[訊息顯示為已發送]
    Result -->|失敗| ShowFailed[訊息顯示為失敗]
    
    ShowSent --> ClearInput[清空輸入框]
    ShowFailed --> Retry{重試?}
    
    Retry -->|是| SendMsg
    Retry -->|否| Keep[保留在輸入框]
    
    ClearInput --> Listen[監聽新訊息]
    Listen --> NewMsg{收到新訊息?}
    
    NewMsg -->|是| AppendMsg[附加到聊天記錄]
    NewMsg -->|否| Listen
    
    AppendMsg --> MarkRead[標記為已讀]
    MarkRead --> Continue[繼續聊天]
    Continue --> TypeMsg
\\\

**邊界案例與錯誤處理**：
- Socket 連線中斷  顯示「連線中斷，正在重新連線...」，自動重連
- 訊息發送失敗  訊息旁顯示紅色驚嘆號，提供重試按鈕
- 對方離線  顯示「對方目前離線」，訊息仍可發送
- 接收到新訊息時在其他頁面  導航欄徽章更新未讀數，發送桌面通知

---

## 4. 關鍵畫面設計 (Key Screen Layouts)

### 4.1 登入頁面 (Login)

**目的**：提供安全便捷的登入體驗

**關鍵元素**：
- Logo 與品牌標語（位於頂部中央）
- Email 輸入框（帶 Email 圖示）
- 密碼輸入框（帶眼睛圖示切換顯示/隱藏）
- 記住我勾選框
- 忘記密碼連結（位於密碼框右側）
- 登入按鈕（藍紫漸變，全寬）
- Google 登入按鈕（白色背景，Google 圖示）
- 註冊連結（底部：「還沒有帳號？立即註冊」）

**互動註釋**：
- 表單即時驗證，錯誤訊息顯示在輸入框下方
- 登入按鈕點擊後顯示 loading 動畫
- 成功登入後平滑過渡到控制台
- 玻璃擬態卡片居中顯示，背景為動態漸變

**響應式**：
- 桌面：卡片寬度 450px，居中
- 平板：卡片寬度 80%，最大 450px
- 手機：卡片寬度 95%，padding 縮小

---

### 4.2 控制台頁面 (Dashboard)

**目的**：提供個人化的活動概覽與快速操作

**關鍵元素**：
1. **歡迎卡片**
   - 問候語（依時間變化：早安/午安/晚安）
   - 用戶名稱
   - 驗證狀態徽章

2. **統計卡片（4 個並排）**
   - 我的活動數
   - 好友數量
   - 未讀訊息（紅色徽章）
   - 評價次數
   - 每個卡片有對應圖示與數字

3. **快速操作區**
   - 發布活動（主要按鈕）
   - 尋找旅伴（成功按鈕）
   - 查看訊息（資訊按鈕）
   - 編輯個人資料（警告按鈕）

4. **最近活動時間軸**（左側）
   - 顯示最近 5 個活動
   - 標題、地點、日期
   - 點擊跳轉到詳情

5. **最新好友列表**（右側）
   - 頭像、名稱、媒合狀態
   - 點擊開啟聊天

**互動註釋**：
- 統計數字使用動態計數動畫
- 快速操作按鈕有 hover 效果（上移 + 陰影）
- 空狀態顯示友善的插圖與引導文案

**響應式**：
- 桌面：統計卡片 4 欄，最近活動與好友 2 欄
- 平板：統計卡片 2 欄，最近活動與好友堆疊
- 手機：所有元素單欄堆疊

---

### 4.3 活動列表頁面 (Activities List)

**目的**：讓用戶瀏覽、搜尋、篩選活動

**關鍵元素**：
1. **頁面標題與操作**
   - 返回按鈕
   - 標題：「活動管理」
   - 創建新活動按鈕（藍紫漸變）

2. **搜尋與篩選卡片**
   - 搜尋框（帶搜尋圖示）
   - 類型下拉選單（登山/露營/旅遊/美食/其他）
   - 狀態下拉選單（招募中/已成團/已完成/已取消）

3. **標籤頁導航**
   - 我的所有活動
   - 我創建的活動
   - 我參加的活動
   - 探索活動

4. **活動卡片網格**
   - 封面圖（如果有）
   - 標題 + 狀態徽章
   - 創建者（如果是自己，顯示「創建者」標籤）
   - 地點圖示 + 地點
   - 日曆圖示 + 日期
   - 人數圖示 + 當前人數/上限
   - 描述摘要（2 行省略）
   - 操作按鈕（查看詳情/編輯/申請加入）

**互動註釋**：
- 卡片 hover 時上移並增強陰影
- 篩選與搜尋即時反應（前端過濾）
- 「待審核」顯示徽章數量
- 空狀態根據標籤頁顯示不同引導

**響應式**：
- 桌面：4 欄網格
- 平板：2 欄網格
- 手機：1 欄堆疊，卡片操作按鈕改為單欄堆疊

---

### 4.4 活動詳情頁面 (Activity Detail)

**目的**：展示活動完整資訊，提供互動功能

**關鍵元素**：
1. **頁首資訊**
   - 返回按鈕
   - 活動標題
   - 狀態徽章
   - 編輯按鈕（創建者可見）

2. **主要資訊卡片**
   - 封面圖（大圖展示）
   - 描述欄位
   - 詳細資訊表格：
     - 活動類型
     - 地點
     - 日期（開始/結束）
     - 參與人數
     - 創建者（可點擊查看資料）

3. **標籤頁內容**
   - **參與者**：頭像列表 + 名稱 + 角色標籤
   - **討論串**：即時訊息區（只有參與者可見）
   - **費用管理**：費用列表 + 結算報告
   - **相簿**：圖片網格展示
   - **評價**：完成後顯示，評價列表

4. **操作區（底部固定）**
   - 申請加入按鈕（探索模式）
   - 查看待審核按鈕（創建者）
   - 編輯活動按鈕（創建者）
   - 分享按鈕

**互動註釋**：
- 討論串支援即時訊息（Socket.IO）
- 費用管理有「新增費用」與「查看結算」按鈕
- 相簿支援上傳與預覽
- 評價只在活動完成後開放

**響應式**：
- 桌面：左右分欄（資訊 40% + 標籤頁 60%）
- 平板/手機：單欄堆疊，操作區固定在底部

---

### 4.5 聊天頁面 (Chat)

**目的**：提供即時訊息溝通介面

**關鍵元素**：
1. **聊天列表（左側）**
   - 搜尋框
   - 聊天室列表：
     - 對方頭像
     - 對方名稱
     - 最後訊息預覽
     - 時間戳記
     - 未讀徽章

2. **聊天視窗（右側）**
   - 標題欄：對方名稱 + 在線狀態
   - 訊息區域：
     - 訊息氣泡（左/右對齊）
     - 時間戳記
     - 已讀/未讀標記
     - 日期分隔線
   - 輸入區：
     - 文字輸入框
     - 表情符號按鈕
     - 圖片上傳按鈕
     - 發送按鈕

**互動註釋**：
- 新訊息自動滾動到底部
- 輸入中顯示「對方正在輸入...」
- 訊息發送失敗顯示紅色驚嘆號 + 重試按鈕
- Socket 斷線時顯示重連狀態

**響應式**：
- 桌面：左右分欄（列表 35% + 視窗 65%）
- 手機：只顯示聊天列表，點擊後全屏顯示聊天視窗

---

## 5. 組件庫與設計系統 (Component Library)

### 5.1 設計系統方法

EdgeSurvivor 使用 **Element Plus** 作為基礎 UI 組件庫，並在其之上建立自訂設計系統。

**核心原則**：
- 保持 Element Plus 的可訪問性與互動性
- 透過 CSS 變數系統化主題客製化
- 建立可重用的複合組件
- 確保設計一致性與開發效率

---

### 5.2 核心組件

#### 5.2.1 按鈕 (Button)

**用途**：觸發操作

**變體**：
- Primary（主要）：藍紫漸變，用於主要操作
- Success（成功）：綠色漸變，用於確認操作
- Warning（警告）：橙色，用於需注意的操作
- Danger（危險）：紅色，用於刪除等危險操作
- Info（資訊）：藍色，用於查看資訊
- Text（文字）：無背景，用於次要連結

**狀態**：
- Default（預設）
- Hover（懸停）：上移 2px + 陰影增強
- Active（按下）：下移回原位
- Disabled（禁用）：半透明 + 不可點擊
- Loading（載入中）：顯示旋轉圖示

**使用指南**：
- 每個頁面最多一個 Primary 按鈕
- 危險操作必須使用 Danger 類型並配合確認對話框
- Loading 狀態時禁用點擊

---

#### 5.2.2 卡片 (Card)

**用途**：內容容器

**變體**：
- Default（預設）：白色背景 + 柔和陰影
- Glass（玻璃）：半透明背景 + 模糊效果
- Hover（可懸停）：hover 時上移 + 陰影增強

**狀態**：
- Default
- Hover（活動卡片等可點擊卡片）
- Selected（選中狀態）

**使用指南**：
- 主要內容使用 Default 卡片
- 導航欄等覆蓋層使用 Glass 卡片
- 列表項目使用 Hover 卡片

---

#### 5.2.3 輸入框 (Input)

**用途**：文字輸入

**變體**：
- Text（文字）
- Password（密碼）：帶顯示/隱藏切換
- Textarea（多行文字）
- Number（數字）：帶增減按鈕
- Date（日期）：日期選擇器

**狀態**：
- Default
- Focus（聚焦）：藍紫光暈
- Error（錯誤）：紅色邊框 + 錯誤訊息
- Disabled（禁用）
- Success（成功）：綠色邊框（驗證通過）

**使用指南**：
- 必填欄位標示紅色星號
- 即時驗證，錯誤訊息顯示在下方
- Placeholder 提供範例或說明

---

#### 5.2.4 徽章 (Badge)

**用途**：顯示狀態或數量

**變體**：
- Dot（圓點）：小紅點
- Number（數字）：顯示數量，超過 99 顯示 99+
- Status（狀態）：不同顏色表示狀態

**狀態類型**：
- Success（成功）：綠色
- Warning（警告）：橙色
- Danger（危險）：紅色
- Info（資訊）：藍色

**使用指南**：
- 未讀訊息使用 Number 徽章
- 在線狀態使用 Dot 徽章
- 活動狀態使用 Status 徽章

---

#### 5.2.5 標籤 (Tag)

**用途**：分類或標記

**變體**：
- Default（預設）：灰色
- Primary（主要）：藍紫色
- Success（成功）：綠色
- Warning（警告）：橙色
- Danger（危險）：紅色
- Info（資訊）：藍色

**狀態**：
- Static（靜態）：不可關閉
- Closable（可關閉）：帶 X 按鈕

**使用指南**：
- 活動類型使用 Info Tag
- 活動狀態使用對應顏色 Tag
- 用戶角色使用 Success Tag（創建者）

---

## 6. 品牌與視覺風格 (Branding & Style Guide)

### 6.1 視覺識別

**品牌定位**：現代、友善、可信賴的旅伴媒合平台

**設計風格關鍵字**：
- 玻璃擬態 (Glassmorphism)
- 漸變色彩
- 柔和圓角
- 微動畫
- 清晰易讀

---

### 6.2 色彩系統

#### 主色調

| 顏色類型 | Hex 代碼 | 用途 | 範例 |
|---------|---------|------|------|
| Primary | #667eea | 主要品牌色、CTA 按鈕 | 登入按鈕、主導航高亮 |
| Primary Light | #818cf8 | Hover 狀態、輔助元素 | 按鈕 hover |
| Primary Dark | #5b63d3 | 按下狀態 | 按鈕 active |
| Secondary | #764ba2 | 次要品牌色、輔助元素 | 漸變終點色 |
| Secondary Light | #9d6cc1 | - | - |
| Secondary Dark | #5e3a7f | - | - |

#### 功能色

| 顏色類型 | Hex 代碼 | 用途 |
|---------|---------|------|
| Success | #10b981 | 成功狀態、批准操作 |
| Warning | #f59e0b | 警告狀態、需注意的操作 |
| Danger | #ef4444 | 錯誤狀態、刪除操作 |
| Info | #3b82f6 | 資訊提示、中性操作 |

#### 中性色

| 顏色類型 | Light Mode | Dark Mode | 用途 |
|---------|-----------|-----------|------|
| Text Primary | #1f2937 | #f9fafb | 主要文字 |
| Text Secondary | #6b7280 | #d1d5db | 次要文字 |
| Text Disabled | #9ca3af | #6b7280 | 禁用文字 |
| Border | #e5e7eb | #374151 | 邊框 |
| Divider | #f3f4f6 | #1f2937 | 分隔線 |
| Background Primary | #ffffff | #111827 | 主背景 |
| Background Secondary | #f9fafb | #1f2937 | 次背景 |
| Background Tertiary | #f3f4f6 | #374151 | 第三背景 |

#### 漸變色

| 漸變名稱 | CSS 值 | 用途 |
|---------|--------|------|
| Primary Gradient | linear-gradient(135deg, #667eea 0%, #764ba2 100%) | 主要按鈕、重要元素 |
| Success Gradient | linear-gradient(135deg, #4ade80 0%, #10b981 100%) | 成功按鈕 |
| Info Gradient | linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%) | 資訊按鈕 |

---

### 6.3 字體系統

#### 字體族

- **主要字體**：-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', 'Microsoft YaHei', '微软雅黑', sans-serif
- **等寬字體**：'Courier New', Courier, monospace（用於代碼或數字）

#### 字級系統

| 元素 | 大小 | 字重 | 行高 | 用途 |
|-----|------|------|------|------|
| H1 | 32px | 700 | 1.2 | 頁面主標題 |
| H2 | 24px | 600 | 1.3 | 區塊標題 |
| H3 | 20px | 600 | 1.4 | 子標題 |
| H4 | 18px | 600 | 1.4 | 卡片標題 |
| Body | 16px | 400 | 1.6 | 正文內容 |
| Small | 14px | 400 | 1.5 | 輔助資訊 |
| Caption | 12px | 400 | 1.4 | 標籤、時間戳記 |

**響應式調整**：
- 手機（< 640px）：整體縮小 2px
- 平板（641-1024px）：整體縮小 1px

---

### 6.4 圖示系統

**圖示庫**：Element Plus Icons

**使用指南**：
- 圖示尺寸：16px（small）、20px（medium）、24px（large）
- 圖示顏色：繼承文字顏色或使用主題色
- 帶文字時：圖示在左，間距 8px

**常用圖示**：
- User：用戶相關
- Calendar：日期時間
- Location：地點
- Chat：聊天訊息
- Plus：新增
- Search：搜尋
- Edit：編輯
- Delete：刪除

---

### 6.5 間距與佈局

#### 間距系統

| 名稱 | 值 | 用途 |
|-----|---|------|
| xs | 4px | 極小間距 |
| sm | 8px | 小間距 |
| md | 16px | 中等間距（預設） |
| lg | 24px | 大間距 |
| xl | 32px | 極大間距 |
| 2xl | 48px | 超大間距（區塊間） |

#### 圓角系統

| 名稱 | 值 | 用途 |
|-----|---|------|
| sm | 4px | 小元素（Tag） |
| md | 8px | 按鈕、輸入框 |
| lg | 12px | 卡片 |
| xl | 16px | 大卡片 |
| 2xl | 24px | 對話框 |
| full | 9999px | 圓形（Avatar、Badge） |

#### 陰影系統

| 名稱 | CSS 值 | 用途 |
|-----|--------|------|
| sm |   1px 2px 0 rgba(0, 0, 0, 0.05) | 輕微立體感 |
| md |   4px 6px -1px rgba(0, 0, 0, 0.1) | 卡片預設 |
| lg |   10px 15px -3px rgba(0, 0, 0, 0.1) | Hover 狀態 |
| xl |   20px 25px -5px rgba(0, 0, 0, 0.1) | 對話框 |
| 2xl |   25px 50px -12px rgba(0, 0, 0, 0.25) | 最高層級 |

---

## 7. 無障礙性 (Accessibility)

### 7.1 目標標準

**合規目標**：WCAG 2.1 Level AA

### 7.2 關鍵要求

#### 視覺

- **色彩對比**：文字與背景對比度至少 4.5:1（正文）、3:1（大字）
- **焦點指示器**：所有可互動元素需有明顯的焦點框（藍紫色光暈）
- **文字大小**：支援瀏覽器文字縮放至 200%

#### 互動

- **鍵盤導航**：所有功能可透過鍵盤操作（Tab、Enter、Esc）
- **螢幕閱讀器**：使用語意化 HTML 與 ARIA 屬性
- **觸控目標**：最小 44x44px（符合 WCAG 2.1 AAA）

#### 內容

- **替代文字**：所有圖片提供 alt 描述
- **標題結構**：遵循 H1-H6 層級結構
- **表單標籤**：所有輸入框有對應 label

### 7.3 測試策略

- **自動化測試**：使用 axe-core 或 Lighthouse
- **鍵盤測試**：確保 Tab 順序合理，無鍵盤陷阱
- **螢幕閱讀器測試**：使用 NVDA（Windows）或 VoiceOver（macOS）
- **對比度檢查**：使用瀏覽器開發工具或 Contrast Checker

---

## 8. 響應式設計 (Responsive Design)

### 8.1 斷點系統

| 斷點名稱 | 最小寬度 | 最大寬度 | 目標裝置 |
|---------|---------|---------|---------|
| Mobile | - | 640px | 智慧型手機 |
| Tablet | 641px | 1024px | 平板電腦 |
| Desktop | 1025px | 1440px | 桌上型電腦 |
| Wide | 1441px | - | 大螢幕 |

### 8.2 調整策略

#### 佈局變化

- **Mobile**：單欄堆疊，隱藏次要資訊，底部導航
- **Tablet**：2 欄網格，部分元素折疊
- **Desktop**：3-4 欄網格，側邊導航，完整功能
- **Wide**：最大寬度限制（1200px），內容居中

#### 導航變化

- **Mobile**：漢堡選單 + 底部 Tab Bar
- **Tablet**：頂部水平選單，部分項目折疊
- **Desktop**：完整頂部選單

#### 內容優先級

**Mobile 隱藏/簡化**：
- 次要統計資訊
- 詳細描述（折疊顯示）
- 側邊欄內容

**保留核心**：
- 主要操作按鈕
- 關鍵資訊（標題、日期、地點）
- 導航

#### 互動變化

- **Touch**：增大點擊區域（44x44px），支援滑動手勢
- **Mouse**：顯示 Hover 效果，支援右鍵選單
- **Keyboard**：顯示焦點指示器，支援快捷鍵

---

## 9. 動畫與微互動 (Animation & Micro-interactions)

### 9.1 動畫原則

1. **有目的性**：動畫應強化理解，而非干擾
2. **快速流暢**：持續時間 150-350ms
3. **自然緩動**：使用 ease-out 或 cubic-bezier
4. **可關閉**：尊重使用者偏好設定（prefers-reduced-motion）

### 9.2 關鍵動畫

| 動畫名稱 | 持續時間 | 緩動函數 | 用途 |
|---------|---------|---------|------|
| fadeIn | 250ms | ease-out | 內容淡入 |
| slideInUp | 250ms | ease-out | 從下滑入 |
| slideInDown | 250ms | ease-out | 從上滑入 |
| slideInLeft | 250ms | ease-out | 從左滑入 |
| slideInRight | 250ms | ease-out | 從右滑入 |
| scaleIn | 250ms | ease-out | 縮放進入 |
| pulse | 2s | ease-in-out | 脈衝動畫（徽章） |
| rotate | 1s | linear | 旋轉動畫（Loading） |
| bounce | 0.6s | cubic-bezier | 彈跳動畫（強調） |
| shake | 0.5s | ease-in-out | 搖晃動畫（錯誤） |

### 9.3 微互動範例

- **按鈕點擊**：上移 2px（150ms）  按下回彈（100ms）
- **卡片懸停**：上移 4px + 陰影增強（250ms）
- **輸入聚焦**：藍紫光暈淡入（200ms）
- **Toast 通知**：從頂部滑下（300ms）  停留 3s  淡出（300ms）
- **Loading**：旋轉動畫 + 脈衝效果
- **新訊息**：輕微彈跳 + 聲音提示（可選）
- **頁面切換**：淡出舊頁（200ms）  淡入新頁（200ms）

---

## 10. 效能考量 (Performance Considerations)

### 10.1 效能目標

| 指標 | 目標值 | 測量方式 |
|-----|-------|---------|
| 首次內容繪製 (FCP) | < 1.5s | Lighthouse |
| 最大內容繪製 (LCP) | < 2.5s | Lighthouse |
| 首次輸入延遲 (FID) | < 100ms | Lighthouse |
| 累積版面配置位移 (CLS) | < 0.1 | Lighthouse |
| 頁面載入時間 | < 3s | DevTools Network |

### 10.2 設計策略

#### 圖片優化

- 使用 WebP 格式（降級 JPEG/PNG）
- 響應式圖片（srcset）
- 延遲載入（Lazy Loading）
- 圖片壓縮（TinyPNG、ImageOptim）
- 封面圖：最大 800x600px
- 頭像：最大 200x200px

#### 程式碼優化

- 路由懶載入（Vue Router Lazy Loading）
- 組件按需載入
- Tree Shaking（移除未使用程式碼）
- 壓縮與醜化（Production Build）

#### 渲染優化

- 骨架屏（Skeleton Screen）替代 Loading Spinner
- 虛擬滾動（長列表）
- 防抖與節流（搜尋、滾動事件）
- CSS 動畫優先於 JS 動畫

#### 快取策略

- Service Worker（PWA 快取）
- LocalStorage（用戶偏好、草稿）
- API 回應快取（適當的 Cache-Control）

---

## 11. 後續步驟 (Next Steps)

### 11.1 立即行動

1. ** 檢閱此規格文檔**  
   與產品經理、開發團隊確認需求與可行性

2. ** 建立高保真設計稿**  
   使用 Figma 或 Sketch 建立詳細的視覺設計稿

3. ** 建立組件庫**  
   在 Storybook 中建立可重用的 UI 組件

4. ** 進行可用性測試**  
   邀請 5-8 位目標用戶進行測試，收集反饋

### 11.2 設計交接清單

- [x] 所有使用者流程已文檔化
- [x] 組件清單完整
- [x] 無障礙性要求已定義
- [x] 響應式策略清晰
- [x] 品牌指南已整合
- [x] 效能目標已建立
- [ ] Figma 設計稿已建立（待辦）
- [ ] 組件庫已建立（待辦）
- [ ] 可用性測試已完成（待辦）

### 11.3 給前端開發者的提示

請前端開發者檢閱此 UI/UX 規格，並確保：

1. **技術實現與設計一致**  
   - 使用 Vue 3 Composition API
   - 整合 Element Plus 並客製化主題
   - 實現玻璃擬態效果與漸變

2. **遵循無障礙性規範**  
   - 語意化 HTML
   - ARIA 屬性
   - 鍵盤導航

3. **優化效能**  
   - 圖片延遲載入
   - 路由懶載入
   - 骨架屏

4. **響應式實現**  
   - Mobile-First 方法
   - 使用 CSS Grid/Flexbox
   - 測試多種裝置

---

## 附錄 A：參考資源

### 設計工具

- **Figma**：https://figma.com - 協作式設計工具
- **Storybook**：https://storybook.js.org - UI 組件開發環境
- **ColorHexa**：https://www.colorhexa.com - 色彩工具

### 無障礙性

- **WCAG 2.1**：https://www.w3.org/WAI/WCAG21/quickref/
- **A11y Project**：https://www.a11yproject.com
- **WebAIM Contrast Checker**：https://webaim.org/resources/contrastchecker/

### 技術文檔

- **Vue 3**：https://vuejs.org
- **Element Plus**：https://element-plus.org
- **Socket.IO**：https://socket.io

---

**文檔結尾**

此 UI/UX 規格文檔由 UX Expert (Sally) 建立，作為 EdgeSurvivor 前端開發的設計指南。如有任何問題或建議，請聯繫專案團隊。

*最後更新：2025-11-03*
