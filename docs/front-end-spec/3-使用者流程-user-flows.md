# 3. 使用者流程 (User Flows)

## 3.1 新用戶註冊流程

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

## 3.2 發布活動流程

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

## 3.3 申請加入活動流程

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

## 3.4 審核參與者申請流程

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

## 3.5 即時聊天流程

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
