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
    start_time = time.time()
    duration = 300  # Set ke 5 menit (300 detik)
    n = 500         # Nilai n untuk loop n^3

    while time.time() - start_time < duration:
        # Perulangan bersarang n^3 (Cubic Complexity)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    _ = i * j * k  # Operasi matematika untuk membebani CPU
                    
    return f"<h1>Stress Test n^3 Selesai</h1><p>Beban CPU tinggi selama 5 menit.</p>"
if __name__ == "__main__":
    app.run()