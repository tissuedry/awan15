from flask import Flask
import os
import pyodbc
import time

app = Flask(__name__)

def get_db_connection():
    # Mengambil kredensial dari Environment Variables di Portal Azure
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
    instance_id = os.environ.get('WEBSITE_INSTANCE_ID', 'Local-Machine')
    return f"""
    <h1>Website Cloud Computing - {instance_id}</h1>
    <p>Status: Running on Indonesia Central</p>
    <hr>
    <a href='/db-test'>Cek Koneksi Database</a> | 
    <a href='/stress'>Mulai Stress Test (Autoscale)</a>
    """

@app.route('/db-test')
def db_test():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        row = cursor.fetchone()
        conn.close()
        return f"<h1>Koneksi Berhasil!</h1><p>Versi DB: {row[0]}</p>"
    except Exception as e:
        return f"<h1>Koneksi Gagal</h1><p>Error: {str(e)}</p>"

@app.route('/stress')
def stress():
    # Loop berat untuk memicu CPU > 70% agar Autoscale aktif
    start = time.time()
    while time.time() - start < 60:  # Berjalan selama 60 detik
        _ = [x**2 for x in range(10000)]
    return "<h1>Stress Test Selesai</h1><p>Periksa Instance Count di Azure Portal.</p>"

if __name__ == "__main__":
    app.run()