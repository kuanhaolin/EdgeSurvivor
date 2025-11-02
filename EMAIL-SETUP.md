# 郵件服務配置指南

EdgeSurvivor 使用 SMTP 協議發送郵件（如重設密碼驗證碼、歡迎郵件等）。

## 配置方式

在 `.env.docker` 文件中設置以下環境變數：

```bash
SMTP_SERVER=smtp.gmail.com          # SMTP 服務器地址
SMTP_PORT=587                       # SMTP 端口
SMTP_USERNAME=your_email@gmail.com # 發件郵箱
SMTP_PASSWORD=your_app_password    # 郵箱密碼或應用程式密碼
SMTP_FROM_EMAIL=your_email@gmail.com # 發件人郵箱（可選，預設使用 SMTP_USERNAME）
SMTP_FROM_NAME=EdgeSurvivor        # 發件人名稱（可選）
```

## 使用 Gmail 發送郵件

### 方法 1: 使用應用程式密碼（推薦）

1. **啟用兩步驟驗證**
   - 前往 [Google 帳戶安全性](https://myaccount.google.com/security)
   - 啟用「兩步驟驗證」

2. **生成應用程式密碼**
   - 前往 [應用程式密碼](https://myaccount.google.com/apppasswords)
   - 選擇「郵件」和「其他（自訂名稱）」
   - 輸入名稱（例如：EdgeSurvivor）
   - 複製生成的 16 位密碼

3. **配置 .env.docker**
   ```bash
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=abcd efgh ijkl mnop  # 使用應用程式密碼
   ```

### 方法 2: 允許低安全性應用程式存取（不推薦）

⚠️ **不建議使用**，因為安全性較低

1. 前往 [低安全性應用程式存取](https://myaccount.google.com/lesssecureapps)
2. 啟用「允許低安全性應用程式存取」
3. 使用您的 Gmail 密碼作為 `SMTP_PASSWORD`

## 使用其他郵件服務

### Outlook / Hotmail

```bash
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your_email@outlook.com
SMTP_PASSWORD=your_password
```

### Yahoo Mail

```bash
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your_email@yahoo.com
SMTP_PASSWORD=your_app_password  # 需要生成應用程式密碼
```

### SendGrid（推薦用於生產環境）

1. 註冊 [SendGrid](https://sendgrid.com/) 帳號
2. 創建 API Key
3. 配置：

```bash
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your_sendgrid_api_key
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

### AWS SES（適合大量發送）

```bash
SMTP_SERVER=email-smtp.us-east-1.amazonaws.com
SMTP_PORT=587
SMTP_USERNAME=your_aws_smtp_username
SMTP_PASSWORD=your_aws_smtp_password
```

## 測試模式

如果未配置郵件服務，系統會自動進入測試模式：

- 開發環境下，驗證碼會直接在 API 回應中返回
- 後端控制台會輸出驗證碼
- 不會真實發送郵件

## 重啟服務

修改環境變數後，需要重啟 Docker 服務：

```bash
docker-compose restart backend
```

## 測試郵件發送

1. 訪問 http://localhost:8080/forgot-password
2. 輸入已註冊的電子郵件
3. 檢查收件匣（包括垃圾郵件資料夾）
4. 輸入收到的驗證碼

## 故障排除

### 郵件未收到

1. **檢查垃圾郵件資料夾**
2. **檢查後端日誌**
   ```bash
   docker-compose logs backend
   ```
3. **驗證配置**
   - SMTP 服務器地址是否正確
   - 端口是否正確（通常是 587）
   - 用戶名和密碼是否正確

### Gmail 錯誤：535 Authentication failed

- 確認已啟用兩步驟驗證
- 使用應用程式密碼，不是 Gmail 密碼
- 檢查應用程式密碼是否包含空格（需要移除）

### 連接超時

- 檢查防火牆設置
- 確認 Docker 容器可以訪問外部網路
- 嘗試使用不同的 SMTP 端口（如 465）

## 郵件模板

目前實作的郵件模板：

1. **重設密碼驗證碼** (`send_reset_password_email`)
   - 包含 6 位數驗證碼
   - 15 分鐘有效期提醒
   - 安全警告

2. **歡迎郵件** (`send_welcome_email`)
   - 註冊成功後發送
   - 包含平台功能介紹

可以在 `backend/utils/email.py` 中自訂郵件模板。

## 安全建議

1. ⚠️ **不要將真實的郵件密碼提交到 Git**
2. ✅ 使用環境變數存儲敏感資訊
3. ✅ 使用應用程式密碼而非帳號密碼
4. ✅ 生產環境使用專業郵件服務（SendGrid、AWS SES）
5. ✅ 定期更換 SMTP 密碼

## 進階配置

### 使用 SSL (端口 465)

修改 `backend/utils/email.py` 中的連接方式：

```python
# 使用 SMTP_SSL 而非 SMTP + starttls()
with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
    server.login(smtp_username, smtp_password)
    server.send_message(message)
```

### 自訂郵件模板

編輯 `backend/utils/email.py` 中的 HTML 模板，修改樣式、內容和結構。
