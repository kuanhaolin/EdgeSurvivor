from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector, os, time

app = Flask(__name__)
CORS(app)

db_conf = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'user'),
    'password': os.environ.get('DB_PASSWORD', 'password'),
    'database': os.environ.get('DB_NAME', 'edgesurvivor')
}

def get_conn(): 
    return mysql.connector.connect(**db_conf)

# 等待 DB
for _ in range(5):
    try:
        get_conn().close()
        break
    except:
        time.sleep(2)

# 建 table
conn = get_conn()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS places (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  location VARCHAR(100)
)
""")
conn.commit()
cursor.close()
conn.close()

@app.route("/places", methods=["GET"])
def get_places():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM places")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(res)

@app.route("/places", methods=["POST"])
def add_place():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO places (name, location) VALUES (%s,%s)",
                   (data['name'], data['location']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)