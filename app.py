from flask import Flask
import os
import pyodbc
import time

app = Flask(__name__)

def get_db_connection():
    # Menggunakan Environment Variables yang Anda buat di Azure
    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={os.environ.get('DB_SERVER')};"
        f"Database={os.environ.get('DB_NAME')};"
        f"UID={os.environ.get('DB_USER')};"
        f"PWD={os.environ.get('DB_PASSWORD')};"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)

@app.route('/')
def home():
    # Mengambil ID Instance untuk membuktikan Autoscale sedang berjalan
    instance_id = os.environ.get('WEBSITE_INSTANCE_ID', 'Local-Machine')
    return f"<h1>Web Berhasil Jalan!</h1><p>Instance ID: {instance_id}</p><br><a href='/db-test'>Cek Koneksi Database</a> | <a href='/stress'>Mulai Stress Test</a>"

@app.route('/db-test')
def db_test():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        conn.close()
        return f"<h1>Koneksi DB Berhasil!</h1><p>Versi: {row[0]}</p>"
    except Exception as e:
        return f"<h1>Koneksi DB Gagal</h1><p>Error: {str(e)}</p>"

@app.route('/stress')
def stress():
    # Memicu CPU > 70% agar Autoscale menambah instance menjadi 3
    start = time.time()
    while time.time() - start < 60:
        _ = [x**2 for x in range(5000)]
    return "<h1>Stress Test Selesai</h1><p>Pantau portal Azure untuk melihat penambahan Instance Count.</p>"

if __name__ == "__main__":
    app.run()