# SampahCerdas — Panduan Deploy

## Struktur file yang dibutuhkan
```
├── app.py
├── requirements.txt
└── model_densenet121_anorganik_best.h5    ← dari hasil training
    (atau folder: model_densenet121_anorganik_saved/)
```

---

## A. Deploy ke Hugging Face Spaces (GRATIS, cocok untuk HP)

1. Buat akun di https://huggingface.co
2. Buat Space baru:
   - New Space → pilih **Streamlit** sebagai SDK
   - Visibility: Public
3. Upload file:
   ```
   app.py
   requirements.txt
   model_densenet121_anorganik_best.h5
   ```
4. Space otomatis build dan bisa diakses dari HP via browser
5. Share URL ke siapapun

> **Catatan model besar:** Jika file .h5 > 100MB, gunakan Git LFS:
> ```bash
> git lfs install
> git lfs track "*.h5"
> git add .gitattributes
> git add model_densenet121_anorganik_best.h5
> git commit -m "add model"
> git push
> ```

---

## B. Deploy ke Streamlit Community Cloud (GRATIS)

1. Push semua file ke GitHub repo
2. Buka https://share.streamlit.io
3. Connect GitHub → pilih repo → pilih app.py
4. Deploy → dapat URL yang bisa dibuka di HP

> **Catatan model:** Streamlit Cloud limit repo 1GB. Untuk model besar,
> upload ke Hugging Face Hub dan load dari sana:
> ```python
> from huggingface_hub import hf_hub_download
> path = hf_hub_download(repo_id="username/repo", filename="model.h5")
> model = tf.keras.models.load_model(path)
> ```

---

## C. Jalankan lokal (untuk testing di HP via WiFi)

```bash
pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Lalu buka di HP: `http://[IP-komputer]:8501`
Cari IP komputer: `ipconfig` (Windows) atau `ifconfig` (Linux/Mac)

---

## Tips akses dari HP

- Gunakan mode "Desktop site" di browser HP untuk tampilan penuh
- Atau tambahkan ke Home Screen untuk pengalaman seperti app native
- Resolusi kamera HP sudah cukup untuk deteksi (model input 224x224)

---

## Cara mengganti nama kelas

Di `app.py`, edit dictionary `CLASS_INFO` — tambah/hapus kelas sesuai
dataset yang kamu miliki. Pastikan urutan kelas SAMA dengan saat training
(`sorted(CLASS_INFO.keys())` harus sama dengan `CLASS_NAMES` di notebook).

