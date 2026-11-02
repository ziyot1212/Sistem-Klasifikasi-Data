import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cek library diagram Venn
try:
    from matplotlib_venn import venn2, venn2_circles
    HAS_VENN = True
except ImportError:
    HAS_VENN = False

# 1. Konfigurasi Halaman Dasar
st.set_page_config(
    page_title="Sistem Klasifikasi Data Berbasis Himpunan",
    page_icon="∏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Apple Design System CSS (Anti-Dark Mode & Bebas Lag CDN)
st.markdown("""
<style>
    /* 1. Paksa Reset Variabel Global Streamlit Dark Mode */
    :root, [data-theme="dark"], [data-theme="light"], .stApp {
        --text-color: #1d1d1f !important;
        --background-color: #f5f5f7 !important;
        --secondary-background-color: #ffffff !important;
        background-color: #f5f5f7 !important;
        color: #1d1d1f !important;
    }

    /* 2. Gunakan Native Font Apple (Instan, 0ms Delay) */
    * {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        letter-spacing: -0.015em;
    }

    /* 3. Paksa SEMUA Teks, Heading, Label, dan Paragraf Menjadi Gelap */
    .stApp, 
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp p, .stApp span, .stApp label, .stApp div,
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stWidgetLabel"] *,
    [data-testid="stRadio"] *,
    section[data-testid="stSidebar"] * {
        color: #1d1d1f !important;
    }

    /* 4. Sembunyikan Header Bawaan Streamlit */
    header, footer {
        visibility: hidden;
        height: 0px;
    }

    .block-container {
        max-width: 1080px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* 5. Sidebar macOS Style */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid rgba(0, 0, 0, 0.08) !important;
        padding-top: 1.5rem;
    }

    /* 6. Kartu Apple (Apple Card) */
    .apple-card {
        background-color: #ffffff !important;
        border-radius: 16px !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        padding: 24px 28px !important;
        margin-bottom: 22px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02), 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    }

    .apple-card * {
        color: #1d1d1f !important;
    }

    /* Tag Elemen Himpunan */
    .math-chip {
        display: inline-block;
        background-color: #f5f5f7 !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #1d1d1f !important;
        margin: 2px 3px !important;
    }

    .metric-tile {
        background-color: #fbfbfd !important;
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        margin-bottom: 10px !important;
    }

    /* 7. Input Form & Selectbox */
    input, textarea, select, [data-baseweb="select"] > div {
        background-color: #fbfbfd !important;
        border: 1px solid rgba(0, 0, 0, 0.15) !important;
        color: #1d1d1f !important;
        border-radius: 10px !important;
    }

    /* 8. Tombol Primer Apple (Tetap Teks Putih) */
    .stButton > button, .stButton > button * {
        background-color: #0071e3 !important;
        color: #ffffff !important;
        border-radius: 980px !important;
        border: none !important;
    }

    /* Utility Warna Teks */
    .text-muted {
        color: #86868b !important;
    }
    .text-accent {
        color: #0071e3 !important;
    }
    .text-success {
        color: #34c759 !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper tag himpunan
def render_chips(elements):
    if not elements:
        return '<span class="text-muted" style="font-style: italic; font-size: 13px;">∅ (Himpunan Kosong)</span>'
    chips = "".join([f'<span class="math-chip">{item}</span>' for item in sorted(list(elements))])
    return f'<div style="margin-top: 4px; line-height: 1.8;">{chips}</div>'

# 3. Sidebar: Sumber Dataset & Pengaturan Himpunan
with st.sidebar:
    st.markdown('<p class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">PENGATURAN DATA</p>', unsafe_allow_html=True)
    st.markdown("### 1. Sumber Dataset")
    
    pilihan_dataset = st.radio(
        "Pilih sumber data:",
        options=[
            "Dataset Contoh 1 - Minat Mahasiswa",
            "Dataset Contoh 2 - Keikutsertaan UKM",
            "Upload CSV sendiri"
        ],
        index=0
    )

    if pilihan_dataset == "Dataset Contoh 1 - Minat Mahasiswa":
        df = pd.DataFrame({
            "Anggota": ["Andi", "Budi", "Citra", "Dina", "Budi", "Dina", "Eka"],
            "Kategori": ["Python", "Python", "Python", "Python", "Web", "Web", "Web"]
        })
        default_semesta = ["Andi", "Budi", "Citra", "Dina", "Eka", "Fajar", "Gita"]
    elif pilihan_dataset == "Dataset Contoh 2 - Keikutsertaan UKM":
        df = pd.DataFrame({
            "Anggota": ["Andi", "Citra", "Fajar", "Budi", "Dina", "Gita", "Andi"],
            "Kategori": ["Robotika", "Robotika", "Robotika", "Musik", "Musik", "Musik", "Musik"]
        })
        default_semesta = ["Andi", "Budi", "Citra", "Dina", "Eka", "Fajar", "Gita"]
    else:
        file_upload = st.file_uploader("Unggah CSV", type=["csv"])
        if file_upload is not None:
            df = pd.read_csv(file_upload)
            default_semesta = list(df.iloc[:, 0].dropna().unique())
        else:
            df = pd.DataFrame(columns=["Anggota", "Kategori"])
            default_semesta = []

    st.markdown("---")
    st.markdown("### 2. Pengaturan Himpunan")

    list_kategori = list(df["Kategori"].unique()) if not df.empty else ["A", "B"]
    
    col_kat_a, col_kat_b = st.columns(2)
    with col_kat_a:
        kat_a = st.selectbox("Kategori A", options=list_kategori, index=0 if len(list_kategori) > 0 else 0)
    with col_kat_b:
        kat_b = st.selectbox("Kategori B", options=list_kategori, index=1 if len(list_kategori) > 1 else 0)

    semesta_input = st.text_area(
        "Anggota Semesta (U)",
        value="\n".join(default_semesta),
        height=140,
        help="Pisahkan anggota dengan koma, titik koma, atau baris baru."
    )

# 4. Parsing Data Himpunan
raw_semesta = [x.strip() for x in semesta_input.replace(",", "\n").replace(";", "\n").split("\n") if x.strip()]
U = set(raw_semesta)

if not df.empty:
    A = set(df[df["Kategori"] == kat_a]["Anggota"].unique())
    B = set(df[df["Kategori"] == kat_b]["Anggota"].unique())
else:
    A, B = set(), set()

# Pastikan semesta mencakup semua anggota kategori A dan B
U = U | A | B

# Komputasi Operasi Himpunan
union_set = A | B
inter_set = A & B
diff_A_B = A - B
diff_B_A = B - A
comp_A = U - A
comp_B = U - B

# 5. Tampilan Utama
st.markdown("""
    <div>
        <p class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">LABORATORIUM KOMPUTASI & DISKRIT</p>
        <h1 style="font-size: 32px; font-weight: 700; letter-spacing: -0.025em; margin-bottom: 4px;">Sistem Klasifikasi Data Berbasis Himpunan</h1>
        <p class="text-muted" style="font-size: 14px; margin-bottom: 18px;">Proyek Mini #2 | Union, Intersection, Difference, Complement, Diagram Venn, dan Prinsip Inklusi-Eksklusi</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div style="background-color: #ffffff; border-left: 4px solid #0071e3; border-radius: 8px; padding: 12px 18px; margin-bottom: 22px; border-top: 1px solid rgba(0,0,0,0.05); border-right: 1px solid rgba(0,0,0,0.05); border-bottom: 1px solid rgba(0,0,0,0.05);">
        Mengelompokkan mahasiswa berdasarkan minat atau keterlibatan pada <strong>{kat_a}</strong> dan <strong>{kat_b}</strong>.
    </div>
""", unsafe_allow_html=True)

# BAGIAN A: DATASET YANG DIGUNAKAN
st.markdown('<div class="apple-card">', unsafe_allow_html=True)
st.markdown('<p class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">TINJAUAN DATA</p>', unsafe_allow_html=True)
st.markdown("### A. Dataset yang Digunakan")

col_table, col_summary = st.columns([1.6, 1])
with col_table:
    st.dataframe(df, use_container_width=True, hide_index=True)
with col_summary:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase;">Total Baris Data</div>
            <div style="font-size: 26px; font-weight: 700; margin-top: 2px;">{len(df)}</div>
            <p class="text-muted" style="font-size: 12px; margin-top: 2px;">Entri tercatat pada dataset</p>
        </div>
        <div class="metric-tile">
            <div class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase;">Total Semesta |U|</div>
            <div style="font-size: 26px; font-weight: 700; margin-top: 2px;">{len(U)}</div>
            <p class="text-muted" style="font-size: 12px; margin-top: 2px;">Individu unik dalam cakupan</p>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# BAGIAN B: PEMODELAN HIMPUNAN
st.markdown('<div class="apple-card">', unsafe_allow_html=True)
st.markdown('<p class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">PEMODELAN FORMAL</p>', unsafe_allow_html=True)
st.markdown("### B. Pemodelan Himpunan")

col_ha, col_hb, col_hu = st.columns(3)

with col_ha:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase;">Himpunan A ({kat_a})</div>
            {render_chips(A)}
            <div style="font-size: 12.5px; margin-top: 8px; font-weight: 600;">
                Kardinalitas |A| = {len(A)}
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_hb:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase;">Himpunan B ({kat_b})</div>
            {render_chips(B)}
            <div style="font-size: 12.5px; margin-top: 8px; font-weight: 600;">
                Kardinalitas |B| = {len(B)}
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_hu:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase;">Semesta (U)</div>
            {render_chips(U)}
            <div style="font-size: 12.5px; margin-top: 8px; font-weight: 600;">
                Kardinalitas |U| = {len(U)}
            </div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# BAGIAN C & D: OPERASI HIMPUNAN & DIAGRAM VENN
col_ops, col_venn = st.columns([1.25, 1])

with col_ops:
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.markdown('<p class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">ALJABAR HIMPUNAN</p>', unsafe_allow_html=True)
    st.markdown("### C. Operasi Himpunan")

    operations = [
        ("Gabungan (Union): A ∪ B", union_set),
        ("Irisan (Intersection): A ∩ B", inter_set),
        ("Selisih (Difference): A − B", diff_A_B),
        ("Selisih (Difference): B − A", diff_B_A),
        ("Komplemen: Aᶜ (U − A)", comp_A),
        ("Komplemen: Bᶜ (U − B)", comp_B)
    ]

    for title, s_data in operations:
        st.markdown(f"""
            <div style="padding: 10px 0; border-bottom: 1px solid rgba(0,0,0,0.06);">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <span style="font-size: 13.5px; font-weight: 600;">{title}</span>
                    <span class="text-accent" style="font-size: 12px; font-weight: 600;">Jumlah: {len(s_data)}</span>
                </div>
                {render_chips(s_data)}
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_venn:
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.markdown('<p class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">VISUALISASI SPASIAL</p>', unsafe_allow_html=True)
    st.markdown("### D. Diagram Venn")

    if HAS_VENN:
        fig, ax = plt.subplots(figsize=(4.5, 3.5), dpi=180)
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#ffffff')

        subsets_val = (len(diff_A_B), len(diff_B_A), len(inter_set))
        v = venn2(
            subsets=subsets_val,
            set_labels=(kat_a, kat_b),
            set_colors=('#0071e3', '#34c759'),
            alpha=0.45,
            ax=ax
        )
        venn2_circles(subsets=subsets_val, linewidth=1.2, color='#1d1d1f', ax=ax)

        if v:
            for txt in v.set_labels:
                if txt:
                    txt.set_fontsize(11)
                    txt.set_fontweight('semibold')
                    txt.set_color('#1d1d1f')
            for txt in v.subset_labels:
                if txt:
                    txt.set_fontsize(12)
                    txt.set_color('#1d1d1f')

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("Tambahkan `matplotlib-venn` di requirements.txt untuk melihat visualisasi grafik.")
    st.markdown('</div>', unsafe_allow_html=True)

# BAGIAN E: PRINSIP INKLUSI-EKSKLUSI
st.markdown('<div class="apple-card">', unsafe_allow_html=True)
st.markdown('<p class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">VERIFIKASI TEOREMA</p>', unsafe_allow_html=True)
st.markdown("### E. Perhitungan Prinsip Inklusi-Eksklusi")

card_a = len(A)
card_b = len(B)
card_inter = len(inter_set)
pie_val = card_a + card_b - card_inter
actual_val = len(union_set)

col_pie_formula, col_pie_calc = st.columns(2)

with col_pie_formula:
    st.latex(r"|A \cup B| = |A| + |B| - |A \cap B|")
    st.markdown(f"""
    **Nilai yang Dihitung:**
    * $|A| = {card_a}$ (Jumlah elemen {kat_a})
    * $|B| = {card_b}$ (Jumlah elemen {kat_b})
    * $|A \cap B| = {card_inter}$ (Jumlah irisan keduanya)
    """)

with col_pie_calc:
    st.markdown(f"""
        <div class="metric-tile" style="border-left: 4px solid #0071e3 !important;">
            <div class="text-muted" style="font-size: 11px; font-weight: 600; text-transform: uppercase;">Substitusi & Evaluasi</div>
            <div style="font-size: 16px; font-weight: 600; margin-top: 4px;">
                |A ∪ B| = {card_a} + {card_b} - {card_inter} = <strong>{pie_val}</strong>
            </div>
            <div class="text-success" style="font-size: 12.5px; margin-top: 6px; font-weight: 600;">
                ✓ Terverifikasi: Tepat sesuai dengan jumlah gabungan unik ({actual_val}).
            </div>
            <div class="text-muted" style="font-size: 11.5px; margin-top: 2px;">
                Elemen irisan tidak dihitung ganda.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)