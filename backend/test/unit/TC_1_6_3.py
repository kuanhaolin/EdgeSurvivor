"""
TC 1.6.3 - 重設密碼郵件測試
測試說明: 測試驗證碼插入與完整性正確
"""

import pytest
from unittest.mock import patch, MagicMock
from utils.email import send_reset_password_email

def test_reset_password_email():
    """測試重設密碼郵件（驗證碼插入、主旨、模板完整性、收件人）"""
    
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        test_code = '123456'
        test_email = 'test@example.com'
        
        result = send_reset_password_email(
            to_email=test_email,
            code=test_code
        )
        
        # 驗證郵件發送
        assert result == True, "郵件應該成功發送"
        assert mock_server.send_message.called, "應該呼叫 send_message"
        
        # 取得發送的訊息
        call_args = mock_server.send_message.call_args
        message = call_args[0][0]
        
        # 驗證主旨
        assert 'EdgeSurvivor' in message['Subject'], "主旨應該包含 EdgeSurvivor"
        assert '重設密碼' in message['Subject'], "主旨應該包含重設密碼"
        
        # 驗證收件人
        assert message['To'] == test_email, f"收件人應該是 {test_email}"
        
        # 取得 HTML 內容
        html_content = None
        for part in message.walk():
            if part.get_content_type() == 'text/html':
                html_content = part.get_payload(decode=True).decode('utf-8')
                break
        
        # 驗證驗證碼與模板完整性
        assert test_code in html_content, f"HTML 內容應該包含驗證碼 {test_code}"
        assert '<!DOCTYPE html>' in html_content, "應該有 DOCTYPE"
        assert '<html>' in html_content, "應該有 html 標籤"
        assert '15 分鐘' in html_content, "應該提示有效期限"
        assert '🔐' in html_content or 'EdgeSurvivor' in html_content, "應該有品牌標識"
    
    # 測試不同驗證碼
    test_codes = ['000000', '999999', '654321']
    for code in test_codes:
        with patch('smtplib.SMTP') as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            send_reset_password_email(
                to_email='test@example.com',
                code=code
            )
            
            call_args = mock_server.send_message.call_args
            message = call_args[0][0]
            
            html_content = None
            for part in message.walk():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True).decode('utf-8')
                    break
            
            assert code in html_content, f"應該包含驗證碼 {code}"
