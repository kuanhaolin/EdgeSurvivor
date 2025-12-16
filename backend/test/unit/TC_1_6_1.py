"""
TC 1.6.1 - SMTP 連線測試
測試說明: 測試能否連接SMTP伺服器
"""

import pytest
from unittest.mock import patch, MagicMock
from utils.email import send_email
import smtplib

def test_smtp_connection():
    """測試 SMTP 連線、認證與錯誤處理"""
    
    # 測試成功連線
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(
            to_email='test@example.com',
            subject='Test Subject',
            html_content='<p>Test Content</p>'
        )
        
        # 驗證連線流程
        assert mock_server.starttls.called, "應該呼叫 starttls"
        assert mock_server.login.called, "應該呼叫 login"
        assert mock_server.send_message.called, "應該呼叫 send_message"
    
    # 測試無認證資訊
    with patch.dict('os.environ', {
        'SMTP_USERNAME': '',
        'SMTP_PASSWORD': ''
    }, clear=False):
        result = send_email(
            to_email='test@example.com',
            subject='Test',
            html_content='<p>Test</p>'
        )
        assert result == False, "無認證資訊應該返回 False"
    
    # 測試認證失敗
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, b'Authentication failed')
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(
            to_email='test@example.com',
            subject='Test',
            html_content='<p>Test</p>'
        )
        assert result == False, "認證失敗應該返回 False"
