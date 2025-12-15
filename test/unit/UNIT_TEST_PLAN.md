# 單元測試規劃 (Unit Test Plan)

根據 USE_CASES.md 的 26 個功能，規劃對應的單元測試

---

## 測試概覽

- **總 Use Cases:** 26 個
- **Epic 1 (使用者管理):** 9 個
- **Epic 2 (活動管理):** 6 個
- **Epic 3 (社交功能):** 4 個
- **Epic 4 (活動參與):** 7 個

---

## Epic 1: 身份與帳戶管理

### TC_1.1 註冊

**測試檔案:** `./frontend/test/TC_1.1.js`  `./backend/test/TC_1_1.py`

**測試案例:**

* [ ] 1.1.1 用戶欄位驗證
  測試檔案: `./frontend/test/TC_1.1.1.js`  `./backend/test/TC_1_1_1.py`
  測試方式：Vitest/Pytest
  測試說明：應該要求用戶名必填，且長度需符合2到20個字元
  測試資料：1:false, 0:false, 000000000000000000000:false, user01:true, user02: true
  結果：PASSED
* [ ] 1.1.2 信箱欄位驗證
  測試檔案:  `./frontend/test/TC_1.1.2.js`  `./backend/test/TC_1_1_2.py`
  測試方式：Vitest/Pytest
  測試說明：應該要求信箱必填，且需符合正確格式
  測試資料：test@test:false, testtest.com:false, test @test.com:false, test@test.com:true, test@gmail.com:true
  結果：PASSED
* [ ] 1.1.3 密碼欄位驗證
  測試檔案: `./frontend/test/TC_1.1.3.js`  `./backend/test/TC_1_1_3.py`
  測試方式：Vitest/Pytest
  測試說明：應該要求密碼必填，且長度只少需6個字元
  測試資料：1:false, 123:false, 123456:true, 000000:true, password: true
  結果：PASSED
* [ ] 1.1.4 確認密碼欄位驗證
  測試檔案: `./frontend/test/TC_1.1.4.js`
  測試方式：Vitest
  測試說明：應該要求確認密碼必填，且需與密碼欄位相同，假設密碼為123456
  測試資料：012345:false, 111111:false, 123456:true
  結果：PASSED
* [ ] 1.1.5 重複信箱註冊失敗
  測試檔案: `./backend/test/TC_1_1_5.py`
  測試方式：Pytest
  測試說明：輸入已存在的 Email 註冊, 假設已存在:test@test.com
  測試資料：test01@test.com:true, test@test02.com:true, test@test.com:false
  結果：PASSED
* [ ] 1.1.6 成功註冊
  測試檔案:   `./backend/test/TC_1_1_6.py`
  測試方式：Pytest
  測試說明：輸入所有必填資訊且符合格式
  測試資料：user01, user01@user01.com, 111111, 111111
  結果：PASSED
* [ ] 1.1.7 密碼加密
  測試檔案:   `./backend/test/TC_1_1_7.py`
  測試方式：Pytest
  測試說明：密碼存入後端必須加密，驗證密碼不是明文
  測試資料：123456:true, 000000:true
  結果：PASSED

### TC_1.2 Email 登入

**測試檔案:** `./frontend/test/TC_1.2.js` `./backend/test/TC_1_2.py`

**測試案例:**

* [ ] 1.2.1 信箱格式轉換
  測試檔案: `./backend/test/TC_1_1_1.py`
  測試方式: Pytest
  測試說明: Email 轉換為小寫處理
  測試資料: test@test.com, TEST@test.com, Test@Test.COM
  結果: PASSED
* [ ] 1.2.2 信箱欄位必填
  測試檔案:  `./frontend/test/TC_1.1.2.js`  `./backend/test/TC_1_1_2.py`
  測試方式：Vitest/Pytest
  測試說明：應該要求信箱必填
  測試資料：test@test.com:true, test@gmail.com:true, ' ':false
  結果：PASSED
* [ ] 1.2.3 密碼欄位必填
  測試檔案:  `./frontend/test/TC_1.1.3.js`  `./backend/test/TC_1_1_3.py`
  測試方式：Vitest/Pytest
  測試說明：應該要求密碼必填，前端會驗證密碼需6個字元
  測試資料：前端-123:false, 123456:true, 000000:true | 後端-" ":false, 123456:true, 000000:true
  結果：PASSED
* [ ] 1.2.4 信箱登入驗證
  測試檔案:  `./backend/test/TC_1_2_4.py`
  測試方式: Pytest
  測試說明: 應為已註冊信箱，假設已建立test@test.com
  測試資料: test@test.com:true, user01@user01.com:false, user02@user02.com:false
* [ ] 1.2.5 密碼登入驗證
  測試檔案:  `./backend/test/TC_1_2_5.py`
  測試方式: Pytest
  測試說明: 應為已註冊信箱與密碼且需經過加密比對，假設已建立test@test.com密碼為123456
  測試資料: 000000:false, 123123:false, 123456:true
  結果：PASSED
* [ ] 1.2.6 帳號使否有啟用2FA驗證
  測試檔案: `./backend/test/TC_1_2_6.py`
  測試方式: Pytest
  測試說明: 應為啟用2FA驗證，假設test@test.com已啟用, user01@user01.com未啟用
  測試資料: test@test.com:true, user01@user01.com:false
  結果：PASSED
* [ ] 1.2.7 JWT Token 正確生成
  測試檔案: `./backend/test/TC_1_2_7.py`
  測試方式: Pytest
  測試說明: 登入成功後應該返回access_token和refresh_token，驗證token都不為空，假設test@test.com已註冊
  測試資料: test@test.com, true, user01@user01.com:false
  結果: PASSED

---

### TC_1.3 2FA驗證

**測試檔案:** `./frontend/test/TC_1.3.js` `./backend/test/TC_1_3.py`

**測試案例:**

* [ ] 1.3.1 啟用 2FA
  測試檔案: `./backend/test/TC_1_3_1.py`
  測試方式: Pytest
  測試說明: 驗證2FA的setup是否能成功驗證
  測試資料: pyotp.TOTP(secret).now()
  結果: PASSED
* [ ] 1.3.2 登入需2FA
  測試檔案: `./backend/test/TC_1_3_2.py`
  測試方式: Pytest
  測試說明: 測試登入驗證是否成功，因未啟用2FA帳號無此步驟，所以只測試成功啟用帳號
  備註: 前端已在1.2測試
  測試資料: user01@user01.com:True
  結果: PASSED
* [ ] 1.3.3 驗證碼驗證
  測試檔案: `./backend/test/TC_1_3_3.py`
  測試方式: Pytest
  測試說明: 測試驗證碼是否成功，假設123456為驗證碼，測試會自動將這個資料自動生成實際的驗證碼並驗證
  測試資料: 123456:true, 000000:false
  結果: PASSED
* [ ] 1.3.4 停用 2FA
  測試檔案: `./backend/test/TC_1_3_4.py`
  測試方式: Pytest
  測試說明: 測試帳戶從啟用轉為停用，並驗證是否已停用
  測試資料: user1@test.com
  結果: PASSED
* [ ] 1.3.5 驗證碼欄位驗證
  測試檔案: `./frontend/test/TC_1.3.5.js`
  測試方式: Vitest
  測試說明: 測試驗證欄位是否成功
  測試資料: 123456:true, " ":false, "123":false
  結果: PASSED

---

### TC_1.4 Google 登入

**測試檔案:** `./backend/test/TC_1_4.py`

**測試案例:**

* [ ] 1.4.1 Google Token 驗證
  測試檔案: `./backend/test/TC_1_4_1.py`
  測試方式: Pytest
  測試說明: 測試回傳成功和失敗時，後端的反應是否正確，透過Mock隨機給一段內容驗證成功，失敗則是給空資料驗證
  測試資料: "valid_google_code": true, " ":false
  結果: PASSED
* [ ] 1.4.2 驗證是否建立帳號
  測試檔案: `./backend/test/TC_1_4_2.py`
  測試方式: Pytest
  測試說明: 第一次用Google登入應該自動建立帳號，如已登入過則不需在建立帳號，後續可跳過其他流程，測試user01@user01.com已存在
  測試資料: user01@user01.com:true, user02@user02.com:false
  結果: PASSED
* [ ] 1.4.3 驗證登入流程
  測試檔案: `./backend/test/TC_1_4_3.py`
  測試方式: Pytest
  測試說明: 第一次用Google登入應該自動建立帳號，第二次則可直接登入，測試同一帳號的重複登入流程
  測試資料: user@user.com
  結果: PASSED
* [ ] 1.4.4 登入返回 JWT Token
  測試檔案: `./backend/test/TC_1_4_4.py`
  測試方式: Pytest
  測試說明: 測試Google登入成功後應該返回JWT token
  測試資料: user@user.com
  結果: PASSED

---

### TC_1.5 忘記/變更密碼

**測試檔案:** `./frontend/test/TC_1.5.js` `./backend/test/TC_1_5.py`

**測試案例:**

* [ ] 1.5.1 驗證 Email 欄位
  測試檔案: `./frontend/test/TC_1.5.1.js` `./backend/test/TC_1_5_1.py`
  測試方式: Vitest/Pytest
  測試說明: 測試email欄位是否正確
  測試資料: " ":false, "123@":false, "user@user.com":true
  結果: PASSED
* [ ] 1.5.2 發送重設密碼 Email
  測試檔案: `./backend/test/TC_1_5_1.py`
  測試方式: Pytest
  測試說明: 測試發送驗證碼信件，使用開發模式直接返回驗證碼，測試驗證碼是否返回
  測試資料: user@user.com
  結果: PASSED
* [ ] 1.5.3 驗證驗證碼欄位
  測試檔案: `./frontend/test/TC_1.5.3.js` `./backend/test/TC_1_5_3.py`
  測試方式: Vitest/Pytest
  測試說明: 前端測試欄位格式，後端只測試驗證是否有值
  測試資料:  前端-" ": false, "123": false, "123456":true | 後端-" ": false, "123456":true
  結果: PASSED
* [ ] 1.5.4 新密碼欄位驗證
  測試檔案: `./frontend/test/TC_1.5.4.js` `./backend/test/TC_1_5_4.py`
  測試方式: Vitest/Pytest
  測試說明: 測試新密碼欄位是否正確
  測試資料: " ": false, "123": false, "123456":true
  結果: PASSED
* [ ] 1.5.5 確認新密碼欄位驗證
  測試檔案: `./frontend/test/TC_1.5.5.js`
  測試方式: Vitest
  測試說明: 測試確認新密碼欄位是否正確且需與新密碼相同
  測試資料: " ": false, "123":false, "123456":true
  結果: PASSED
* [ ] 1.5.6 重設密碼成功
  測試檔案: `./backend/test/TC_1_5_6.py`
  測試方式: Pytest
  測試說明: 測試根據驗證碼與新密碼重設密碼成功，並測試能否登入
  測試資料: newpassword
  結果: PASSED
* [ ] 1.5.7 刪除已使用驗證碼
  測試檔案: `./backend/test/TC_1_5_7.py`
  測試方式: Pytest
  測試說明: 測試已使用的驗證碼是否被刪除
  測試資料: 000000
  結果: PASSED
* [ ] 1.5.8 已登入使用者變更密碼舊密碼欄位驗證
  測試檔案: `./frontend/test/TC_1.5.8.js` `./backend/test/TC_1_5_8.py`
  測試方式: Vitest/Pytest
  測試說明: 測試登入狀態下變更密碼，舊密碼欄位驗證
  測試資料: " ":false, fakepassword:false, oldpassword:true
  結果: PASSED
* [ ] 1.5.9 已登入使用者變更密碼新密碼欄位驗證
  測試檔案: `./frontend/test/TC_1.5.9.js` `./backend/test/TC_1_5_9.py`
  測試方式: Vitest/Pytest
  測試說明: 測試登入狀態下變更密碼，新密碼欄位驗證
  測試資料: " ":false, 123:false, 123456:true
  結果: PASSED
* [ ] 1.5.10 已登入使用者變更密碼確認密碼欄位驗證
  測試檔案: `./frontend/test/TC_1.5.10.js`
  測試方式: Vitest
  測試說明: 測試登入狀態下變更密碼，確認新密碼必須與新密碼相同，假設新密碼為123456
  測試資料: ' ':false, '654321':false, '123456':true
  結果: PASSED
* [ ] 1.5.11 已登入使用者變更密碼成功
  測試檔案: `./backend/test/TC_1_5_11.py`
  測試方式: Pytest
  測試說明: 測試已登入使用者變JWT更密碼
  測試資料: oldpassword, newpassword
  結果: PASSED
* [ ] 1.5.12 更新 JWT Token
  測試檔案: `./backend/test/TC_1_5_12.py`
  測試方式: Pytest
  測試說明: 測試更新密碼後，更新JWT token，並且新與舊不能相同
  測試資料: oldpassword, newpassword
  結果: PASSED

---

### TC_1.6 Email 驗證

**測試檔案:** `./backend/test/TC_1_6.py`

**測試案例:**

* [ ] 1.6.1 SMTP 連線測試
  測試檔案: `./backend/test/TC_1_6_1.py`
  測試方式: Pytest
  測試說明: 測試能否連接SMTP伺服器
  測試資料:
  結果: PASSED
* [ ] 1.6.2 驗證 Email 格式測試
  測試檔案: `./backend/test/TC_1_6_2.py`
  測試方式: Pytest
  測試說明: 測試HTML內容生成
  測試資料:
  結果: PASSED
* [ ] 1.6.3 重設密碼郵件測試
  測試檔案: `./backend/test/TC_1_6_3.py`
  測試方式: Pytest
  測試說明: 測試驗證碼插入與完整性正確
  測試資料:
  結果: PASSED

---

### TC_1.7 刪除帳號

**測試檔案:** `./backend/test/TC_1_7.py`

**測試案例:**

* [ ] 1.7.1 刪除帳號需要密碼確認
  測試檔案: `./backend/test/TC_1_7_1.py`
  測試方式: Pytest
  測試說明: 測試刪除帳號必須正確密碼，假設密碼為123456
  測試資料: 654321:false, 123456:true
  結果: PASSED
* [ ] 1.7.2 成功刪除帳號
  測試檔案: `./backend/test/TC_1_7_2.py`
  測試方式: Pytest
  測試說明: 測試成功刪除自己的帳號，驗證能否登入
  測試資料:
  結果: PASSED
* [ ] 1.7.3 級聯刪除相關資料
  測試檔案: `./backend/test/TC_1_7_3.py`
  測試方式: Pytest
  測試說明: 刪除帳號應該清除相關資料
  測試資料:
  結果: PASSED

---

### TC_1.8 管理個人資料

**測試檔案:** `./frontend/test/TC_1.8.js` `./backend/test/TC_1_8.py`

**測試案例:**

* [ ] 1.8.1 更新姓名
  測試檔案: `./backend/test/TC_1_8_1.py`
  測試方式: Pytest
  測試說明: 測試更新姓名，驗證是否更新資訊
  測試資料: user01
  結果: PASSED
* [ ] 1.8.2 更新性別
  測試檔案: `./backend/test/TC_1_8_2.py`
  測試方式: Pytest
  測試說明: 測試更新姓名，以選單進行，驗證是否更新資訊
  測試資料: 男性
  結果: PASSED
* [ ] 1.8.3 更新年齡
  測試檔案: `./backend/test/TC_1_8_3.py`
  測試方式: Pytest
  測試說明: 測試更新年齡，驗證是否更新資訊
  測試資料: 18
  結果: PASSED
* [ ] 1.8.4 更新地區
  測試檔案: `./backend/test/TC_1_8_4.py`
  測試方式: Pytest
  測試說明: 測試更新地區，以選單進行，驗證是否更新資訊
  測試資料: 台灣
  結果: PASSED
* [ ] 1.8.5 更新隱私設定
  測試檔案: `./backend/test/TC_1_8_5.py`
  測試方式: Pytest
  測試說明: 測試更新隱私設定，驗證社群資訊是否依要求可見
  測試資料:
  結果: PASSED
* [ ] 1.8.6 隱私所有人可見
  測試檔案: `./backend/test/TC_1_8_6.py`
  測試方式: Pytest
  測試說明: 測試更新隱私設定，驗證社群資訊是否所有人可見
  測試資料:
  結果: PASSED
* [ ] 1.8.7 隱私僅好友可見
  測試檔案: `./backend/test/TC_1_8_7.py`
  測試方式: Pytest
  測試說明: 測試更新隱私設定，驗證社群資訊是否僅好友求可見
  測試資料: PASSED
* [ ] 1.8.8 更新大頭照
  測試檔案: `./frontend/test/TC_1.8.8.js` `./backend/test/TC_1_8_8.py`
  測試方式: Vitest/Pytest
  測試說明: 測試上傳照片，驗證是否更新
  測試資料: 前端-over2mb.jpg:false, paper.pdf:false, 1.5mb.jpg:true | 後端-photo.jpg
  結果: PASSED
* [ ] 1.8.9 未登入無法更新資料
  測試檔案: `./backend/test/TC_1_8_9.py`
  測試方式: Pytest
  測試說明: 測試更新條件，未登入無法透過api進行更新，使用未登入帳號更新姓名
  測試資料: user01
  結果: PASSED
* [ ] 1.8.10 無效 token 無法更新資料
  測試檔案: `./backend/test/TC_1_8_10.py`
  測試方式: Pytest
  測試說明: 測試更新條件，無效token無法透過api進行更新，更新姓名
  測試資料: user01
  結果: PASSED

---

### TC_1.9 連結社群帳號

**測試檔案:**  `./frontend/test/TC_1.9.js` `./backend/test/TC_1_9.py`

**測試案例:**

* [ ] 1.9.1 連結 Instagram
  測試檔案: `./backend/test/TC_1_9_1.py`
  測試方式: Pytest
  測試說明: 連結https://instagram.com/your_username帳號，測試是否能成功生成icon與連結
  測試資料: https://instagram.com/user01
  結果: PASSED
* [ ] 1.9.2 連結 Facebook
  測試檔案: `./backend/test/TC_1_9_2.py`
  測試方式: Pytest
  測試說明: 連結https://facebook.com/your_profile帳號，測試是否能成功生成icon與連結
  測試資料: https://facebook.com/user01
  結果: PASSED
* [ ] 1.9.3 連結 LINE
  測試檔案: `./frontend/test/TC_1.9.3.js` `./backend/test/TC_1_9_3.py`
  測試方式: Vitest/Pytest
  測試說明: 連結line_id，測試是否能成功生成icon與qrcode
  測試資料: user01
  結果: PASSED
* [ ] 1.9.4 連結 Twitter (X)
  測試檔案: `./backend/test/TC_1_9_4.py`
  測試方式: Pytest
  測試說明: 連結https://twitter.com/your_username帳號，測試是否能成功生成icon與連結
  測試資料: https://twitter.com/user01
  結果: PASSED
* [ ] 1.9.5 顯示連結
  測試檔案: `./frontend/test/TC_1.9.5.js`
  測試方式: Vitest
  測試說明: 測試社群帳號是否能顯示
  測試資料: "https://instagram.com/user01", " ", "user01", " ":true, " ", " ", " ", " ":false
  結果: PASSED

---

## Epic 2: 活動建立與管理

### TC_2.1 建立活動

**測試檔案:** `./frontend/test/TC_2.1.js` `./backend/test/TC_2_1.py`

**測試案例:**

* [ ] 2.1.1 活動欄位必填驗證
  測試檔案: `./frontend/test/TC_2.1.1.js` `./backend/test/TC_2_1_2.py`
  測試方式: Vitest/Pytest
  測試說明: 測試欄位必填測試，包含五項
  測試資料: "期末考", "其他", "中央大學", "2025/12/10", "2025/12/10", "", "5", "":true, "放寒假", "", "", "", "", "", "", "":false, "開學", "其他", "", "", "", "", "", "":false,
  結果: PASSED
* [ ] 2.1.2 時間驗證
  測試檔案: `./frontend/test/TC_2.1.2.js`  `./backend/test/TC_2_1_2.py`
  測試方式: Vitest/Pytest
  測試說明: 測試開始時間必須早於結束時間
  測試資料: "2025/01/01", "2025/01/02":true, "2026/01/01", "2025/01/01":false
  結果: PASSED
* [ ] 2.1.3 未登入無法建立
  測試檔案: `./backend/test/TC_2_1_3.py`
  測試方式: Pytest
  測試說明: 測未登入狀態無法建立活動
  測試資料:
  結果: PASSED
* [ ] 2.1.4 建立者自動成為參與者
  測試檔案: `./backend/test/TC_2_1_4.py`
  測試方式: Pytest
  測試說明: 測試建立活動後創建者自動新增為參與者
  測試資料: user
  結果: PASSED

---

### TC_2.2 管理活動

**測試檔案:** `./frontend/test/TC_2.2.js` `./backend/test/TC_2_2.py`

**測試案例:**

* [ ] 2.2.1 創建者可以編輯活動
  測試檔案: `./backend/test/TC_2_2_1.py`
  測試方式: Pytest
  測試說明: 測試活動創建者能編輯活動，其餘則無法
  測試資料:
  結果: PASSED
* [ ] 2.2.2 創建者更新活動資訊
  測試檔案: `./backend/test/TC_2_2_2.py`
  測試方式: Pytest
  測試說明: 測試活動創建者能更新活動資訊
  測試資料:
  結果: PASSED
* [ ] 2.2.3 更新活動資訊欄位驗證
  測試檔案: `./frontend/test/TC_2.2.3.js` `./backend/test/TC_2_2_3.py`
  測試方式: Vitest/Pytest
  測試說明: 測試使用有效資料更新活動
  測試資料:
  結果: PASSED
* [ ] 2.2.4 更新活動資訊部分其他欄位不變
  測試檔案: `./backend/test/TC_2_2_4.py`
  測試方式: Pytest
  測試說明: 測試部分欄位更新，其他欄位不變
  測試資料:
  結果: PASSED
* [ ] 2.2.5 更新活動資其他必填欄位保持有效
  測試檔案: `./backend/test/TC_2_2_5.py`
  測試方式: Pytest
  測試說明: 測試更新時必填欄位保持有效
  測試資料:
  結果: PASSED
* [ ] 2.2.6 刪除所有相關記錄
  測試檔案: `./backend/test/TC_2_2_6.py`
  測試方式: Pytest
  測試說明: 測試刪除活動前，需刪除所有活動紀錄
  測試資料:
  結果: PASSED
* [ ] 2.2.7 刪除活動
  測試檔案: `./backend/test/TC_2_2_7.py`
  測試方式: Pytest
  測試說明: 測試活動創建者能刪除活動，非創建者與未存在的無法刪除
  測試資料:
  結果: PASSED

---

### TC_2.3 審核活動申請

**測試檔案:** `./frontend/test/TC_2.3.js` `./backend/test/TC_2_3.py`

**測試案例:**

* [ ] 2.3.1 待審核申請管理
  測試檔案: `./frontend/test/TC_2.3.1.js` `./backend/test/TC_2_3_1.py`
  測試方式: Vitest/Pytest
  測試說明: 測試創建者查看所有待審核申請，驗證創建者是否能查看
  測試資料:
  結果: PASSED
* [ ] 2.3.2 批准申請
  測試檔案: `./backend/test/TC_2_3_2.py`
  測試方式: Pytest
  測試說明: 測試批准申請並加入參與者名單
  測試資料:
  結果: PASSED
* [ ] 2.3.3 拒絕申請
  測試檔案: `./backend/test/TC_2_3_3.py`
  測試方式: Pytest
  測試說明: 測試拒絕申請
  測試資料:
  結果: PASSED
* [ ] 2.3.4 審核後移除申請名單
  測試檔案: `./backend/test/TC_2_3_4.py`
  測試方式: Pytest
  測試說明: 測試審核後移除申請名單
  測試資料:
  結果: PASSED
* [ ] 2.3.5 批准後人數增加
  測試檔案: `./backend/test/TC_2_3_5.py`
  測試方式: Pytest
  測試說明: 測試驗證人數變化，批准後活動參與人數+1
  測試資料:
  結果: PASSED
* [ ] 2.3.6 達到人數上限自動拒絕
  測試檔案: `./backend/test/TC_2_3_6.py`
  測試方式: Pytest
  測試說明: 測試人數已滿時自動拒絕新申請
  測試資料:
  結果: PASSED
* [ ] 2.3.7 非創建者無法審核
  測試檔案: `./backend/test/TC_2_3_7.py`
  測試方式: Pytest
  測試說明: 測試非創建者無法審核申請
  測試資料:
  結果: PASSED

---

### TC_2.4 移除參與者

**測試檔案:** `./frontend/test/TC_2.4.js` `./backend/test/TC_2_4.py`

**測試案例:**

* [ ] 2.4.1 創建者移除參與者
  測試檔案: `./frontend/test/TC_2.4.1.js` `./backend/test/TC_2_4_1.py`
  測試方式: Pytest
  測試說明: 測試創建者可以移除參與者
  測試資料:
  結果: PASSED
* [ ] 2.4.2 移除後更新參與者人數
  測試檔案: `./backend/test/TC_2_4_2.py`
  測試方式: Pytest
  測試說明: 測試移除後更新參與者人數
  測試資料:
  結果: PASSED
* [ ] 2.4.3 創建者無法移除自己
  測試檔案: `./backend/test/TC_2_4_3.py`
  測試方式: Pytest
  測試說明: 測試創建者移除自己是否成功
  測試資料:
  結果: PASSED
* [ ] 2.4.4 非創建者無法移除他人
  測試檔案: `./backend/test/TC_2_4_4.py`
  測試方式: Pytest
  測試說明: 測試一般參與者移除其他人是否成功
  測試資料:
  結果: PASSED

---

### TC_2.5 控制討論區訊息

**測試檔案:** `./frontend/test/TC_2.5.js` `./backend/test/TC_2_5.py`

**測試案例:**

* [ ] 2.5.1 創建者刪除任何訊息
  測試檔案: `./frontend/test/TC_2.5.1.js`  `./backend/test/TC_2_5_1.py`
  測試方式: Vitest/Pytest
  測試說明: 測試創建者可以刪除任何活動討論訊息
  測試資料:
  結果: PASSED

---

### TC_2.6 分攤費用管理

**測試檔案:** `./frontend/test/TC_2.6.js` `./backend/test/TC_2_6.py`

**測試案例:**

* [ ] 2.6.1 創建者刪除任何費用項目
  測試檔案: `./frontend/test/TC_2.5.1.js`  `./backend/test/TC_2_6_1.py`
  測試方式: Vitest/Pytest
  測試說明: 測試創建者可以刪除任何費用項目
  測試資料:
  結果: PASSED
* [ ] 2.6.2 刪除後重新計算分攤
  測試檔案: `./backend/test/TC_2_6_2.py`
  測試方式: Pytest
  測試說明: 測試刪除費用後重新計算每人應付
  測試資料:
  結果: PASSED

---

## Epic 3: 互動與交友

### TC_3.1 好友瀏覽與篩選

**測試檔案:** `./frontend/test/TC_3.1.js` `./backend/test/TC_3_1.py`

**測試案例:**

* [ ] 3.1.1 依性別搜尋
  測試檔案: `./frontend/test/TC_3.1.1.js`
  測試方式: Vitest
  測試說明: 測試篩選性別條件
  測試資料:
  結果: PASSED
* [ ] 3.1.2 依年齡範圍篩選
  測試檔案: `./frontend/test/TC_3.1.2.js`
  測試方式: Vitest
  測試說明: 測試篩選年齡範圍條件
  測試資料:
  結果: PASSED
* [ ] 3.1.3 依地區篩選
  測試檔案: `./frontend/test/TC_3.1.3.js`
  測試方式: Vitest
  測試說明: 測試篩選地區條件
  測試資料:
  結果: PASSED
* [ ] 3.1.4 依興趣篩選
  測試檔案: `./frontend/test/TC_3.1.4.js`
  測試方式: Vitest
  測試說明: 測試篩選興趣條件
  測試資料:
  結果: PASSED
* [ ] 3.1.5 重置篩選
  測試檔案: `./frontend/test/TC_3.1.4.js`
  測試方式: Vitest
  測試說明: 測試重置篩選條件
  測試資料:
  結果: PASSED
* [ ] 3.1.6 查看用戶資料
  測試檔案: `./frontend/test/TC_3.1.6.js` `./backend/test/TC_3_1_6.py`
  測試方式: Vitest/Pytest
  測試說明: 測試是否顯示用戶資料
  測試資料:
  結果: PASSED
* [ ] 3.1.7 用戶最小資料驗證
  測試檔案: `./frontend/test/TC_3.1.7.js`
  測試方式: Vitest
  測試說明: 測試系統處理最小必要資料的能力
  測試資料:
  結果: PASSED
* [ ] 3.1.8 排除交友名單
  測試檔案: `./backend/test/TC_3_1_8.py`
  測試方式: Pytest
  測試說明: 測試交友配對關係都會被排除在名單，只會有未配對與已拒絕用戶
  測試資料:
  結果: PASSED

---

### TC_3.2 申請好友

**測試檔案:** `./frontend/test/TC_3.2.js` `./backend/test/TC_3_2.py`

**測試案例:**

* [ ] 3.2.1 驗證請求好友狀態
  測試檔案: `./frontend/test/TC_3.2.1.js` `./backend/test/TC_3_2_1.py`
  測試方式: Vitest/Pytest
  測試說明: 測試請求狀態，已發送未被回應的或好友不能再次請求
  測試資料:
  結果: PASSED
* [ ] 3.2.2 發送好友請求
  測試檔案: `./frontend/test/TC_3.2.2.js` `./backend/test/TC_3_2_2.py`
  測試方式: Vitest/Pytest
  測試說明: 測試發送好友請求
  測試資料:
  結果: PASSED
* [ ] 3.2.3 取消好友邀請
  測試檔案: `./frontend/test/TC_3.2.3.js` `./backend/test/TC_3_2_3.py`
  測試方式: Vitest/Pytest
  測試說明: 測試取消已發送的請求
  測試資料:
  結果: PASSED
* [ ] 3.2.4 更新交友名單
  測試檔案: `./backend/test/TC_3_2_4.py`
  測試方式: Pytest
  測試說明: 測試交友名單的更新邏輯，已請求和配對都不在名單上，被拒絕則會重新顯示在交友名單
  測試資料:
  結果: PASSED
* [ ] 3.2.5 查看已發送狀態
  測試檔案: `./frontend/test/TC_3.2.5.js` `./backend/test/TC_3_2_5.py`
  測試方式: Vitest/Pytest
  測試說明: 測試自己發送的所有請求狀態紀錄
  測試資料:
  結果: PASSED
* [ ] 3.2.6 更新已發送狀態
  測試檔案: `./frontend/test/TC_3.2.6.js` `./backend/test/TC_3_2_6.py`
  測試方式: Vitest/Pytest
  測試說明: 測試已發送名單的更新邏輯，如果操作取消不會留存紀錄
  測試資料:
  結果: PASSED

---

### TC_3.3 審核好友申請

**測試檔案:** `./frontend/test/TC_3.3.js` `./backend/test/TC_3_3.py`

**測試案例:**

* [ ] 3.3.1 查看待審核邀請
  測試檔案: `./frontend/test/TC_3.3.1.js` `./backend/test/TC_3_3_1.py`
  測試方式: Vitest/Pytest
  測試說明: 測試查看收到的好友請求名單
  測試資料:
  結果: PASSED
* [ ] 3.3.2 驗證用戶審核狀態
  測試檔案: `./backend/test/TC_3_3_2.py`
  測試方式: Pytest
  測試說明: 測試好友請求狀態
  測試資料:
  結果: PASSED
* [ ] 3.3.3 批准好友請求
  測試檔案: `./frontend/test/TC_3.3.3.js` `./backend/test/TC_3_3_3.py`
  測試方式: Vitest/Pytest
  測試說明: 測試批准好友請求
  測試資料:
  結果: PASSED
* [ ] 3.3.4 拒絕好友請求
  測試檔案: `./frontend/test/TC_3.3.4.js` `./backend/test/TC_3_3_4.py`
  測試方式: Vitest/Pytest
  測試說明: 測試拒絕好友邀請
  測試資料:
  結果: PASSED
* [ ] 3.3.5 建立雙向好友關係
  測試檔案: `./backend/test/TC_3_3_5.py`
  測試方式: Pytest
  測試說明: 測試批准後建立雙向好友關係
  測試資料:
  結果: PASSED
* [ ] 3.3.6 更新審核名單
  測試檔案: `./backend/test/TC_3_3_6.py`
  測試方式: Pytest
  測試說明: 測試更新審核名單
  測試資料:
  結果: PASSED
* [ ] 3.3.7 更新好友名單
  測試檔案: `./backend/test/TC_3_3_7.py`
  測試方式: Pytest
  測試說明: 測試更新好友名單
  測試資料:
  結果: PASSED

---

### TC_3.4 私訊/傳訊息

**測試檔案:** `./frontend/test/TC_3.4.js` `./backend/test/TC_3_4.py`

**測試案例:**

* [ ] 3.4.1 發送訊息給用戶
  測試檔案: `./frontend/test/TC_3.4.1.js` `./backend/test/TC_3_4_1.py`
  測試方式: Vitest/Pytest
  測試說明: 測試發送訊息給任何用戶是否成功
  測試資料:
  結果: PASSED
* [ ] 3.4.2 驗證訊息未讀狀態
  測試檔案: `./frontend/test/TC_3.4.2.js` `./backend/test/TC_3_4_2.py`
  測試方式: Vitest/Pytest
  測試說明: 測試未讀訊息數
  測試資料:
  結果: PASSED
* [ ] 3.4.3 即時訊息傳遞
  測試檔案: `./backend/test/TC_3_4_3.py`
  測試方式: Pytest
  測試說明: 測試WebSocket即時傳遞訊息
  測試資料:
  結果:
* [ ] 3.4.4 更新聊天室
  測試檔案: `./frontend/test/TC_3.4.4.js` `./backend/test/TC_3_4_4.py`
  測試方式: Vitest/Pytest
  測試說明: 測試訊息是否會在介面同步更新
  測試資料:
  結果: PASSED
* [ ] 3.4.5 刪除訊息
  測試檔案: `./frontend/test/TC_3.4.5.js` `./backend/test/TC_3_4_5.py`
  測試方式: Vitest/Pytest
  測試說明: 測試刪除自己發送的訊息是否可以被刪除
  測試資料:
  結果: PASSED

---

### TC_3.5 刪除好友

**測試檔案:** `./frontend/test/TC_3.5.js` `./backend/test/TC_3_5.py`

* [ ] 3.5.1 驗證好友狀態
  測試檔案: `./backend/test/TC_3_5_1.py`
  測試方式: Pytest
  測試說明: 測試使否為好友狀態
  測試資料:
  結果: PASSED
* [ ] 3.5.2 刪除好友
  測試檔案: `./frontend/test/TC_3.5.2.js` `./backend/test/TC_3_5_2.py`
  測試方式: Vitest//Pytest
  測試說明: 測試刪除好友是否成功
  測試資料:
  結果: PASSED
* [ ] 3.5.3 更新好友名單
  測試檔案: `./backend/test/TC_3_5_3.py`
  測試方式: Pytest
  測試說明: 測試刪除的好友是否還在名單
  測試資料:
  結果: PASSED

---

## Epic 4: 活動參與與互動

### TC_4.1 活動瀏覽與篩選

**測試檔案:** `./frontend/test/TC_4.1.js` `./backend/test/TC_4_1.py`

* [ ] 4.1.1 查看我的所有活動
  測試檔案: `./frontend/test/TC_4.1.1.js` `./backend/test/TC_4_1_1.py`
  測試方式: Vitest/Pytest
  測試說明: 測試我的所有活動清單
  測試資料:
  結果: PASSED
* [ ] 4.1.2 查看我創建的活動
  測試檔案: `./frontend/test/TC_4.1.2.js` `./backend/test/TC_4_1_2.py`
  測試方式: Vitest/Pytest
  測試說明: 測試我創建的活動清單
  測試資料:
  結果: PASSED
* [ ] 4.1.3 查看我參加的活動
  測試檔案: `./frontend/test/TC_4.1.3.js` `./backend/test/TC_4_1_3.py`
  測試方式: Vitest/Pytest
  測試說明: 測試我參加的活動清單
  測試資料:
  結果: PASSED
* [ ] 4.1.4 查看探索活動
  測試檔案: `./frontend/test/TC_4.1.4.js` `./backend/test/TC_4_1_4.py`
  測試方式: Vitest/Pytest
  測試說明: 測試探索活動清單
  測試資料:
  結果: PASSED
* [ ] 4.1.5 依活動關鍵字篩選
  測試檔案: `./frontend/test/TC_4.1.5.js`
  測試方式: Vitest
  測試說明: 測試關鍵字篩選
  測試資料:
  結果: PASSED
* [ ] 4.1.6 依活動類型篩選
  測試檔案: `./frontend/test/TC_4.1.6.js`
  測試方式: Vitest
  測試說明: 測試類型篩選
  測試資料:
  結果: PASSED
* [ ] 4.1.7 依活動狀態篩選
  測試檔案: `./frontend/test/TC_4.1.7.js`
  測試方式: Vitest
  測試說明: 測試狀態篩選
  測試資料:
  結果: PASSED

### TC_4.2 申請活動

**測試檔案:** `./frontend/test/TC_4.2.js` `./backend/test/TC_4_2.py`

**測試案例:**

* [ ] 4.2.1 驗證活動狀態
  測試檔案: `./backend/test/TC_4_2_1.py`
  測試方式: Pytest
  測試說明: 測試是否活動狀態為未參與活動與人數未滿
  測試資料:
  結果:
* [ ] 4.2.2 申請活動
  測試檔案: `./frontend/test/TC_4.2.2.js` `./backend/test/TC_4_2_2.py`
  測試方式: Vitest/Pytest
  測試說明: 測試申請活動
  測試資料: 
  結果: PASSED
* [ ] 4.2.3 驗證申請狀態
  測試檔案: `./backend/test/TC_4_2_3.py`
  測試方式: Pytest
  測試說明: 測試活動聲請狀態
  測試資料:
  結果: PASSED
* [ ] 4.2.4 更新探索活動清單
  測試檔案: `./backend/test/TC_4_2_4.py`
  測試方式: Pytest
  測試說明: 測試更新探索活動清單
  測試資料:
  結果: PASSED
* [ ] 4.2.5 更新我的活動清單
  測試檔案: `./backend/test/TC_4_2_5.py`
  測試方式: Pytest
  測試說明: 測試我的活動清單
  測試資料:
  結果: PASSED

---

### TC_4.3 互評

**測試檔案:** `./frontend/test/TC_4.3.js` `./backend/test/TC_4_3.py`

**測試案例:**

* [ ] 4.3.1 活動狀態驗證
  測試檔案: `./backend/test/TC_4_3_1.py`
  測試方式: Pytest
  測試說明: 測試活動結束和標示已完成狀態
  測試資料:
  結果: PASSED
* [ ] 4.3.2 驗證互評評分
  測試檔案: `./frontend/test/TC_4.3.2.js` `./backend/test/TC_4_3_2.py`
  測試方式: Vitest/Pytest
  測試說明: 測試互評評分，必填
  測試資料:
  結果: PASSED
* [ ] 4.3.3 更新評價者平均分數
  測試檔案: `./backend/test/TC_4_3_3.py`
  測試方式: Pytest
  測試說明: 測試評價者平均分數
  測試資料:
  結果: PASSED
* [ ] 4.3.4 驗證評價內容
  測試檔案: `./frontend/test/TC_4.3.4.js` `./backend/test/TC_4_3_4.py`
  測試方式: Vitest/Pytest
  測試說明: 測試評價者評價內容，必填
  測試資料:
  結果: PASSED
* [ ] 4.3.5 更新評價者評論
  測試檔案: `./backend/test/TC_4_3_5.py`
  測試方式: Pytest
  測試說明: 測試評價者評論
  測試資料:
  結果: PASSED

---

### TC_4.4 新增分攤費用

**測試檔案:** `./frontend/test/TC_4.4.js` `./backend/test/TC_4_4.py`

**測試案例:**

* [ ] 4.4.1 費用項目欄位驗證
  測試檔案: `./frontend/test/TC_4.4.1.js` `./backend/test/TC_4_4_1.py`
  測試方式: Vitest/Pytest
  測試說明: 測試費用項目欄位驗證
  測試資料:
  結果: PASSED
* [ ] 4.4.2 費用金額欄位驗證
  測試檔案: `./frontend/test/TC_4.4.2.js` `./backend/test/TC_4_4_2.py`
  測試方式: Vitest/Pytest
  測試說明: 測試金額欄位驗證
  測試資料:
  結果: PASSED
* [ ] 4.4.3 費用類別欄位驗證
  測試檔案: `./frontend/test/TC_4.4.3.js` `./backend/test/TC_4_4_3.py`
  測試方式: Vitest/Pytest
  測試說明: 測試類別欄位驗證
  測試資料:
  結果: PASSED
* [ ] 4.4.4 費用代墊人欄位驗證
  測試檔案: `./frontend/test/TC_4.4.4.js` `./backend/test/TC_4_4_4.py`
  測試方式: Vitest/Pytest
  測試說明: 測試代墊人欄位驗證
  測試資料:
  結果: PASSED
* [ ] 4.4.5 分攤方式欄位驗證
  測試檔案: `./frontend/test/TC_4.4.5.js` `./backend/test/TC_4_4_5.py`
  測試方式: Vitest/Pytest
  測試說明: 測試分攤方式欄位驗證
  測試資料:
  結果: PASSED
* [ ] 4.4.6 分攤參與者欄位驗證
  測試檔案: `./frontend/test/TC_4.4.6.js` `./backend/test/TC_4_4_6.py`
  測試方式: Pytest
  測試說明: 測試分攤參與者欄位驗證
  測試資料:
  結果: PASSED
* [ ] 4.4.7 驗證用戶狀態
  測試檔案: `./backend/test/TC_4_4_7.py`
  測試方式: Pytest
  測試說明: 測試用戶是否為活動參與者
  測試資料:
  結果: PASSED
* [ ] 4.4.8 費用新增
  測試檔案: `./backend/test/TC_4_4_8.py`
  測試方式: Pytest
  測試說明: 測試用戶是否成功新增費用
  測試資料:
  結果: PASSED
* [ ] 4.4.9 更新費用清單
  測試檔案: `./backend/test/TC_4_4_9.py`
  測試方式: Pytest
  測試說明: 測試費用清單使否正確
  測試資料:
  結果: PASSED

---

### TC_4.5 分攤費用

**測試檔案:** `./backend/test/TC_4_5.py`

**測試案例:**

* [ ] 4.5.1 結算計算邏輯
  測試檔案: `./backend/test/TC_4_5_1.py`
  測試方式: Pytest
  測試說明: 測試全體平攤的結算計算，包含所有分攤項目
  測試資料:
  結果: PASSED
* [ ] 4.5.2 算法優化轉帳次數
  測試檔案: `./backend/test/TC_4_5_5.py`
  測試方式: Pytest
  測試說明: 測試多人情況下驗證轉帳次數最少
  測試資料:
  結果: PASSED
* [ ] 4.5.3 驗證用戶狀態
  測試檔案: `./backend/test/TC_4_5_3.py`
  測試方式: Pytest
  測試說明: 測試用戶是否為活動參與者
  測試資料:
  結果: PASSED
* [ ] 4.5.4 驗證費用的編輯權
  測試檔案: `./backend/test/TC_4_5_3.py`
  測試方式: Pytest
  測試說明: 測試費用明細的編輯權，驗證自己新增的資訊
  測試資料:
  結果: PASSED
* [ ] 4.5.5 刪除費用
  測試檔案: `./backend/test/TC_4_5_5.py`
  測試方式: Pytest
  測試說明: 測試用戶是否成功刪除費用
  測試資料:
  結果: PASSED
* [ ] 4.5.6 更新費用明細清單
  測試檔案: `./backend/test/TC_4_5_6.py`
  測試方式: Pytest
  測試說明: 測試費用明細清單是否正確
  測試資料:
  結果: PASSED

---

### TC_4.6 上傳照片

**測試檔案:** `./frontend/test/TC_4.6.js` `./backend/test/TC_4_6.py`

**測試案例:**

* [ ] 4.6.1 驗證用戶狀態
  測試檔案: `./backend/test/TC_4_5_1.py`
  測試方式: Pytest
  測試說明: 測試用戶是否為活動參與者
  測試資料:
  結果: PASSED
* [ ] 4.6.2 驗證檔案格式規範
  測試檔案: `./frontend/test/TC_4.6.2.js` `./backend/test/TC_4_6_2.py`
  測試方式: Vitest/Pytest
  測試說明: 測試檔案大小、格式與類型
  測試資料:
  結果: PASSED
* [ ] 4.6.3 上傳照片
  測試檔案: `./backend/test/TC_4_6_3.py`
  測試方式: Pytest
  測試說明: 測試檔案是否上傳成功
  測試資料:
  結果: PASSED
* [ ] 4.6.4 更新活動相簿
  測試檔案: `./backend/test/TC_4_6_4.py`
  測試方式: Pytest
  測試說明: 測試活動相簿的照片是否正確
  測試資料:
  結果: PASSED
* [ ] 4.6.5 驗證照片狀況
  測試檔案: `./backend/test/TC_4_6_5.py`
  測試方式: Pytest
  測試說明: 測試照片URL正確存入資料庫
  測試資料:
  結果: PASSED

### TC_4.7 活動討論區留言

**測試檔案:** `./frontend/test/TC_4.7.js` `./backend/test/TC_4_7.py`

**測試案例:**

* [ ] 4.7.1 驗證用戶狀態
  測試檔案: `./backend/test/TC_4_7_1.py`
  測試方式: Pytest
  測試說明: 測試用戶是否為活動參與者
  測試資料:
  結果: PASSED
* [ ] 4.7.2 參與者發送留言
  測試檔案: `./frontend/test/TC_4.7.2js` `./backend/test/TC_4_7_2.py`
  測試方式: Vitest/Pytest
  測試說明: 測試參與者是否成功發布留言
  測試資料:
  結果: PASSED
* [ ] 4.7.3 討論區訊息即時同步
  測試檔案: `./backend/test/TC_4_7_3.py`
  測試方式: Pytest
  測試說明: 測試WebSocket即時傳遞留言
  測試資料:
  結果: PASSED
* [ ] 4.7.4 刪除自己的留言
  測試檔案: `./frontend/test/TC_4.7.4.js` `./backend/test/TC_4_7_4.py`
  測試方式: Vitest/Pytest
  測試說明: 測試刪除自己的留言
  測試資料:
  結果: PASSED
* [ ] 4.7.5 更新討論區
  測試檔案: `./frontend/test/TC_4.7.5.js` `./backend/test/TC_4_7_5.py`
  測試方式: Vitest/Pytest
  測試說明: 測試訊息是否會在介面同步更新
  測試資料:
  結果: PASSED
