"""
Aplikasi Caesar Cipher dengan Modulo Arithmetic
Menggunakan Python dan Flask Framework
Tanpa Emoticon
"""

import os
from flask import Flask, render_template, request

# Inisialisasi Flask App dengan direktori template dan static yang disesuaikan
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# Pemetaan Huruf ke Angka (A=0 ... Z=25) dan sebaliknya
CHAR_TO_INDEX = {chr(ord('A') + i): i for i in range(26)}
INDEX_TO_CHAR = {i: chr(ord('A') + i) for i in range(26)}


def proses_caesar_cipher(teks: str, shift: int, mode: str = "enkripsi") -> dict:
    """
    Memproses teks menggunakan Caesar Cipher dengan operasi modulo.
    
    Rumus Enkripsi: C = (P + K) mod 26
    Rumus Dekripsi: P = (C - K) mod 26
    
    Args:
        teks (str): Teks masukan (Plaintext / Ciphertext)
        shift (int): Nilai pergeseran (Kunci K)
        mode (str): 'enkripsi' atau 'dekripsi'
        
    Returns:
        dict: Hasil proses beserta detail perhitungan modulo per karakter
    """
    shift_effective = shift % 26
    tanda_operasi = "+" if mode == "enkripsi" else "-"
    k_val = shift_effective if mode == "enkripsi" else -shift_effective
    
    detail_proses = []
    hasil_karakter = []
    
    for idx, char in enumerate(teks, start=1):
        if char.isalpha():
            is_upper = char.isupper()
            base_char = 'A' if is_upper else 'a'
            base_ord = ord(base_char)
            
            p_val = ord(char) - base_ord  # Nilai posisi (0 - 25)
            
            if mode == "enkripsi":
                raw_calc = p_val + shift
                c_val = raw_calc % 26
                rumus_str = f"({p_val} + {shift}) mod 26"
                proses_str = f"{raw_calc} mod 26 = {c_val}"
            else:  # dekripsi
                raw_calc = p_val - shift
                c_val = raw_calc % 26
                rumus_str = f"({p_val} - {shift}) mod 26"
                proses_str = f"{raw_calc} mod 26 = {c_val}"
                
            char_res = chr(base_ord + c_val)
            
            detail_proses.append({
                'no': idx,
                'char_asal': char,
                'val_asal': p_val,
                'rumus': rumus_str,
                'proses': proses_str,
                'val_hasil': c_val,
                'char_hasil': char_res,
                'is_alpha': True,
                'case_type': "Kapital" if is_upper else "Kecil"
            })
            hasil_karakter.append(char_res)
        else:
            # Karakter non-alfabet (spasi, angka, tanda baca) dipertahankan
            detail_proses.append({
                'no': idx,
                'char_asal': char,
                'val_asal': "-",
                'rumus': "Karakter Non-Alfabet",
                'proses': "Dipertahankan (Tanpa Modulo)",
                'val_hasil': "-",
                'char_hasil': char,
                'is_alpha': False,
                'case_type': "Simbol/Spasi"
            })
            hasil_karakter.append(char)
            
    teks_hasil = "".join(hasil_karakter)
    
    return {
        'teks_asal': teks,
        'teks_hasil': teks_hasil,
        'shift_original': shift,
        'shift_effective': shift_effective,
        'mode': mode,
        'detail': detail_proses,
        'jumlah_karakter': len(teks),
        'jumlah_huruf': sum(1 for c in teks if c.isalpha())
    }


@app.route("/", methods=["GET", "POST"])
def index():
    """Route utama aplikasi web Caesar Cipher."""
    mode = "enkripsi"
    teks_input = ""
    shift_input = 3
    hasil_data = None
    error = None

    if request.method == "POST":
        mode = request.form.get("mode", "enkripsi")
        teks_input = request.form.get("teks_input", "")
        raw_shift = request.form.get("shift_input", "3").strip()

        # Validasi input
        if not teks_input.strip():
            error = "Teks masukan tidak boleh kosong. Silakan masukkan teks yang ingin diproses."
        else:
            try:
                shift_input = int(raw_shift)
                hasil_data = proses_caesar_cipher(teks_input, shift_input, mode)
            except ValueError:
                error = "Nilai pergeseran (shift) harus berupa angka bulat (integer)."

    # Tabel referensi alfabet 0..25 -> A..Z
    tabel_referensi = [{'angka': i, 'huruf': INDEX_TO_CHAR[i]} for i in range(26)]

    return render_template(
        "index.html",
        mode=mode,
        teks_input=teks_input,
        shift_input=shift_input,
        hasil_data=hasil_data,
        error=error,
        tabel_referensi=tabel_referensi,
    )


if __name__ == "__main__":
    print("Menjalankan Aplikasi Caesar Cipher Modulo pada http://127.0.0.1:5002")
    app.run(debug=True, port=5002)
