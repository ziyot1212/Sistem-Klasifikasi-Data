import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cek ketersediaan library diagram Venn agar tidak memicu ImportError fatal
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

# 2. Styling Apple Human Interface System
st.markdown("""
<style>
    @import url('https://fonts.cdnfonts.com/css/sf-pro-display');

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Helvetica Neue", sans-serif !important;
        color: #1d1d1f;
        letter-spacing: -0.015em;
    }

    .stApp {
        background-color: #f5f5f7;
    }

    header, footer {
        visibility: hidden;
        height: 0px;
    }

    .block-container {
        max-width: 1080px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid rgba(0, 0, 0, 0.08);
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #1d1d1f;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em;
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
    }

    /* Kartu Konten Bersih */
    .apple-card {
        background-color: #ffffff;
        border-radius: 16px;
        border: 1px solid rgba(0, 0, 0, 0.07);
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02), 0 4px 12px rgba(0, 0, 0, 0.02);
    }

    .apple-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #86868b;
        margin-bottom: 6px;
    }

    .apple-title {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.025em;
        line-height: 1.2;
        color: #1d1d1f;
        margin-bottom: 4px;
    }

    .apple-subtitle {
        font-size: 14px;
        color: #86868b;
        margin-bottom: 18px;
    }

    .apple-banner {
        background-color: #ffffff;
        border-left: 4px solid #0071e3;
        border-radius: 8px;
        padding: 12px 18px;
        font-size: 14px;
        color: #1d1d1f;
        margin-bottom: 22px;
        border-top: 1px solid rgba(0, 0, 0, 0.04);
        border-right: 1px solid rgba(0, 0, 0, 0.04);
        border-bottom: 1px solid rgba(0, 0, 0, 0.04);
    }

    /* Tag Elemen Himpunan Matematika */
    .math-chip {
        display: inline-block;
        background-color: #f5f5f7;
        border: 1px solid rgba(0, 0, 0, 0.08);
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 12px;
        font-weight: 500;
        color: #1d1d1f;
        margin: 2px 3px;
        font-family: -apple-system, monospace !important;
    }

    .metric-tile {
        background-color: #fbfbfd;
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
    }

    .metric-num {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #1d1d1f;
    }

    /* Form Inputs */
    .stSelectbox > div > div, 
    .stTextArea textarea, 
    .stTextInput input {
        background-color: #fbfbfd !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0, 0, 0, 0.12) !important;
        color: #1d1d1f !important;
        font-size: 13.5px !important;
    }

    .stSelectbox > div > div:focus-within, 
    .stTextArea textarea:focus {
        border-color: #0071e3 !important;
        box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.15) !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(0, 0, 0, 0.06);
    }
</style>
""", unsafe_allow_html=True)

# Helper untuk merender tag anggota himpunan
def render_chips(elements):
    if not elements:
        return '<span style="color: #86868b; font-style: italic; font-size: 13px;">∅ (Himpunan Kosong)</span>'
    chips = "".join([f'<span class="math-chip">{item}</span>' for item in sorted(list(elements))])
    return f'<div style="margin-top: 4px; line-height: 1.8;">{chips}</div>'

# 3. Sidebar: Sumber Dataset & Pengaturan Himpunan
with st.sidebar:
    st.markdown('<p class="apple-label">Pengaturan Data</p>', unsafe_allow_html=True)
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
        <p class="apple-label">Laboratorium Komputasi & Diskrit</p>
        <h1 class="apple-title">Sistem Klasifikasi Data Berbasis Himpunan</h1>
        <p class="apple-subtitle">Proyek Mini #2 | Union, Intersection, Difference, Complement, Diagram Venn, dan Prinsip Inklusi-Eksklusi</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="apple-banner">
        Mengelompokkan mahasiswa berdasarkan minat atau keterlibatan pada <strong>{kat_a}</strong> dan <strong>{kat_b}</strong>.
    </div>
""", unsafe_allow_html=True)

# BAGIAN A: DATASET YANG DIGUNAKAN
st.markdown('<div class="apple-card">', unsafe_allow_html=True)
st.markdown('<p class="apple-label">Tinjauan Data</p>', unsafe_allow_html=True)
st.markdown("### A. Dataset yang Digunakan")

col_table, col_summary = st.columns([1.6, 1])
with col_table:
    st.dataframe(df, use_container_width=True, hide_index=True)
with col_summary:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="apple-label">Total Baris Data</div>
            <div class="metric-num">{len(df)}</div>
            <p style="color: #86868b; font-size: 12px; margin-top: 2px;">Entri tercatat pada dataset</p>
        </div>
        <div class="metric-tile">
            <div class="apple-label">Total Semesta |U|</div>
            <div class="metric-num">{len(U)}</div>
            <p style="color: #86868b; font-size: 12px; margin-top: 2px;">Individu unik dalam cakupan</p>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# BAGIAN B: PEMODELAN HIMPUNAN
st.markdown('<div class="apple-card">', unsafe_allow_html=True)
st.markdown('<p class="apple-label">Pemodelan Formal</p>', unsafe_allow_html=True)
st.markdown("### B. Pemodelan Himpunan")

col_ha, col_hb, col_hu = st.columns(3)

with col_ha:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="apple-label">Himpunan A ({kat_a})</div>
            {render_chips(A)}
            <div style="font-size: 12.5px; color: #1d1d1f; margin-top: 8px; font-weight: 600;">
                Kardinalitas |A| = {len(A)}
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_hb:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="apple-label">Himpunan B ({kat_b})</div>
            {render_chips(B)}
            <div style="font-size: 12.5px; color: #1d1d1f; margin-top: 8px; font-weight: 600;">
                Kardinalitas |B| = {len(B)}
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_hu:
    st.markdown(f"""
        <div class="metric-tile">
            <div class="apple-label">Semesta (U)</div>
            {render_chips(U)}
            <div style="font-size: 12.5px; color: #1d1d1f; margin-top: 8px; font-weight: 600;">
                Kardinalitas |U| = {len(U)}
            </div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# BAGIAN C & D: OPERASI HIMPUNAN & DIAGRAM VENN
col_ops, col_venn = st.columns([1.25, 1])

with col_ops:
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.markdown('<p class="apple-label">Aljabar Himpunan</p>', unsafe_allow_html=True)
    st.markdown("### C. Operasi Himpunan")

    operations = [
        (f"Gabungan (Union): A ∪ B", union_set),
        (f"Irisan (Intersection): A ∩ B", inter_set),
        (f"Selisih (Difference): A − B", diff_A_B),
        (f"Selisih (Difference): B − A", diff_B_A),
        ("Komplemen: Aᶜ (U − A)", comp_A),
        ("Komplemen: Bᶜ (U − B)", comp_B)
    ]

    for title, s_data in operations:
        st.markdown(f"""
            <div style="padding: 10px 0; border-bottom: 1px solid rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <span style="font-size: 13.5px; font-weight: 600; color: #1d1d1f;">{title}</span>
                    <span style="font-size: 12px; font-weight: 600; color: #0071e3;">Jumlah: {len(s_data)}</span>
                </div>
                {render_chips(s_data)}
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_venn:
    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.markdown('<p class="apple-label">Visualisasi Spasial</p>', unsafe_allow_html=True)
    st.markdown("### D. Diagram Venn")

    if HAS_VENN:
        fig, ax = plt.subplots(figsize=(4.8, 3.8), dpi=300)
        fig.patch.set_facecolor('#ffffff')
        ax.set_facecolor('#ffffff')

        subsets_val = (len(diff_A_B), len(diff_B_A), len(inter_set))
        v = venn2(
            subsets=subsets_val,
            set_labels=(kat_a, kat_b),
            set_colors=('#0071e3', '#34c759'),
            alpha=0.42,
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
        st.info("Pustaka diagram belum terpasang. Jalankan: `pip install matplotlib-venn` di terminal.")
    st.markdown('</div>', unsafe_allow_html=True)

# BAGIAN E: PRINSIP INKLUSI-EKSKLUSI
st.markdown('<div class="apple-card">', unsafe_allow_html=True)
st.markdown('<p class="apple-label">Verifikasi Teorema</p>', unsafe_allow_html=True)
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
        <div class="metric-tile" style="border-left: 4px solid #0071e3;">
            <div class="apple-label">Substitusi & Evaluasi</div>
            <div style="font-size: 16px; font-weight: 600; color: #1d1d1f; margin-top: 4px;">
                |A ∪ B| = {card_a} + {card_b} - {card_inter} = <strong>{pie_val}</strong>
            </div>
            <div style="font-size: 12.5px; color: #34c759; margin-top: 6px; font-weight: 600;">
                ✓ Terverifikasi: Tepat sesuai dengan jumlah gabungan unik ({actual_val}).
            </div>
            <div style="font-size: 11.5px; color: #86868b; margin-top: 2px;">
                Elemen irisan tidak dihitung ganda.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)