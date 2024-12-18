from flask import Flask, request, render_template, redirect, url_for, session, flash
from koneksi import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Dibutuhkan untuk session management

REDIRECT_PORT_5000 = "http://127.0.0.1:5000/"

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Halaman register pengguna baru."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash("Semua field wajib diisi!", "error")
            return render_template('register.html')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tb_users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("Username atau Email sudah digunakan!", "error")
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO tb_users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        conn.commit()
        conn.close()

        flash("Registrasi berhasil! Silakan login di tombol login sebelah kiri.", "success")
        return render_template('register.html')

    return render_template('register.html')

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

        session['user'] = user['username']
        # Redirect ke port 5000 setelah login berhasil
        return redirect(REDIRECT_PORT_5000)

    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout pengguna."""
    session.pop('user', None)
    flash("Anda telah logout.", "success")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
