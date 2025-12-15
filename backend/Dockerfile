FROM python:3.12
#Debian
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
# 使用 Gunicorn + gevent worker 支援 Socket.IO 和高併發（極限配置）
# workers=12: 大幅提高並發處理能力
# worker-connections=2000: 每個 worker 可處理 2000 個併發連接
# timeout=180: 增加超時時間應對慢請求
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "12", "--worker-class", "gevent", "--worker-connections", "2000", "--timeout", "180", "--backlog", "2048", "app:app"]