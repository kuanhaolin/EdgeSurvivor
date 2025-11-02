import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to_email, subject, html_content):
    """發送電子郵件"""
    try:
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        from_email = os.getenv('SMTP_FROM_EMAIL', smtp_username)
        from_name = os.getenv('SMTP_FROM_NAME', 'EdgeSurvivor')
        
        if not smtp_username or not smtp_password:
            print("警告: 郵件服務未配置")
            return False
        
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = f'{from_name} <{from_email}>'
        message['To'] = to_email
        
        html_part = MIMEText(html_content, 'html', 'utf-8')
        message.attach(html_part)
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        
        print(f"郵件已發送到: {to_email}")
        return True
        
    except Exception as e:
        print(f"發送郵件失敗: {str(e)}")
        return False

def send_reset_password_email(to_email, code):
    """發送重設密碼郵件"""
    subject = "EdgeSurvivor - 重設密碼驗證碼"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; padding: 30px; color: white;">
            <h1 style="margin: 0;">🔐 EdgeSurvivor</h1>
            <p>重設密碼</p>
        </div>
        <div style="background: white; border-radius: 8px; padding: 30px; margin-top: 20px;">
            <h2 style="color: #667eea;">重設密碼驗證碼</h2>
            <p>您好，您請求重設密碼。請使用以下驗證碼：</p>
            <div style="font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 8px; text-align: center; padding: 20px; background: #f5f7fa; border-radius: 8px; margin: 20px 0;">
                {code}
            </div>
            <p><strong>此驗證碼將在 15 分鐘後失效。</strong></p>
            <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; margin: 20px 0;">
                ⚠️ 如果您沒有請求重設密碼，請忽略此郵件。
            </div>
        </div>
    </body>
    </html>
    """
    return send_email(to_email, subject, html_content)

def send_welcome_email(to_email, user_name):
    """發送歡迎郵件"""
    subject = "歡迎加入 EdgeSurvivor！"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; padding: 30px; color: white;">
            <h1>🎉 歡迎加入 EdgeSurvivor！</h1>
        </div>
        <div style="background: white; border-radius: 8px; padding: 30px; margin-top: 20px;">
            <h2 style="color: #667eea;">嗨，{user_name}！</h2>
            <p>感謝您註冊 EdgeSurvivor，一個專為邊緣人打造的旅伴交友平台。</p>
            <p><strong>您現在可以：</strong></p>
            <ul>
                <li>建立和參加旅遊活動</li>
                <li>尋找志同道合的旅伴</li>
                <li>即時聊天交流</li>
            </ul>
        </div>
    </body>
    </html>
    """
    return send_email(to_email, subject, html_content)
