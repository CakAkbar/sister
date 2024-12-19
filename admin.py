from flask import Flask, request, render_template, redirect, url_for, session, flash
from koneksi import get_db_connection

app = Flask(__name__)
app.secret_key = "your_secret_key"

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
        cursor.close()
        conn.close()

        if not user or user['password'] != password:
            flash("Username atau Password salah!", "error")
            return redirect(url_for('login'))

        session['admin'] = user['id_admin']  # Simpan id_admin di session
        return redirect(url_for('homeadmin'))

    return render_template('loginadmin.html')


@app.route('/logout', methods=['GET'])
def logout():
    """Logout pengguna."""
    session.clear()
    flash("Anda telah logout!", "info")
    return redirect(url_for('login'))


@app.route('/', methods=['GET'])
def homeadmin():
    """Halaman utama."""
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil nama pengguna
    cursor.execute("SELECT username FROM tb_admin WHERE id_admin = %s", (session['admin'],))
    admin = cursor.fetchone()
    if not admin:
        flash("Data pengguna tidak ditemukan!", "error")
        cursor.close()
        conn.close()
        return redirect(url_for('login'))

    # Ambil data dari tb_form
    cursor.execute("SELECT * FROM tb_form")
    forms = cursor.fetchall()

    cursor.close()
    conn.close()

    # Kirim data ke template
    return render_template('indexadmin.html', admin_name=admin['username'], forms=forms)


@app.route('/update_status', methods=['POST'])
def update_status():
    if 'admin' not in session:
        return redirect(url_for('login'))

    id_form = request.form.get('id_form')
    action = request.form.get('action')
    print(f"DEBUG: Received id_form={id_form}, action={action}")

    if not id_form or not action:
        flash("Data form tidak valid!", "error")
        return redirect(url_for('homeadmin'))

    # Tentukan status baru berdasarkan action
    if action == "accept":
        new_status = "Diterima"
    elif action == "reject":
        new_status = "Ditolak"
    else:
        flash("Aksi tidak valid!", "error")
        return redirect(url_for('homeadmin'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tb_form SET status = %s WHERE id_form = %s AND status = 'Pending'", (new_status, id_form))
        conn.commit()
        print(f"DEBUG: Updated {cursor.rowcount} rows")
        if cursor.rowcount == 0:
            flash("Tidak ada baris yang diperbarui. Pastikan status awal adalah Pending.", "error")
        else:
            flash(f"Status berhasil diperbarui menjadi {new_status}!", "success")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"ERROR: {e}")
        flash("Terjadi kesalahan saat memperbarui status.", "error")

    return redirect(url_for('homeadmin'))

if __name__ == '__main__':
    app.run(debug=True, port=6969)
