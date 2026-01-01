from flask import Flask
import os
import pyodbc
import time

app = Flask(__name__)

# Konfigurasi Database dari Environment Variables Azure
def get_db_connection():
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
def index():
    # Menampilkan ID Instance untuk melihat perubahan saat scaling
    instance_id = os.environ.get('WEBSITE_INSTANCE_ID', 'Local-Machine')
    return f"<h1>Web Berhasil Berjalan!</h1><p>Instance ID: {instance_id}</p><br><a href='/db-test'>Test Database</a> | <a href='/stress'>Stress Test (CPU)</a>"

@app.route('/db-test')
def db_test():
    try:
        conn = get_db_connection()
        return "Koneksi ke db_awan15 via Private Endpoint Berhasil!"
    except Exception as e:
        return f"Gagal Koneksi Database: {str(e)}"

@app.route('/stress')
def stress():
    # Loop berat untuk menaikkan CPU > 70%
    start_time = time.time()
    while time.time() - start_time < 60: # Berjalan selama 1 menit
        _ = [x**2 for x in range(5000)]
    return "Stress test selesai. Pantau kenaikan instance di Portal Azure!"

if __name__ == '__main__':
    app.run()