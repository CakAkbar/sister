from flask import Flask, request, render_template, redirect, url_for, session, flash
from koneksi import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Dibutuhkan untuk session management

# Halaman utama
@app.route('/', methods=['GET'])
def home():
    """Halaman utama."""
    if 'user' not in session:
        return redirect(url_for('login'))

    # Ambil data pengguna berdasarkan session['user']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil nama pengguna
    cursor.execute("SELECT username FROM tb_users WHERE id_user = %s", (session['user'],))
    user = cursor.fetchone()
    if not user:
        flash("Data pengguna tidak ditemukan!", "error")
        cursor.close()
        conn.close()
        return redirect(url_for('login'))

    # Ambil data tb_ruang
    cursor.execute("SELECT * FROM tb_ruang LIMIT 3")
    ruang = cursor.fetchall()

    cursor.close()
    conn.close()

    # Kirim data ke template
    return render_template('index.html', user_name=user['username'], ruangs=ruang)

# Halaman register
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Halaman register pengguna baru."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash("Semua field wajib diisi!", "error")
            return redirect(url_for('register'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("Username atau Email sudah digunakan!", "error")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO tb_users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        conn.commit()
        conn.close()

        flash("Registrasi berhasil, silakan login!", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Halaman login pengguna."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user or not check_password_hash(user['password'], password):
            flash("Username atau Password salah!", "error")
            return redirect(url_for('login'))

        session['user'] = user['id_user']
        return redirect(url_for('home'))

    return render_template('login.html')

# Halaman logout
@app.route('/logout')
def logout():
    """Logout pengguna."""
    session.pop('user', None)
    flash("Anda telah logout.", "success")
    return redirect(url_for('login'))

# Halaman untuk melihat daftar ruangan
@app.route('/ruang/view', methods=['GET'])
def view_ruang():
    """Halaman untuk melihat daftar ruangan."""
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_ruang")
    ruangs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('ruang_view.html', ruangs=ruangs, user=session['user'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
