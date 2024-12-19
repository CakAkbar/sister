import os
from flask import Flask, request, render_template, redirect, url_for, session, flash, send_from_directory
from koneksi import get_db_connection, abort

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = os.path.abspath("../uploads")  # Path absolut ke folder uploads

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


@app.route('/logoutadmin', methods=['GET'])
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

    # Hitung jumlah status Pending
    cursor.execute("SELECT COUNT(*) AS pending_count FROM tb_form WHERE status = 'Pending'")
    pending = cursor.fetchone()['pending_count']
    
    cursor.execute("SELECT COUNT(*) AS tolak_count FROM tb_form WHERE status = 'Ditolak'")
    tolak = cursor.fetchone()['tolak_count']
    
    cursor.execute("SELECT COUNT(*) AS terima_count FROM tb_form WHERE status = 'Diterima'")
    terima = cursor.fetchone()['terima_count']

    cursor.close()
    conn.close()

    # Kirim data ke template
    return render_template('indexadmin.html', admin_name=admin['username'], forms=forms, pending=pending, tolak=tolak, terima=terima)


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

@app.route('/uploads/<filename>')
def serve_uploads(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        abort(404)

@app.route('/gedungadmin', methods=['GET'])
def gedungadmin():
    """Halaman daftar ruangan."""
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Ambil data dari tb_ruang
    cursor.execute("SELECT * FROM tb_ruang")
    rooms = cursor.fetchall()

    cursor.close()
    conn.close()

    # Kirim data ke template
    return render_template('gedungadmin.html', rooms=rooms)


@app.route('/tambah_ruang', methods=['GET', 'POST'])
def tambah_ruang():
    """Menambahkan ruangan baru ke dalam database."""
    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Ambil data dari form
        nama_ruang = request.form.get('nama_ruang')
        kapasitas = request.form.get('kapasitas')
        deskripsi = request.form.get('deskripsi')
        iframe = request.form.get('iframe')
        fasilitas = request.form.get('fasilitas')
        img = request.files.get('img')

        # Validasi input
        if not (nama_ruang and kapasitas and deskripsi and iframe and fasilitas and img):
            flash("Semua field harus diisi!", "error")
            return redirect(url_for('tambah_ruang'))

        # Simpan file gambar
        filename = None
        if img:
            # Path ke folder static/img
            upload_folder = os.path.join('static', 'img')
            os.makedirs(upload_folder, exist_ok=True)  # Buat folder jika belum ada

            # Simpan file gambar
            filename = img.filename
            img_path = os.path.join(upload_folder, filename)
            img.save(img_path)

        try:
            # Simpan data ke database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tb_ruang (nama_ruang, kapasitas, deskripsi, iframe, fasilitas, img)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nama_ruang, kapasitas, deskripsi, iframe, fasilitas, filename))
            conn.commit()
            cursor.close()
            conn.close()

            # Redirect dengan parameter success ke halaman tambahruang
            return redirect(url_for('tambah_ruang', success='true'))

        except Exception as e:
            print(f"ERROR: {e}")
            flash("Terjadi kesalahan saat menambahkan ruangan.", "error")
            return redirect(url_for('tambah_ruang'))

    # Cek parameter success
    success = request.args.get('success')
    return render_template('tambahruang.html', success=success)


@app.route('/edit_ruang/<int:id_ruang>', methods=['GET', 'POST'])
def edit_ruang(id_ruang):
    """Edit data ruangan."""
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Ambil data dari form
        nama_ruang = request.form.get('nama_ruang')
        kapasitas = request.form.get('kapasitas')
        deskripsi = request.form.get('deskripsi')
        iframe = request.form.get('iframe')
        fasilitas = request.form.get('fasilitas')
        img = request.files.get('img')

        # Validasi input
        if not (nama_ruang and kapasitas and deskripsi and iframe and fasilitas):
            flash("Semua field harus diisi!", "error")
            return redirect(url_for('edit_ruang', id_ruang=id_ruang))

        # Simpan file gambar jika ada
        filename = None
        if img and img.filename != "":
            # Path ke folder static/img
            upload_folder = os.path.join('static', 'img')
            os.makedirs(upload_folder, exist_ok=True)  # Buat folder jika belum ada

            # Simpan file gambar
            filename = img.filename
            img_path = os.path.join(upload_folder, filename)
            img.save(img_path)

        try:
            # Update data di database
            if img and img.filename != "":
                cursor.execute("""
                    UPDATE tb_ruang
                    SET nama_ruang = %s, kapasitas = %s, deskripsi = %s, iframe = %s, fasilitas = %s, img = %s
                    WHERE id_ruang = %s
                """, (nama_ruang, kapasitas, deskripsi, iframe, fasilitas, filename, id_ruang))
            else:
                cursor.execute("""
                    UPDATE tb_ruang
                    SET nama_ruang = %s, kapasitas = %s, deskripsi = %s, iframe = %s, fasilitas = %s
                    WHERE id_ruang = %s
                """, (nama_ruang, kapasitas, deskripsi, iframe, fasilitas, id_ruang))

            conn.commit()
            flash("Ruangan berhasil diperbarui!", "success")
        except Exception as e:
            print(f"ERROR: {e}")
            flash("Terjadi kesalahan saat memperbarui ruangan.", "error")
        finally:
            cursor.close()
            conn.close()

        # Redirect ke halaman yang sama dengan parameter success
        return redirect(url_for('edit_ruang', id_ruang=id_ruang, success='true'))

    # Ambil data ruangan berdasarkan ID
    cursor.execute("SELECT * FROM tb_ruang WHERE id_ruang = %s", (id_ruang,))
    room = cursor.fetchone()
    cursor.close()
    conn.close()

    if not room:
        flash("Ruangan tidak ditemukan.", "error")
        return redirect(url_for('gedungadmin'))

    success = request.args.get('success')
    return render_template('editruang.html', room=room, success=success)

@app.route('/hapus_ruang', methods=['GET'])
def hapus_ruang():
    """Halaman daftar ruangan untuk dihapus."""
    if 'admin' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_ruang, nama_ruang, kapasitas, SUBSTRING(deskripsi, 1, 30) AS deskripsi FROM tb_ruang")
    rooms = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('hapusruang.html', rooms=rooms)


@app.route('/delete_ruang/<int:id_ruang>', methods=['POST'])
def delete_ruang(id_ruang):
    """Menghapus ruangan dari database."""
    if 'admin' not in session:
        return redirect(url_for('login'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tb_ruang WHERE id_ruang = %s", (id_ruang,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Ruangan berhasil dihapus.", "success")
    except Exception as e:
        print(f"ERROR: {e}")
        flash("Terjadi kesalahan saat menghapus ruangan.", "error")

    return redirect(url_for('hapus_ruang'))



if __name__ == '__main__':
    app.run(debug=True, port=6969)
