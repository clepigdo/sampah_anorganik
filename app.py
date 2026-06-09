import streamlit as st
import numpy as np
from PIL import Image
import io, os, time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SampahCerdas",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

/* ===== FONT & BASE ===== */
html, body, [class*="css"] {
    font-family: Inter, system-ui, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Mengubah background utama aplikasi menjadi gelap */
[data-testid="stAppViewContainer"]{
    background: #0f172a; /* Slate 900 */
}

/* Memastikan teks dasar bawaan Streamlit menjadi terang */
.stMarkdown, p, h1, h2, h3, h4, h5, h6, li, span, label {
    color: #f8fafc !important; /* Slate 50 */
}

[data-testid="stHeader"]{
    background: transparent;
}

[data-testid="block-container"]{
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 900px;
}

/* ===== HERO ===== */
.hero{
    background: #065f46; /* Emerald 800 */
    border-radius: 24px;
    padding: 2.5rem 2rem;
    text-align: center;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

.hero h1{
    font-size: 2.3rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.5px;
    color: white !important;
}

.hero p{
    font-size: 1rem;
    color: #d1fae5 !important; /* Emerald 100 */
    opacity: 1;
    margin-top: 8px;
}

/* ===== CARD ===== */
.card{
    background: #1e293b; /* Slate 800 */
    border: 1px solid #334155; /* Slate 700 */
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

/* ===== RESULT SUCCESS ===== */
.result-main{
    background: #1e293b;
    border: none;
    border-left: 6px solid #22c55e; /* Green 500 */
    border-radius: 20px;
    padding: 1.8rem;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.result-main .class-name{
    font-size: 2rem;
    font-weight: 800;
    color: #4ade80 !important; /* Green 400 */
}

.result-main .confidence{
    color: #94a3b8 !important; /* Slate 400 */
    margin-top: 8px;
}

/* ===== RESULT UNKNOWN ===== */
.result-unknown{
    background: #1e293b;
    border: none;
    border-left: 6px solid #f59e0b; /* Amber 500 */
    border-radius: 20px;
    padding: 1.8rem;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.result-unknown .class-name{
    font-size: 1.8rem;
    font-weight: 800;
    color: #fbbf24 !important; /* Amber 400 */
}

/* ===== BUTTON ===== */
div.stButton > button{
    width: 100%;
    height: 54px;
    border: none;
    border-radius: 14px;
    background: #16a34a;
    color: white !important;
    font-size: 1rem;
    font-weight: 700;
    box-shadow: 0 6px 16px rgba(0,0,0,0.3);
    transition: .25s;
}

div.stButton > button:hover{
    background: #15803d;
    transform: translateY(-2px);
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"]{
    border: 2px dashed #22c55e;
    border-radius: 18px;
    background: #0f172a;
    padding: 1rem;
}

[data-testid="stFileUploader"] * {
    color: #f8fafc !important; /* Memastikan teks dalam uploader terang */
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"]{
    gap: 10px;
}

.stTabs [data-baseweb="tab"]{
    background: #1e293b;
    border-radius: 12px;
    padding: 10px 18px;
    border: 1px solid #334155;
    color: #cbd5e1 !important; /* Teks abu-abu terang untuk tab non-aktif */
}

.stTabs [aria-selected="true"]{
    background: #16a34a !important;
    color: white !important;
    border-color: #16a34a;
}

/* ===== CONFIDENCE BAR ===== */
.conf-bar-bg{
    background: #334155; /* Slate 700 */
    height: 10px;
    border-radius: 999px;
    overflow: hidden;
}

.conf-bar-fill{
    height: 100%;
    border-radius: 999px;
}

/* ===== TIP BOX ===== */
/* Menggunakan background semi-transparan dengan teks berwarna terang */
.tip-box{
    background: rgba(34, 197, 94, 0.1); 
    border-left: 5px solid #22c55e;
    border-radius: 12px;
    padding: 1rem;
    color: #86efac !important; /* Green 300 */
}

.tip-box-info{
    background: rgba(59, 130, 246, 0.1);
    border-left: 5px solid #3b82f6;
    border-radius: 12px;
    padding: 1rem;
    color: #93c5fd !important; /* Blue 300 */
}

.tip-box-warn{
    background: rgba(245, 158, 11, 0.1);
    border-left: 5px solid #f59e0b;
    border-radius: 12px;
    padding: 1rem;
    color: #fde047 !important; /* Yellow 300 */
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader{
    font-weight: 600 !important;
    color: #f8fafc !important;
}

.streamlit-expanderContent {
    background: #1e293b;
    border-radius: 0 0 12px 12px;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"]{
    background: #1e293b;
    border-right: 1px solid #334155;
}

section[data-testid="stSidebar"] *{
    color: #f8fafc !important; /* Teks sidebar jadi putih */
}

/* ===== METRIC CARDS ===== */
.metric-card{
    background: #1e293b;
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    border: 1px solid #334155;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
}

.metric-number{
    font-size: 1.4rem;
    font-weight: 800;
    color: #4ade80 !important; /* Green 400 */
}

.metric-label{
    font-size: .8rem;
    color: #94a3b8 !important; /* Slate 400 */
}

/* ===== FOOTER ===== */
.footer{
    text-align: center;
    color: #64748b !important; /* Slate 500 */
    font-size: .85rem;
    margin-top: 2rem;
}

/* ===== MOBILE ===== */
@media (max-width:768px){

.hero{
    padding: 2rem 1rem;
}

.hero h1{
    font-size: 1.8rem;
}

.result-main .class-name{
    font-size: 1.5rem;
}

.result-unknown .class-name{
    font-size: 1.4rem;
}

[data-testid="block-container"]{
    padding-left: 1rem;
    padding-right: 1rem;
}

}

</style>
""", unsafe_allow_html=True)

# ── Kelas anorganik & info daur ulang ────────────────────────────────────────
CLASS_INFO = {
    "Baterai": {
        "icon": "🔋",
        "bahaya": True,
        "cara_daur_ulang": "Bawa ke drop-box baterai di minimarket atau mall. JANGAN dibuang ke tempat sampah biasa karena mengandung logam berat berbahaya (merkuri, kadmium, timbal).",
        "tips": [
            "Simpan di wadah tertutup sebelum dikumpulkan",
            "Cari drop-box di Indomaret, Alfamart, atau kantor pos terdekat",
            "1 baterai AA bisa mencemari 1 m³ tanah selama 50 tahun"
        ],
        "warna_sortir": "Merah (B3 - Bahan Berbahaya Beracun)"
    },
    "Botol Kaca": {
        "icon": "🍾",
        "bahaya": False,
        "cara_daur_ulang": "Bersihkan dan pisahkan dari sampah lain. Bisa dijual ke pelapak atau bank sampah. Kaca dapat didaur ulang 100% tanpa degradasi kualitas.",
        "tips": [
            "Cuci bersih sebelum dibuang",
            "Lepas tutup plastik/logam terlebih dahulu",
            "Pecahan kaca: bungkus koran sebelum dibuang agar tidak melukai"
        ],
        "warna_sortir": "Putih / transparan untuk kaca bening, hijau untuk kaca berwarna"
    },
    "Botol Plastik": {
        "icon": "🧴",
        "bahaya": False,
        "cara_daur_ulang": "Cuci, gepeng, kumpulkan. Plastik PET (kode 1) dan HDPE (kode 2) paling mudah didaur ulang menjadi serat polyester atau pipa.",
        "tips": [
            "Cek kode segitiga di bawah botol: 1 (PET) dan 2 (HDPE) paling bernilai",
            "Lepas label dan tutup botol (beda jenis plastik)",
            "10 botol PET = 1 kaos polyester daur ulang"
        ],
        "warna_sortir": "Kuning (plastik)"
    },
    "Elektronik": {
        "icon": "💻",
        "bahaya": True,
        "cara_daur_ulang": "Kumpulkan di program e-waste resmi. Jangan dibakar. Banyak produsen elektronik memiliki program trade-in atau drop-off resmi.",
        "tips": [
            "Hapus data sebelum menyerahkan",
            "Cari program 'take-back' dari brand HP, Samsung, Asus, dll",
            "1 ton HP bekas mengandung 200-300g emas — lebih kaya dari bijih tambang"
        ],
        "warna_sortir": "Merah (B3)"
    },
    "Kardus": {
        "icon": "📦",
        "bahaya": False,
        "cara_daur_ulang": "Lipat rata, simpan kering. Kardus adalah salah satu material paling mudah dan menguntungkan untuk didaur ulang menjadi kardus baru.",
        "tips": [
            "Pastikan kering — kardus basah tidak bisa didaur ulang",
            "Lepas selotip dan staples sebelum dijual",
            "Daur ulang kardus menghemat 17 pohon per ton"
        ],
        "warna_sortir": "Biru (kertas & kardus)"
    },
    "Kertas": {
        "icon": "📄",
        "bahaya": False,
        "cara_daur_ulang": "Kumpulkan dan jual ke bank sampah atau pelapak kertas. Hindari kertas berminyak (bekas makanan) karena susah didaur ulang.",
        "tips": [
            "Kertas HVS, koran, majalah = mudah didaur ulang",
            "Kertas bekas makanan berminyak → sulit, sebaiknya ke kompos",
            "Rata-rata orang Indonesia menghasilkan 10 kg sampah kertas/tahun"
        ],
        "warna_sortir": "Biru (kertas & kardus)"
    },
    "Logam": {
        "icon": "🔧",
        "bahaya": False,
        "cara_daur_ulang": "Kumpulkan dan jual ke tukang loak atau pengepul besi. Logam memiliki nilai jual tertinggi di antara sampah anorganik.",
        "tips": [
            "Kaleng aluminium adalah sampah paling bernilai per kg",
            "Pisahkan aluminium (kaleng minuman) dari besi/baja (kaleng makanan)",
            "Daur ulang aluminium hemat 95% energi dibanding tambang baru"
        ],
        "warna_sortir": "Abu-abu (logam)"
    },
    "Plastik": {
        "icon": "🛍️",
        "bahaya": False,
        "cara_daur_ulang": "Pisahkan berdasarkan kode resin (1-7 di bawah produk). Bawa ke bank sampah atau kumpulkan untuk dijual ke pengepul plastik.",
        "tips": [
            "Plastik kode 3 (PVC), 6 (PS/styrofoam), 7 (campuran) sulit didaur ulang",
            "Kantong plastik tipis: kembalikan ke supermarket yang punya kotak pengumpulan",
            "Styrofoam: cari pengepul khusus di kota besar"
        ],
        "warna_sortir": "Kuning (plastik)"
    },
    "Sepatu": {
        "icon": "👟",
        "bahaya": False,
        "cara_daur_ulang": "Jika masih layak pakai, donasikan. Jika rusak, cari program recycle sepatu (Nike Reuse-a-Shoe, dll) atau bawa ke bank sampah khusus tekstil.",
        "tips": [
            "Sepatu masih bagus → donasikan ke yayasan sosial",
            "Sepatu rusak → program daur ulang karet/sol",
            "Jangan campur dengan sampah umum — sulit terurai"
        ],
        "warna_sortir": "Kuning (campuran non-organik)"
    },
}

# Default untuk kelas yang tidak ada di dict di atas
DEFAULT_INFO = {
    "icon": "♻️",
    "bahaya": False,
    "cara_daur_ulang": "Pisahkan dari sampah organik dan kumpulkan di bank sampah terdekat.",
    "tips": ["Pisahkan dari sampah basah", "Kumpulkan dan jual ke pelapak", "Cari bank sampah terdekat di aplikasi SIPSN"],
    "warna_sortir": "Kuning (anorganik umum)"
}

CONFIDENCE_THRESHOLD = 0.65  # default

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
@st.cache_resource(show_spinner=False)
def load_model():
    """Load model TF/Keras. Fallback ke mock jika belum ada."""
    try:
        import tensorflow as tf
        for path in [
            "model_anorganik_terbaik.h5",
        ]:
            if os.path.exists(path):
                model = tf.keras.models.load_model(path, compile=False)
                return model, "tensorflow"
        return None, "mock"
    except ImportError:
        return None, "mock"

def predict_image(img_pil, model, backend, threshold):
    """Prediksi gambar, kembalikan (predicted_class, confidence, all_probs)."""
    from tensorflow.keras.applications.densenet import preprocess_input
    import tensorflow as tf

    CLASS_NAMES = sorted(CLASS_INFO.keys())

    if backend == "mock":
        # Mock untuk demo tanpa model
        time.sleep(0.8)
        probs = np.random.dirichlet(np.ones(len(CLASS_NAMES)) * 0.5)
        idx = np.argmax(probs)
        conf = float(probs[idx])
        if conf < threshold:
            return "Tidak Teridentifikasi", conf, dict(zip(CLASS_NAMES, probs.tolist()))
        return CLASS_NAMES[idx], conf, dict(zip(CLASS_NAMES, probs.tolist()))

    # TF inference
    img = img_pil.resize((224, 224)).convert("RGB")
    arr = np.array(img, dtype=np.float32)
    arr = preprocess_input(arr)
    arr = np.expand_dims(arr, 0)

    preds = model.predict(arr, verbose=0)[0]
    idx = int(np.argmax(preds))
    conf = float(preds[idx])

    CLASS_NAMES_MODEL = sorted(CLASS_INFO.keys())  # harus sama urutan saat training
    all_probs = dict(zip(CLASS_NAMES_MODEL, preds.tolist()))

    if conf < threshold:
        return "Tidak Teridentifikasi", conf, all_probs
    return CLASS_NAMES_MODEL[idx], conf, all_probs

# ── App ───────────────────────────────────────────────────────────────────────
def main():
    # Hero header
    st.markdown("""
    <div class="hero">
        <h1>♻️ SampahCerdas</h1>
        <p>Foto sampahmu → kami identifikasi jenis & cara daur ulangnya</p>
    </div>
    """, unsafe_allow_html=True)

    # Statistik Ringkas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">10</div>
            <div class="metric-label">Jenis Sampah</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">95%</div>
            <div class="metric-label">Akurasi Model</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-number">AI</div>
            <div class="metric-label">DenseNet121</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Load model (with nice spinner)
    with st.spinner("Memuat model AI..."):
        model, backend = load_model()

    if backend == "mock":
        st.info("ℹ️ Model belum ditemukan — berjalan dalam mode demo. Upload file model `.h5` atau folder `model_densenet121_anorganik_saved` ke direktori yang sama.", icon="ℹ️")

    # ── Sidebar settings ──────────────────────────────────────────────────────
    # ── Sidebar Info ──────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ℹ️ Pusat Informasi")
        st.markdown("**Mengapa ada 'Tidak Teridentifikasi'?**")
        st.markdown("""
Model hanya dilatih dengan **sampah anorganik**.
Jika kamu memfoto sampah organik (sisa makanan, daun, dll)
atau benda lain yang bukan sampah, model tidak akan
memaksakan prediksi yang salah.

> Sampah organik langsung bisa dijadikan kompos — tidak perlu diklasifikasikan lebih lanjut.
        """)
        st.markdown("---")
        st.markdown("**Kelas yang dikenali:**")
        for k, v in CLASS_INFO.items():
            st.markdown(f"- {v['icon']} {k}")

    threshold = CONFIDENCE_THRESHOLD

    # ── Upload / Kamera ───────────────────────────────────────────────────────
    tab1, tab2 = st.tabs(["📤 Upload Foto", "📷 Kamera HP"])

    img_input = None
    with tab1:
        uploaded = st.file_uploader(
            "Pilih foto sampah",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed"
        )
        if uploaded:
            img_input = Image.open(uploaded)

    with tab2:
        camera = st.camera_input("Ambil foto sampah", label_visibility="collapsed")
        if camera:
            img_input = Image.open(camera)

    if img_input is None:
        st.markdown("""
        <div class="card" style="text-align:center; color:#6b7280; padding: 2.5rem 1.5rem;">
            <div style="font-size:3rem; margin-bottom:0.5rem;">📸</div>
            <div style="font-size:1rem; font-weight:500; margin-bottom:0.4rem;">Upload foto atau gunakan kamera</div>
            <div style="font-size:0.85rem;">Foto yang jelas dan terang menghasilkan prediksi lebih akurat</div>
        </div>
        """, unsafe_allow_html=True)

        # Contoh sampah yang bisa dideteksi
        st.markdown("##### Contoh yang bisa dideteksi:")
        cols = st.columns(3)
        examples = [
            ("🔋", "Baterai bekas"),
            ("🧴", "Botol plastik"),
            ("📦", "Kardus"),
            ("💻", "Elektronik"),
            ("🔧", "Logam/kaleng"),
            ("📄", "Kertas/koran"),
        ]
        for i, (icon, label) in enumerate(examples):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background:white;border:1px solid #e9ecef;border-radius:12px;
                padding:0.8rem;text-align:center;margin-bottom:8px;">
                    <div style="font-size:1.8rem">{icon}</div>
                    <div style="font-size:0.8rem;color:#374151;margin-top:4px">{label}</div>
                </div>
                """, unsafe_allow_html=True)
        return

    # ── Preview foto ──────────────────────────────────────────────────────────
    col_img, col_btn = st.columns([3, 1])
    with col_img:
        st.image(img_input, use_container_width=True, caption="Foto yang akan dianalisis")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        do_predict = st.button("🔍 Analisis", use_container_width=True)

    if not do_predict:
        return

    # ── Prediksi ──────────────────────────────────────────────────────────────
    with st.spinner("Menganalisis gambar..."):
        try:
            pred_class, confidence, all_probs = predict_image(
                img_input, model, backend, threshold
            )
        except Exception as e:
            st.error(f"Gagal memproses gambar: {e}")
            return

    # ── Hasil ─────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔎 Hasil Analisis")

    identified = pred_class != "Tidak Teridentifikasi"

    if identified:
        info = CLASS_INFO.get(pred_class, DEFAULT_INFO)
        st.markdown(f"""
        <div class="result-main">
            <div style="font-size:3rem">{info['icon']}</div>
            <div class="class-name">{pred_class}</div>
            <div class="confidence">Kepercayaan model: {confidence*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        # Bar kepercayaan
        bar_color = "#10b981" if confidence >= 0.85 else "#f59e0b" if confidence >= 0.70 else "#ef4444"
        st.markdown(f"""
        <div class="conf-bar-wrap">
            <div class="conf-bar-label"><span>Tingkat kepercayaan</span><span>{confidence*100:.1f}%</span></div>
            <div class="conf-bar-bg">
                <div class="conf-bar-fill" style="width:{confidence*100:.1f}%;background:{bar_color}"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if info.get("bahaya"):
            st.markdown("""
            <div class="tip-box-warn">
            ⚠️ <strong>Sampah B3 (Bahan Berbahaya & Beracun)</strong> — jangan buang sembarangan!
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="tip-box">
        ♻️ <strong>Cara daur ulang:</strong><br>{info['cara_daur_ulang']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="tip-box-info">
        🏷️ <strong>Warna tempat sampah:</strong> {info['warna_sortir']}
        </div>
        """, unsafe_allow_html=True)

        with st.expander("💡 Tips lebih lanjut"):
            for tip in info["tips"]:
                st.markdown(f"- {tip}")

    else:
        # Tidak teridentifikasi
        st.markdown(f"""
        <div class="result-unknown">
            <div style="font-size:3rem">🤔</div>
            <div class="class-name">Tidak Teridentifikasi</div>
            <div class="confidence">Kepercayaan tertinggi: {confidence*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="tip-box-warn">
        Model tidak cukup yakin untuk mengklasifikasikan gambar ini sebagai sampah anorganik.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Kemungkinan ini adalah:**")
        st.markdown("""
        - 🌿 **Sampah organik** (sisa makanan, sayuran, daun, ranting) → langsung bisa dijadikan **kompos** atau **biogas**
        - 🏠 **Bukan sampah** (tanah, batu, barang masih terpakai)
        - 📷 **Foto kurang jelas** (terlalu gelap, blur, atau sudut terlalu jauh)
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="tip-box">
            🌱 <strong>Kalau ini organik:</strong><br>
            Masukkan ke komposter atau titip ke bank sampah organik terdekat.
            Jangan campur dengan plastik/kertas!
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="tip-box-info">
            📸 <strong>Foto kurang jelas?</strong><br>
            Coba foto ulang dengan pencahayaan lebih baik, lebih dekat,
            atau turunkan threshold di sidebar.
            </div>
            """, unsafe_allow_html=True)

    # ── Top-3 prediksi (selalu tampil) ───────────────────────────────────────
    with st.expander("📊 Lihat probabilitas semua kelas"):
        sorted_probs = sorted(all_probs.items(), key=lambda x: x[1], reverse=True)
        for cls, prob in sorted_probs:
            info_c = CLASS_INFO.get(cls, DEFAULT_INFO)
            bar_w = prob * 100
            bar_col = "#10b981" if prob >= 0.7 else "#94a3b8"
            st.markdown(f"""
            <div style="margin-bottom:8px">
                <div style="display:flex;justify-content:space-between;font-size:0.82rem;color:#374151;margin-bottom:3px">
                    <span>{info_c['icon']} {cls}</span>
                    <span style="color:#6b7280">{prob*100:.1f}%</span>
                </div>
                <div style="background:#e5e7eb;border-radius:999px;height:6px;overflow:hidden">
                    <div style="width:{bar_w:.1f}%;height:100%;background:{bar_col};border-radius:999px"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Bank sampah ───────────────────────────────────────────────────────────
    with st.expander("📍 Cara temukan bank sampah terdekat"):
        st.markdown("""
        **Aplikasi & website resmi:**
        - 🌐 [SIPSN Kementerian LHK](https://sipsn.menlhk.go.id) — cari TPS & bank sampah
        - 📱 **Rekosistem** (iOS/Android) — layanan jemput sampah anorganik
        - 📱 **Waste4Change** — khusus e-waste & B3
        - 📱 **Rapel** — jual sampah anorganik dengan jemput gratis

        **Tips:**
        > Ketik *"bank sampah + nama kotamu"* di Google Maps untuk lokasi terdekat.
        """)

    st.markdown("""
    <div class="footer">
        SampahCerdas v1.0 · Model: DenseNet121 · Dataset: Anorganik<br>
        Dibuat untuk mendukung pengelolaan sampah yang lebih baik 🌍
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
