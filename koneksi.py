from flask import Flask, abort 
import mysql.connector

app = Flask(__name__)

# Konfigurasi koneksi database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_booking'
}

def get_db_connection():
    """Membuat koneksi ke database."""
    return mysql.connector.connect(**DB_CONFIG)

if __name__ == '__main__':
    app.run(debug=True)
