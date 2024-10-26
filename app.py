from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "masanto"  # Ganti dengan key yang lebih aman

def cek_imei(imei):
    """
    Fungsi untuk memeriksa IMEI melalui API dan menentukan statusnya.

    Args:
      imei: Nomor IMEI yang akan diperiksa.

    Returns:
      Dictionary berisi IMEI dan statusnya ("LIVE" atau "DIE").
    """
    url = f"https://api.quanlybanhang.store/mi/fmi.php?imei={imei}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('message') == 'FIND XIAOMI OFF':
            status = "LIVE"
        else:
            status = "DIE"
        return {"imei": imei, "status": status}
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"imei": imei, "status": "ERROR"}

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        key = request.form['key']
        if key == "masanto":  # Ganti dengan kunci yang sebenarnya
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Key salah")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/cek_imei', methods=['POST'])
def cek_imei_api():
    """
    Endpoint untuk memeriksa IMEI. Menerima data IMEI dalam format JSON.

    Contoh request body:
    {
        "imei": "123456789012345"
    }
    """
    data = request.get_json()
    imei = data.get('imei')
    if not imei:
        return jsonify({"error": "IMEI tidak ditemukan dalam request"}), 400
    hasil = cek_imei(imei)
    return jsonify(hasil)

if __name__ == '__main__':
    app.run(debug=True)