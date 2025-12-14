FROM python:3.12
#Debian
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
# 使用 Gunicorn 作為生產伺服器，4 個 worker，每個 2 個線程
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "--timeout", "120", "--worker-class", "gthread", "app:app"]