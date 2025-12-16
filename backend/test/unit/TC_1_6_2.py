"""
TC 1.6.2 - Email 格式測試
測試說明: 測試HTML內容生成
"""

import pytest
from unittest.mock import patch, MagicMock, call
from utils.email import send_email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_format():
    """測試 Email 格式（HTML、UTF-8、From header、multipart）"""
    
    # 測試 HTML 格式
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        html_content = '<html><body><h1>Test</h1><p>Content</p></body></html>'
        send_email(
            to_email='test@example.com',
            subject='Test Subject',
            html_content=html_content
        )
        
        call_args = mock_server.send_message.call_args
        message = call_args[0][0]
        
        assert message['Subject'] == 'Test Subject', "Subject 應該正確"
        assert message['To'] == 'test@example.com', "收件人應該正確"
        assert 'From' in message, "應該有寄件人"
        assert message.is_multipart(), "應該是 multipart 訊息"
    
    # 測試 UTF-8 編碼
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(
            to_email='test@example.com',
            subject='測試主旨',
            html_content='<html><body><p>測試中文內容</p></body></html>'
        )
        assert result == True, "應該成功發送"
    
    # 測試 From header 格式
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        with patch.dict('os.environ', {
            'SMTP_FROM_NAME': 'EdgeSurvivor',
            'SMTP_FROM_EMAIL': 'noreply@edgesurvivor.com',
            'SMTP_USERNAME': 'test',
            'SMTP_PASSWORD': 'test'
        }, clear=False):
            send_email(
                to_email='test@example.com',
                subject='Test',
                html_content='<p>Test</p>'
            )
            
            call_args = mock_server.send_message.call_args
            message = call_args[0][0]
            assert 'EdgeSurvivor' in message['From'], "From header 應該包含名稱"
            assert 'noreply@edgesurvivor.com' in message['From'], "From header 應該包含 email"
