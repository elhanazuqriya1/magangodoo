# 🎉 ODOO SIMRS ADDONS 🎉
Sistem Informasi Rumah Sakit berbasis Odoo

---

## 🚀 Ketentuan Pengembangan

1. 🏷️ **Gunakan Odoo versi 17.0**
2. 🔄 **Selalu lakukan pull** (tarik update terbaru) dari repository sebelum mulai coding
3. 📤 **Selalu push** (unggah perubahan) sekecil apapun coding yang telah dilakukan

---

## ⚙️ System Requirements

- 🐍 **Python 3.10+**
- 🗃️ **Odoo 17.0** (Community Edition)
- 🐘 **PostgreSQL** (versi yang direkomendasikan oleh Odoo 17)
- 💻 pip, virtualenv
- 🖥️ Sistem operasi: Linux (direkomendasikan Ubuntu 22.04 LTS), Windows, atau MacOS

---

## 🧑‍💻 Setup Virtual Environment

1. **Clone repository ini**
   ```bash
   git clone https://github.com/elhanazuqriya1/magangodoo.git
   cd magangodoo
   ```
2. **Buat dan aktifkan virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # untuk Linux/MacOS
   venv\Scripts\activate      # untuk Windows
   ```
3. **Install dependencies Odoo**
   > Daftar dependencies mengikuti dokumentasi Odoo 17, atau bisa menggunakan file `requirements.txt` jika tersedia.

   Jika tidak ada file requirements, instalasi umum:
   ```bash
   pip install wheel
   pip install -r requirements.txt   # jika file tersedia
   ```

4. **Konfigurasi Odoo**
   - Pastikan Odoo 17 telah terpasang dengan benar.
   - Tambahkan path add-ons custom ini pada konfigurasi Odoo Anda.

5. **Menjalankan Odoo**
   - Jalankan Odoo seperti biasa, pastikan modul SIMRS terdeteksi.

---

## 📝 Catatan Pengembangan

- Setiap developer **WAJIB** melakukan `git pull` sebelum coding, dan segera `git push` setelah selesai atau ada perubahan.
- Dokumentasikan setiap fitur atau perubahan yang signifikan di commit message.

---

<p align="center">
  <img src="https://media.giphy.com/media/26ufnwz3wDUli7GU0/giphy.gif" width="200" alt="Coding Animation" />
  <br>
  <b>Selamat Berkarya dan Berkolaborasi!</b> 🚑💻🚀
</p>

---

*Silakan update README ini jika ada perubahan sistem requirement atau ketentuan pengembangan.*
