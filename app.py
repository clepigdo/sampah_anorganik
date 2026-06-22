import streamlit as st
import numpy as np
from PIL import Image
import os, time

st.set_page_config(
    page_title="SampahCerdas",
    page_icon="♻",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'Instrument Sans', system-ui, sans-serif;
    font-weight: 400;
    background: #f8fafc;
    color: #0f172a;
    -webkit-font-smoothing: antialiased;
}
[data-testid="stAppViewContainer"] { background: #f8fafc; }
[data-testid="stHeader"]           { background: transparent; }
[data-testid="block-container"]    { padding-top: 2.5rem; padding-bottom: 5rem; max-width: 740px; }

/* 🔥 MENGHILANGKAN TOMBOL SIDEBAR BAWAAN STREAMLIT 🔥 */
[data-testid="collapsedControl"] { display: none !important; }
            

            

.sc-nav { display:flex; align-items:center; justify-content:space-between; margin-bottom:3rem; }
.sc-logo { font-family:'Instrument Serif',serif; font-size:1.4rem; color:#0f172a; letter-spacing:-.3px; }
.sc-logo-dot { color:#10b981; } 
.sc-badge { font-size:.7rem; font-weight:600; letter-spacing:.05em; text-transform:uppercase; color:#047857; background:#d1fae5; border:1px solid #6ee7b7; border-radius:999px; padding:4px 12px; }

.sc-title { font-family:'Instrument Serif',serif; font-size:2.9rem; font-weight:400; letter-spacing:-1.4px; line-height:1.14; color:#0f172a; margin-bottom:1rem; }
.sc-title em { font-style:italic; color:#10b981; } 
.sc-lead { font-size:.95rem; color:#475569; line-height:1.72; margin-bottom:1.8rem; } 

.sc-team { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:2.5rem; }
.sc-chip { display:inline-flex; align-items:center; gap:6px; background:white; border:1px solid #cbd5e1; border-radius:999px; padding:5px 12px 5px 6px; font-size:.8rem; color:#334155; }
.av { width:22px; height:22px; border-radius:50%; font-size:.58rem; font-weight:600; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.av1{background:#d1fae5;color:#047857} .av2{background:#dbeafe;color:#1d4ed8}
.av3{background:#fee2e2;color:#b91c1c} .av4{background:#fef3c7;color:#b45309}

/* ── HOW IT WORKS CARD ── */
.sc-steps-card { background:white; border:1px solid #cbd5e1; border-radius:16px; padding:1.2rem 1.5rem; margin-bottom:2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
.sc-steps-title { font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:1rem; }
.sc-steps-row { display:flex; flex-wrap:wrap; gap:15px; }
.sc-step-item { flex:1; min-width:140px; }
.sc-step-num { font-size:1.1rem; margin-bottom:4px; }
.sc-step-t { font-size:0.9rem; font-weight:600; color:#1e293b; }
.sc-step-d { font-size:0.8rem; color:#64748b; line-height:1.4; margin-top:2px; }

.sc-divider { height:1px; background:#e2e8f0; margin:2rem 0; }
.sc-section-label { font-size:.75rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:#64748b; margin:1.8rem 0 1rem; }

/* ── CATEGORY GRID ── */
.cat-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }
.cat-card { background:white; border:1px solid #cbd5e1; border-radius:14px; overflow:hidden; cursor:default; transition:border-color .2s, transform .15s; }
.cat-card:hover { border-color:#10b981; transform:translateY(-2px); box-shadow:0 4px 12px rgba(16,185,129,0.1); }
.cat-img { width:100%; aspect-ratio:1/1; object-fit:cover; background:#f1f5f9; display:block; }
.cat-name { font-size:.8rem; font-weight:600; color:#1e293b; }
.cat-sub  { font-size:.67rem; color:#64748b; margin-top:1px; }

/* ── RESULT ── */
.sc-result-found { background:white; border:2px solid #34d399; border-radius:20px; padding:1.8rem; margin:1.2rem 0; position:relative; overflow:hidden; box-shadow: 0 4px 20px rgba(52, 211, 153, 0.15); }
.sc-result-found::before { content:''; position:absolute; top:-40px; right:-40px; width:160px; height:160px; background:#d1fae5; border-radius:50%; opacity:.6; }
.sc-result-tag { display:inline-block; font-size:.68rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:#047857; background:#d1fae5; border-radius:999px; padding:4px 12px; margin-bottom:.9rem; }
.sc-result-ico  { font-size:2.6rem; margin-bottom:.4rem; }
.sc-result-name { font-family:'Instrument Serif',serif; font-size:2rem; color:#0f172a; letter-spacing:-.5px; margin-bottom:.3rem; font-weight:600; }
.sc-result-sub  { font-size:.9rem; color:#059669; font-weight:500; }

.sc-result-unknown { background:white; border:2px solid #fbbf24; border-radius:20px; padding:1.8rem; margin:1.2rem 0; position:relative; overflow:hidden; box-shadow: 0 4px 20px rgba(251, 191, 36, 0.15); }
.sc-result-unknown::before { content:''; position:absolute; top:-40px; right:-40px; width:160px; height:160px; background:#fef3c7; border-radius:50%; opacity:.7; }
.sc-result-unknown .sc-result-tag { color:#b45309; background:#fef3c7; }
.sc-result-unknown .sc-result-name { color:#92400e; font-weight:600; }

.sc-info-grid { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:1rem 0; }
.sc-ic { background:#f8fafc; border:1px solid #cbd5e1; border-radius:12px; padding:1rem; }
.sc-ic.full { grid-column:1/-1; }
.sc-ic-l { font-size:.67rem; font-weight:700; letter-spacing:.09em; text-transform:uppercase; color:#64748b; margin-bottom:.5rem; }
.sc-ic-v { font-size:.87rem; color:#1e293b; line-height:1.6; font-weight:500; }

.sc-b3 { display:flex; align-items:flex-start; gap:10px; background:#fef2f2; border:1px solid #fca5a5; border-radius:10px; padding:.9rem 1rem; margin:.8rem 0; font-size:.85rem; color:#b91c1c; font-weight:500; }

.sc-tip { display:flex; align-items:flex-start; gap:8px; padding:.6rem 0; border-bottom:1px solid #e2e8f0; font-size:.85rem; color:#334155; line-height:1.55; }
.sc-tip:last-child { border-bottom:none; }
.sc-tip-dot { width:6px; height:6px; border-radius:50%; background:#10b981; flex-shrink:0; margin-top:7px; }

.sc-empty { background:white; border:1px solid #cbd5e1; border-radius:16px; padding:2.5rem 2rem; text-align:center; margin:1rem 0; }
.sc-empty-ico { font-size:2.2rem; margin-bottom:.7rem; opacity:.8; }
.sc-empty-t { font-size:.94rem; font-weight:600; color:#1e293b; margin-bottom:.3rem; }
.sc-empty-s { font-size:.85rem; color:#64748b; }

.sc-footer { margin-top:4rem; padding-top:1.5rem; border-top:1px solid #e2e8f0; display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:1rem; }
.sc-footer-logo { font-family:'Instrument Serif',serif; font-size:1.1rem; color:#64748b; }
.sc-footer-logo span { color:#10b981; }
.sc-footer-meta { font-size:.74rem; color:#64748b; text-align:right; line-height:1.9; font-weight:500; }

[data-testid="stFileUploader"] { background:white; border:2px dashed #34d399; border-radius:14px; padding:.4rem; transition: border-color .2s; }
[data-testid="stFileUploader"]:hover { border-color: #10b981; }
[data-testid="stFileUploader"] section { border:none !important; background:transparent !important; }
[data-testid="stFileUploader"] * { color:#334155 !important; font-weight: 500; } 
[data-testid="stCameraInput"] { border:1px solid #cbd5e1 !important; border-radius:14px; overflow:hidden; }

.stTabs [data-baseweb="tab-list"] { gap:0; background:white; border:1px solid #cbd5e1; border-radius:12px; padding:4px; }
.stTabs [data-baseweb="tab"] { background:transparent; border:none; border-radius:9px; color:#64748b !important; font-size:.88rem; font-weight:600; padding:9px 20px; transition:all .2s; }
.stTabs [aria-selected="true"] { background:#ecfdf5 !important; color:#047857 !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }

div.stButton > button { width:100%; height:50px; background:#10b981; color:white !important; border:none; border-radius:10px; font-family:'Instrument Sans',sans-serif; font-size:.95rem; font-weight:600; transition:all .2s; box-shadow: 0 4px 10px rgba(16,185,129,0.2); }
div.stButton > button:hover { background:#059669; transform:translateY(-2px); box-shadow:0 6px 15px rgba(5,150,105,0.3); }

.streamlit-expanderHeader { background:white !important; border:1px solid #cbd5e1 !important; border-radius:10px !important; color:#334155 !important; font-size:.86rem !important; font-weight:600 !important; padding:.8rem 1rem !important; margin-top:.5rem !important; }
.streamlit-expanderContent { background:white !important; border:1px solid #cbd5e1 !important; border-top:none !important; border-radius:0 0 10px 10px !important; padding:.8rem 1rem !important; }

@media(max-width:580px){
    .sc-title{font-size:2.1rem}
    .cat-grid{grid-template-columns:repeat(2,1fr)}
    .sc-info-grid{grid-template-columns:1fr}
    .sc-footer{flex-direction:column}
    .sc-footer-meta{text-align:left}
}
</style>
""", unsafe_allow_html=True)

# ── Ilustrasi SVG per kategori (inline, tidak butuh internet) ─────────────────
CATEGORY_SVG = {
    "Baterai": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="120" fill="#f0f4f0"/>
  <rect x="28" y="38" width="64" height="44" rx="7" fill="#c8d8ca" stroke="#9ab89d" stroke-width="2"/>
  <rect x="92" y="48" width="8" height="24" rx="3" fill="#9ab89d"/>
  <rect x="20" y="48" width="8" height="24" rx="3" fill="#9ab89d"/>
  <rect x="36" y="52" width="8" height="16" rx="2" fill="#3a7a44" opacity=".7"/>
  <rect x="52" y="52" width="8" height="16" rx="2" fill="#3a7a44" opacity=".7"/>
  <rect x="68" y="52" width="8" height="16" rx="2" fill="#3a7a44" opacity=".7"/>
  <line x1="44" y1="56" x2="44" y2="64" stroke="#edf5ee" stroke-width="2" stroke-linecap="round"/>
  <text x="60" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#7a9a7d">AA / AAA</text>
</svg>""",
    "Botol Kaca": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="120" fill="#eef4f0"/>
  <path d="M50 22 L50 38 Q34 48 34 65 L34 92 Q34 98 40 98 L80 98 Q86 98 86 92 L86 65 Q86 48 70 38 L70 22 Z" fill="#a8ceb0" stroke="#7cb685" stroke-width="2" opacity=".85"/>
  <rect x="47" y="16" width="26" height="10" rx="3" fill="#9ab89d" stroke="#7cb685" stroke-width="1.5"/>
  <ellipse cx="60" cy="68" rx="16" ry="18" fill="white" opacity=".18"/>
  <path d="M46 55 Q60 50 74 55" stroke="white" stroke-width="1.5" fill="none" opacity=".4" stroke-linecap="round"/>
  <text x="60" y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#5a8a60">Kaca</text>
</svg>""",
    "Botol Plastik": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="120" fill="#eef4f8"/>
  <path d="M53 20 L53 34 Q38 42 38 60 L38 90 Q38 96 44 96 L76 96 Q82 96 82 90 L82 60 Q82 42 67 34 L67 20 Z" fill="#b8d4e8" stroke="#78aac8" stroke-width="1.5" opacity=".9"/>
  <rect x="50" y="14" width="20" height="9" rx="3" fill="#78aac8" stroke="#5890b0" stroke-width="1.5"/>
  <rect x="53" y="14" width="14" height="5" rx="2" fill="#5890b0"/>
  <ellipse cx="60" cy="62" rx="14" ry="16" fill="white" opacity=".22"/>
  <path d="M46 50 Q60 44 74 50" stroke="white" stroke-width="1.5" fill="none" opacity=".5" stroke-linecap="round"/>
  <rect x="42" y="74" width="36" height="6" rx="2" fill="white" opacity=".25"/>
  <text x="60" y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#4a80a0">PET / HDPE</text>
</svg>""",
    "Elektronik": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="120" fill="#f0f0f4"/>
  <rect x="22" y="30" width="76" height="52" rx="6" fill="#b0b8d0" stroke="#8890b0" stroke-width="1.5"/>
  <rect x="26" y="34" width="68" height="40" rx="4" fill="#d8dce8"/>
  <rect x="30" y="38" width="30" height="20" rx="3" fill="#8890b0" opacity=".6"/>
  <rect x="30" y="62" width="60" height="4" rx="2" fill="#8890b0" opacity=".35"/>
  <circle cx="74" cy="48" r="8" fill="#c0c8e0"/>
  <circle cx="74" cy="48" r="4" fill="#8890b0" opacity=".5"/>
  <rect x="44" y="82" width="32" height="6" rx="3" fill="#a0a8c0"/>
  <rect x="46" y="88" width="28" height="4" rx="2" fill="#b0b8d0"/>
  <text x="60" y="110" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#6870a0">E-Waste</text>
</svg>""",
    "Kardus": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="120" fill="#faf4ec"/>
  <path d="M20 50 L60 38 L100 50 L100 90 L60 102 L20 90 Z" fill="#d4b896" stroke="#b8986a" stroke-width="1.5"/>
  <path d="M60 38 L60 102" stroke="#b8986a" stroke-width="1" opacity=".5"/>
  <path d="M20 50 L60 38 L100 50" fill="#e8ccaa" stroke="#b8986a" stroke-width="1.5"/>
  <path d="M20 50 L60 62 L100 50" fill="#c8a87c" stroke="#b8986a" stroke-width="1"/>
  <path d="M60 62 L60 38" stroke="#b8986a" stroke-width="1"/>
  <path d="M38 56 L60 63 L82 56" stroke="#b8986a" stroke-width="1" fill="none" opacity=".5"/>
  <text x="60" y="114" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#8a6840">Kardus</text>
</svg>""",
    "Kertas": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="120" fill="#fdfaf5"/>
  <rect x="25" y="22" width="70" height="88" rx="4" fill="#f5f0e0" stroke="#d8d0b0" stroke-width="1.5" transform="rotate(-4 60 66)"/>
  <rect x="25" y="22" width="70" height="88" rx="4" fill="#faf8f0" stroke="#d8d0b0" stroke-width="1.5" transform="rotate(2 60 66)"/>
  <rect x="25" y="22" width="70" height="88" rx="4" fill="white" stroke="#d8d0b0" stroke-width="1.5"/>
  <line x1="36" y1="42" x2="84" y2="42" stroke="#d0c8a8" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="36" y1="52" x2="84" y2="52" stroke="#d0c8a8" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="36" y1="62" x2="84" y2="62" stroke="#d0c8a8" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="36" y1="72" x2="72" y2="72" stroke="#d0c8a8" stroke-width="1.5" stroke-linecap="round"/>
  <text x="60" y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#8a8060">HVS / Koran</text>
</svg>""",
    "Logam": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="120" fill="#f2f2f0"/>
  <ellipse cx="60" cy="36" rx="28" ry="8" fill="#c0c0be" stroke="#989894" stroke-width="1.5"/>
  <rect x="32" y="36" width="56" height="52" fill="#b8b8b4" stroke="#989894" stroke-width="1.5"/>
  <rect x="32" y="36" width="56" height="52" fill="url(#can-shine)" opacity=".4"/>
  <ellipse cx="60" cy="88" rx="28" ry="8" fill="#a8a8a4" stroke="#989894" stroke-width="1.5"/>
  <ellipse cx="60" cy="36" rx="20" ry="5" fill="#d0d0ce" opacity=".6"/>
  <line x1="38" y1="48" x2="82" y2="48" stroke="white" stroke-width="1" opacity=".3"/>
  <line x1="38" y1="60" x2="82" y2="60" stroke="white" stroke-width="1" opacity=".2"/>
  <line x1="38" y1="72" x2="82" y2="72" stroke="white" stroke-width="1" opacity=".2"/>
  <defs><linearGradient id="can-shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="white" stop-opacity=".5"/><stop offset="40%" stop-color="white" stop-opacity=".1"/><stop offset="100%" stop-color="white" stop-opacity="0"/></linearGradient></defs>
  <text x="60" y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#707070">Aluminium</text>
</svg>""",
    "Plastik": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="120" fill="#fef8ee"/>
  <path d="M30 38 Q28 36 32 34 L88 34 Q92 36 90 38 L84 88 Q83 94 76 94 L44 94 Q37 94 36 88 Z" fill="#f0d898" stroke="#d4b840" stroke-width="1.5"/>
  <path d="M38 34 L32 94" stroke="#d4b840" stroke-width=".8" opacity=".3"/>
  <path d="M60 34 L60 94" stroke="#d4b840" stroke-width=".8" opacity=".3"/>
  <path d="M82 34 L88 94" stroke="#d4b840" stroke-width=".8" opacity=".3"/>
  <path d="M30 52 Q60 48 90 52" stroke="#d4b840" stroke-width=".8" fill="none" opacity=".4"/>
  <path d="M31 64 Q60 60 89 64" stroke="#d4b840" stroke-width=".8" fill="none" opacity=".4"/>
  <path d="M33 76 Q60 72 87 76" stroke="#d4b840" stroke-width=".8" fill="none" opacity=".4"/>
  <path d="M26 34 Q28 28 32 28 L88 28 Q92 28 94 34 L90 38 L30 38 Z" fill="#e8c830" stroke="#d4b840" stroke-width="1.5"/>
  <text x="60" y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#8a7020">Kantong / Wrap</text>
</svg>""",
    "Sepatu": """<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="120" fill="#f4f0ee"/>
  <path d="M20 78 Q18 68 30 62 L48 42 Q54 36 62 38 L88 40 Q96 40 96 50 L96 66 Q96 72 88 74 L36 82 Q26 84 20 78 Z" fill="#c0a898" stroke="#a08878" stroke-width="1.5"/>
  <path d="M20 78 L36 82 L88 74 L96 66 L96 72 L88 80 L32 88 Q22 88 20 80 Z" fill="#a89080" stroke="#a08878" stroke-width="1"/>
  <path d="M48 42 L48 62 Q54 64 60 62 L60 40" fill="white" stroke="#a08878" stroke-width="1" opacity=".5"/>
  <path d="M64 40 L64 60 Q70 62 74 60 L74 40" fill="white" stroke="#a08878" stroke-width="1" opacity=".4"/>
  <path d="M30 62 Q32 54 40 50" stroke="#a08878" stroke-width="1.5" fill="none" opacity=".5" stroke-linecap="round"/>
  <circle cx="52" cy="52" r="2" fill="#c8b0a0" opacity=".7"/>
  <circle cx="52" cy="58" r="2" fill="#c8b0a0" opacity=".7"/>
  <circle cx="66" cy="52" r="2" fill="#c8b0a0" opacity=".7"/>
  <circle cx="66" cy="58" r="2" fill="#c8b0a0" opacity=".7"/>
  <text x="60" y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#806858">Alas kaki</text>
</svg>""",
}

# ── Data kelas ─────────────────────────────────────────────────────────────────
CLASS_INFO = {
    "Baterai":       {"icon":"🔋","bahaya":True, "bg":"#f0f4f0",
        "cara_daur_ulang":"Bawa ke drop-box baterai di minimarket atau mall. Jangan dibuang ke tempat sampah biasa — mengandung bahan kimia beracun.",
        "tips":["Simpan dalam wadah tertutup sebelum dikumpulkan","Cari drop-box di minimarket atau kantor pos","Jangan biarkan baterai bocor di tanah"],"warna_sortir":"Merah — Berbahaya"},
    "Botol Kaca":    {"icon":"🍾","bahaya":False,"bg":"#eef4f0",
        "cara_daur_ulang":"Cuci bersih, pisahkan dari sampah lain. Kaca dapat didaur ulang berkali-kali tanpa batas.",
        "tips":["Cuci sisa minuman sebelum dibuang","Lepas tutup plastik atau logamnya","Jika pecah, bungkus dengan koran agar aman"],"warna_sortir":"Putih / Hijau — Kaca"},
    "Botol Plastik": {"icon":"🧴","bahaya":False,"bg":"#eef4f8",
        "cara_daur_ulang":"Cuci bersih, remas/gepengkan agar tidak makan tempat, lalu kumpulkan.",
        "tips":["Lepas label dan tutup botol (karena beda jenis plastik)","Gepengkan botol agar mudah disimpan","Bisa ditabung di bank sampah terdekat"],"warna_sortir":"Kuning — Plastik"},
    "Elektronik":    {"icon":"💻","bahaya":True, "bg":"#f0f0f4",
        "cara_daur_ulang":"Kumpulkan di program e-waste resmi. Jangan dibakar atau dibongkar sendiri.",
        "tips":["Hapus data probadi sebelum menyerahkan HP/Laptop","Cari program tukar-tambah dari merek elektronik","Mengandung logam berat berbahaya"],"warna_sortir":"Merah — Berbahaya"},
    "Kardus":        {"icon":"📦","bahaya":False,"bg":"#faf4ec",
        "cara_daur_ulang":"Lipat rata dan simpan di tempat kering. Kardus sangat mudah didaur ulang menjadi kardus baru.",
        "tips":["Pastikan kardus tidak basah atau berminyak","Lepas selotip dan staples sebelum dikumpulkan","Lipat pipih agar rapi"],"warna_sortir":"Biru — Kertas & Kardus"},
    "Kertas":        {"icon":"📄","bahaya":False,"bg":"#fdfaf5",
        "cara_daur_ulang":"Kumpulkan kertas bekas dalam kondisi kering dan rapi untuk disetorkan ke pelapak.",
        "tips":["Kertas HVS, koran, dan majalah sangat mudah didaur ulang","Kertas bungkus makanan berminyak tidak bisa didaur ulang","Jangan biarkan kertas basah"],"warna_sortir":"Biru — Kertas & Kardus"},
    "Logam":         {"icon":"🔧","bahaya":False,"bg":"#f2f2f0",
        "cara_daur_ulang":"Kumpulkan kaleng minuman atau besi bekas. Logam adalah salah satu sampah paling bernilai tinggi.",
        "tips":["Cuci bersih sisa makanan di dalam kaleng","Kaleng minuman (aluminium) sangat bagus untuk didaur ulang","Pisahkan dari sampah basah"],"warna_sortir":"Abu-abu — Logam"},
    "Plastik":       {"icon":"🛍️","bahaya":False,"bg":"#fef8ee",
        "cara_daur_ulang":"Kumpulkan kantong kresek dan kemasan plastik bersih. Pastikan tidak bercampur sampah sisa makanan.",
        "tips":["Cuci dan keringkan kemasan plastik bekas makanan","Bawa tas belanja sendiri untuk mengurangi sampah ini","Lipat rapi sebelum dikumpulkan"],"warna_sortir":"Kuning — Plastik"},
    "Sepatu":        {"icon":"👟","bahaya":False,"bg":"#f4f0ee",
        "cara_daur_ulang":"Jika masih layak pakai, lebih baik didonasikan. Jika rusak parah, buang di tempat sampah anorganik.",
        "tips":["Donasikan sepatu yang hanya kekecilan","Ikat sepasang sepatu agar tidak terpisah","Jangan campur dengan sampah dapur basah"],"warna_sortir":"Kuning — Campuran"},
}

DEFAULT_INFO = {"icon":"♻","bahaya":False,"cara_daur_ulang":"Pisahkan dari sampah organik (basah) dan kumpulkan dengan rapi.","tips":["Pastikan sampah dalam keadaan kering","Kumpulkan di tempat sampah anorganik","Jangan buang sembarangan"],"warna_sortir":"Kuning — Anorganik"}
THRESHOLD = 0.65
TEAM = [("IR","Igdo Ragil Manuel","av1"),("F","Firnanda","av2"),("I","Ihda","av3"),("G","Goklas","av4")]

@st.cache_resource(show_spinner=False)
@st.cache_resource(show_spinner=False)
def load_model():
    try:
        import tensorflow as tf
        here = os.path.dirname(os.path.abspath(__file__))
        for name in ["model_densenet121_anorganik_best.keras","model_densenet121_anorganik_best.h5"]:
            p = os.path.join(here, name)
            if os.path.exists(p):
                return tf.keras.models.load_model(p, compile=False), "tensorflow"
        return None, "mock"
    except Exception as e:
        # 🔥 TAMPILKAN ERROR-NYA DI SINI 🔥
        st.error(f"Sistem gagal memuat model AI: {e}") 
        return None, "mock"

def predict(img_pil, model, backend, threshold):
    CLASS_NAMES = sorted(CLASS_INFO.keys())
    if backend == "mock":
        time.sleep(0.6)
        probs = np.random.dirichlet(np.ones(len(CLASS_NAMES)) * 0.5)
        idx = int(np.argmax(probs)); conf = float(probs[idx])
        return (CLASS_NAMES[idx] if conf >= threshold else "Tidak Teridentifikasi"), conf, dict(zip(CLASS_NAMES, probs.tolist()))
    from tensorflow.keras.applications.densenet import preprocess_input
    img  = img_pil.resize((224,224)).convert("RGB")
    arr  = preprocess_input(np.array(img, dtype=np.float32))
    arr  = np.expand_dims(arr, 0)
    preds = model.predict(arr, verbose=0)[0]
    idx   = int(np.argmax(preds)); conf = float(preds[idx])
    return (CLASS_NAMES[idx] if conf >= threshold else "Tidak Teridentifikasi"), conf, None

def render_category_grid():
    cols = list(CLASS_INFO.keys())
    rows = [cols[i:i+3] for i in range(0, len(cols), 3)]
    for row in rows:
        html_row = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:10px">'
        for cat in row:
            info = CLASS_INFO[cat]
            svg  = CATEGORY_SVG.get(cat, "")
            html_row += f"""
            <div style="background:white;border:1px solid #e8e4de;border-radius:14px;overflow:hidden;transition:transform .15s">
                <div style="width:100%;aspect-ratio:1/1;background:{info['bg']};display:flex;align-items:center;justify-content:center;padding:6px">
                    {svg}
                </div>
                <div style="padding:8px 10px 10px;border-top:1px solid #f0ede8">
                    <div style="font-size:.8rem;font-weight:600;color:#2c2a26">{cat}</div>
                </div>
            </div>"""
        html_row += "</div>"
        st.markdown(html_row, unsafe_allow_html=True)

def main():
    # nav
    st.markdown("""
    <div class="sc-nav">
        <div class="sc-logo">Sampah<span class="sc-logo-dot">.</span>Cerdas</div>
        <div class="sc-badge">SAMPAH ANORGANIK</div>
    </div>""", unsafe_allow_html=True)

    # hero
    chips = "".join(f'<div class="sc-chip"><div class="av {c}">{i}</div>{n}</div>' for i,n,c in TEAM)
    st.markdown(f"""
    <div class="sc-title">Cari tahu cara buang sampahmu dengan <em>benar.</em></div>
    <p class="sc-lead">Tidak yakin ini sampah apa? Cukup ambil foto, dan biarkan kami yang memberitahu jenis serta cara mendaur ulangnya agar lingkungan tetap bersih.</p>
    <div class="sc-team">{chips}</div>""", unsafe_allow_html=True)

    # ── HOW IT WORKS CARDS (PENGGANTI SIDEBAR) ──
    st.markdown("""
    <div class="sc-steps-card">
        <div class="sc-steps-title">Cara Penggunaan</div>
        <div class="sc-steps-row">
            <div class="sc-step-item">
                <div class="sc-step-num">📸</div>
                <div class="sc-step-t">1. Ambil Foto</div>
                <div class="sc-step-d">Foto jelas sampah anorganikmu.</div>
            </div>
            <div class="sc-step-item">
                <div class="sc-step-num">✨</div>
                <div class="sc-step-t">2. Klik Analisis</div>
                <div class="sc-step-d">Biarkan sistem yang mengenali.</div>
            </div>
            <div class="sc-step-item">
                <div class="sc-step-num">♻️</div>
                <div class="sc-step-t">3. Ikuti Panduan</div>
                <div class="sc-step-d">Buang sesuai petunjuk.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(""):
        model, backend = load_model()
    if backend == "mock":
        st.caption("⚙ Sistem sedang dalam mode pemeliharaan (demo).")

    tab1, tab2 = st.tabs(["  Pilih dari Galeri  ","  Gunakan Kamera  "])
    img_input  = None
    with tab1:
        up = st.file_uploader("", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
        if up: img_input = Image.open(up)
    with tab2:
        cam = st.camera_input("", label_visibility="collapsed")
        if cam: img_input = Image.open(cam)

    if img_input is None:
        st.markdown("""
        <div class="sc-empty">
            <div class="sc-empty-ico">📷</div>
            <div class="sc-empty-t">Ayo Mulai Memilah!</div>
            <div class="sc-empty-s">Upload foto sampahmu atau jepret langsung dari kamera HP</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="sc-section-label">Sampah yang bisa kami kenali:</div>', unsafe_allow_html=True)
        render_category_grid()
        _footer(); return

    c1, c2 = st.columns([3,1])
    with c1: st.image(img_input, use_container_width=True)
    with c2:
        st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
        run = st.button("Analisis Foto ✨", use_container_width=True)

    if not run: _footer(); return

    with st.spinner("Sedang melihat gambar..."):
        try:
            pred_class, conf, _ = predict(img_input, model, backend, THRESHOLD)
        except Exception as e:
            st.error("Maaf, terjadi kesalahan saat melihat foto. Coba lagi ya!"); return

    found = pred_class != "Tidak Teridentifikasi"
    info  = CLASS_INFO.get(pred_class, DEFAULT_INFO)

    st.markdown('<div class="sc-divider"></div>', unsafe_allow_html=True)

    if found:
        st.markdown(f"""
        <div class="sc-result-found">
            <div class="sc-result-tag">Sampah Dikenali!</div>
            <div class="sc-result-ico">{info['icon']}</div>
            <div class="sc-result-name">{pred_class}</div>
            <div class="sc-result-sub">✓ Kami sangat yakin dengan hasil ini.</div>
        </div>""", unsafe_allow_html=True)
        
        if info["bahaya"]:
            st.markdown('<div class="sc-b3"><span>⚠️</span><span><strong>Awas, Sampah Berbahaya!</strong> Jangan buang ini sembarangan karena bisa merusak lingkungan.</span></div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="sc-info-grid">
            <div class="sc-ic full"><div class="sc-ic-l">Langkah Terbaik</div><div class="sc-ic-v">{info['cara_daur_ulang']}</div></div>
            <div class="sc-ic"><div class="sc-ic-l">Kategori Tong Sampah</div><div class="sc-ic-v">{info['warna_sortir']}</div></div>
        </div>""", unsafe_allow_html=True)
        
        with st.expander("💡 Tips tambahan untukmu"):
            for tip in info["tips"]:
                st.markdown(f'<div class="sc-tip"><span class="sc-tip-dot"></span><span>{tip}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="sc-result-unknown">
            <div class="sc-result-tag">Hmm... Kurang Yakin</div>
            <div class="sc-result-ico">🤔</div>
            <div class="sc-result-name">Tidak Dikenali</div>
        </div>
        <div class="sc-info-grid">
            <div class="sc-ic"><div class="sc-ic-l">Apakah ini sisa makanan?</div><div class="sc-ic-v">Kalau iya, ini adalah sampah organik yang bisa dijadikan pupuk kompos yang bagus untuk tanaman.</div></div>
            <div class="sc-ic"><div class="sc-ic-l">Fotonya kurang jelas?</div><div class="sc-ic-v">Coba ambil foto lagi yang lebih terang, dekat, dan tidak terpotong.</div></div>
        </div>""", unsafe_allow_html=True)

    with st.expander("📍 Bingung cari tempat buang sampah yang benar?"):
        st.markdown("""<div class="sc-ic-v" style="line-height:2.1">
Kamu bisa menggunakan aplikasi di HP-mu untuk mencari tempat pembuangan terdekat:<br>
📱 <strong>Rekosistem</strong> — Bisa jemput sampah ke rumahmu<br>
📱 <strong>Rapel</strong> — Jual sampah bekasmu dari rumah<br><br>
<span style="color:#b0ada6">Atau ketik "bank sampah terdekat" di Google Maps.</span>
</div>""", unsafe_allow_html=True)

    _footer()

def _footer():
    st.markdown("""
    <div class="sc-footer">
        <div class="sc-footer-logo">Sampah<span>.</span>Cerdas</div>
        <div class="sc-footer-meta">Dibuat untuk lingkungan yang lebih baik 🌍<br>Igdo · Firnanda · Ihda · Goklas @ Universitas Dian Nuswantoro</div>
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()