from flask import Flask, render_template, request, redirect, url_for, session, flash
from koneksi import get_db_connection
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pastikan folder `static/uploads` ada
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/booking', methods=['GET', 'POST'])
def booking_form():
    if 'user' not in session:  # Pastikan pengguna sudah login
        flash("Silakan login terlebih dahulu!", "warning")
        return redirect(url_for('login'))  # Arahkan ke halaman login jika belum login

    id_user = session['user']  # Ambil id_user dari session
    id_ruang = request.args.get('id_ruang')

    with get_db_connection() as conn:
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute("SELECT nama_ruang FROM tb_ruang WHERE id_ruang = %s", (id_ruang,))
            ruang = cursor.fetchone()

            if not ruang:
                return "Ruang tidak ditemukan", 404

            if request.method == 'POST':
                nim = request.form['nim']
                nama_peminjam = request.form['nama_peminjam']
                tanggal_mulai = request.form['tanggal_mulai']
                tanggal_selesai = request.form['tanggal_selesai']
                perihal = request.form['perihal']
                file_proposal = request.files['file_proposal']
                status = 'Pending'

                # Validasi apakah end_date lebih besar dari start_date
                if tanggal_selesai < tanggal_mulai:
                    return render_template(
                        'form_booking.html',
                        id_ruang=id_ruang,
                        nama_ruang=ruang['nama_ruang'],
                        error="Masukkan Tanggal Mulai dan Tanggal Selesai yang Sesuai !!"
                    )

                # Pengecekan apakah tanggal sudah terpakai
                query_check = """
                    SELECT * FROM tb_form 
                    WHERE id_ruang = %s AND (
                        (start_date <= %s AND end_date >= %s) OR
                        (start_date <= %s AND end_date >= %s) OR
                        (start_date >= %s AND end_date <= %s)
                    )
                """
                cursor.execute(query_check, (id_ruang, tanggal_mulai, tanggal_mulai, tanggal_selesai, tanggal_selesai, tanggal_mulai, tanggal_selesai))
                konflik = cursor.fetchone()

                if konflik:
                    return render_template(
                        'form_booking.html',
                        id_ruang=id_ruang,
                        nama_ruang=ruang['nama_ruang'],
                        error="Ruangan sudah dipesan pada tanggal tersebut."
                    )

                # Proses unggah file
                if file_proposal and file_proposal.filename != '':
                    filename = secure_filename(file_proposal.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file_proposal.save(file_path)
                    file_path_db = filename  # Simpan hanya nama file ke database
                else:
                    file_path_db = None

                # Simpan data ke database termasuk id_user
                query_insert = """
                    INSERT INTO tb_form (id_user, nim, nama_peminjam, id_ruang, start_date, end_date, perihal, proposal, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_insert, (id_user, nim, nama_peminjam, id_ruang, tanggal_mulai, tanggal_selesai, perihal, file_path_db, status))
                conn.commit()

                # Redirect dengan parameter sukses
                return redirect(url_for('booking_form', id_ruang=id_ruang, success=True))

    success = request.args.get('success', False)
    return render_template('form_booking.html', id_ruang=id_ruang, id_user=id_user, nama_ruang=ruang['nama_ruang'], success=success)



if __name__ == '__main__':
    app.run(debug=True, port=5001)
