from flask import Flask, render_template, request, redirect, url_for
from koneksi import get_db_connection
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/booking', methods=['GET', 'POST'])
def booking_form():
    id_ruang = request.args.get('id_ruang')

    with get_db_connection() as conn:
        with conn.cursor(dictionary=True, buffered=True) as cursor:
            cursor.execute("SELECT nama_ruang FROM tb_ruang WHERE id_ruang = %s", (id_ruang,))
            ruang = cursor.fetchone()

            if not ruang:
                return "Ruang tidak ditemukan", 404

            if request.method == 'POST':
                nama_peminjam = request.form['nama_peminjam']
                tanggal_mulai = request.form['tanggal_mulai']
                tanggal_selesai = request.form['tanggal_selesai']
                file_proposal = request.files['file_proposal']

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
                else:
                    file_path = None

                # Simpan data ke database
                query_insert = """
                    INSERT INTO tb_form (nama_peminjam, id_ruang, start_date, end_date, proposal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query_insert, (nama_peminjam, id_ruang, tanggal_mulai, tanggal_selesai, file_path))
                conn.commit()

                # Redirect dengan parameter sukses
                return redirect(url_for('booking_form', id_ruang=id_ruang, success=True))

    success = request.args.get('success', False)
    return render_template('form_booking.html', id_ruang=id_ruang, nama_ruang=ruang['nama_ruang'], success=success)




if __name__ == '__main__':
    app.run(debug=True, port=5001)
