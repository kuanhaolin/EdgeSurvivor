FROM python:3.12
#Debian
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
# 使用 Gunicorn + eventlet worker 支援 Socket.IO
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--worker-class", "eventlet", "--worker-connections", "1000", "--timeout", "120", "app:app"]