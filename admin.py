from flask import Flask, request, render_template, redirect, url_for, session, flash
from koneksi import get_db_connection

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route('/', methods=['GET'])
def homeadmin():
    """Halaman utama."""
    if 'admin' not in session:
        return redirect(url_for('login99'))

    # Ambil data pengguna berdasarkan session['user']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil nama pengguna
    cursor.execute("SELECT username FROM tb_admin WHERE id_admin = %s", (session['user'],))
    admin = cursor.fetchone()
    if not admin:
        flash("Data pengguna tidak ditemukan!", "error")
        cursor.close()
        conn.close()
        return redirect(url_for('login99'))

    # Ambil data tb_ruang
    cursor.execute("SELECT * FROM tb_ruang LIMIT 3")
    ruang = cursor.fetchall()

    cursor.close()
    conn.close()

    # Kirim data ke template
    return render_template('index.html', admin_name=admin['username'], ruangs=ruang)

@app.route('/login99', methods=['GET', 'POST'])
def login():
    """Halaman login pengguna."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_admin WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user or not user['password']:
            flash("Username atau Password salah!", "error")
            return redirect(url_for('login'))

        session['user'] = user['id_user']
        return redirect(url_for('homeadmin'))

    return render_template('loginadmin.html')
  
  
if __name__ == '__main__':
  app.run(debug=True, port=6969)