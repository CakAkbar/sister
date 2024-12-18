from flask import Flask, render_template, redirect
from koneksi import get_db_connection, app

@app.route('/', methods=['GET'])
def home():
    # Redirect ke /ruang/view
    return redirect('/ruang/view')

@app.route('/ruang/view', methods=['GET'])
def view_ruang():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_ruang")
    ruangs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('ruang_view.html', ruangs=ruangs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
