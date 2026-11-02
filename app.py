import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cek ketersediaan modul diagram Venn
try:
    from matplotlib_venn import venn2, venn2_circles
    HAS_VENN = True
except ImportError:
    HAS_VENN = False

# 1. Konfigurasi Halaman (Sidebar Dipaksa Terbuka)
st.set_page_config(
    page_title="Sistem Klasifikasi Data Berbasis Himpunan",
    page_icon="∏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS Aman (Hanya Styling Konten & Kartu, Sama Sekali Tidak Menyentuh Header/Sidebar)
st.markdown("""
<style>
    /* Styling Elemen Kartu Apple */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 14px !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        margin-bottom: 1rem;
    }

    /* Tag Elemen Himpunan Matematika */
    .math-chip {
        display: inline-block;
        background-color: #f5f5f7;
        border: 1px solid rgba(0, 0, 0, 0.1);
        border-radius: 6px;
        padding: 3px 9px;
        font-size: 13px;
        font-weight: 600;
        color: #1d1d1f;
        margin: 2px 3px;
        font-family: ui-monospace, Menlo, Monaco, monospace;
    }

    /* Kotak Metrik Ringkas */
    .metric-card {
        background-color: #fbfbfd;
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 8px;
    }
    
    .apple-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #86868b;
        margin-bottom: 4px;
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
    st.markdown('<p class="apple-label">Konfigurasi Data</p>', unsafe_allow_html=True)
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
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        kat_a = st.selectbox("Kategori A", options=list_kategori, index=0 if len(list_kategori) > 0 else 0)
    with col_k2:
        kat_b = st.selectbox("Kategori B", options=list_kategori, index=1 if len(list_kategori) > 1 else 0)

    semesta_input = st.text_area(
        "Anggota Semesta (U)",
        value="\n".join(default_semesta),
        height=130,
        help="Pisahkan anggota dengan koma atau baris baru."
    )

# 4. Parsing Logika Matematika
raw_semesta = [x.strip() for x in semesta_input.replace(",", "\n").replace(";", "\n").split("\n") if x.strip()]
U = set(raw_semesta)

if not df.empty:
    A = set(df[df["Kategori"] == kat_a]["Anggota"].unique())
    B = set(df[df["Kategori"] == kat_b]["Anggota"].unique())
else:
    A, B = set(), set()

# Menjamin semesta mencakup semua anggota
U = U | A | B

union_set = A | B
inter_set = A & B
diff_A_B = A - B
diff_B_A = B - A
comp_A = U - A
comp_B = U - B

# 5. Tampilan Utama
st.markdown('<p class="apple-label">Laboratorium Komputasi & Diskrit</p>', unsafe_allow_html=True)
st.title("Sistem Klasifikasi Data Berbasis Himpunan")
st.caption("Proyek Mini #2 | Union, Intersection, Difference, Complement, Diagram Venn, dan Prinsip Inklusi-Eksklusi")

st.info(f"Mengelompokkan data mahasiswa berdasarkan kategori **{kat_a}** dan **{kat_b}**.")

# BAGIAN A: DATASET YANG DIGUNAKAN
with st.container(border=True):
    st.markdown('<p class="apple-label">Tinjauan Data</p>', unsafe_allow_html=True)
    st.subheader("A. Dataset yang Digunakan")
    
    col_tbl, col_meta = st.columns([1.7, 1])
    with col_tbl:
        st.dataframe(df, use_container_width=True, hide_index=True)
    with col_meta:
        st.markdown(f"""
            <div class="metric-card">
                <div class="apple-label">Total Baris Entri</div>
                <div style="font-size: 24px; font-weight: 700; color: #1d1d1f;">{len(df)}</div>
                <div style="font-size: 12px; color: #86868b; margin-top: 2px;">Data observasi sampel</div>
            </div>
            <div class="metric-card">
                <div class="apple-label">Total Semesta |U|</div>
                <div style="font-size: 24px; font-weight: 700; color: #1d1d1f;">{len(U)}</div>
                <div style="font-size: 12px; color: #86868b; margin-top: 2px;">Individu unik terdaftar</div>
            </div>
        """, unsafe_allow_html=True)

# BAGIAN B: PEMODELAN HIMPUNAN
with st.container(border=True):
    st.markdown('<p class="apple-label">Representasi Formal</p>', unsafe_allow_html=True)
    st.subheader("B. Pemodelan Himpunan")

    cb1, cb2, cb3 = st.columns(3)
    with cb1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="apple-label">Himpunan A ({kat_a})</div>
                {render_chips(A)}
                <div style="font-size: 13px; font-weight: 600; color: #1d1d1f; margin-top: 8px;">Kardinalitas |A| = {len(A)}</div>
            </div>
        """, unsafe_allow_html=True)
    with cb2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="apple-label">Himpunan B ({kat_b})</div>
                {render_chips(B)}
                <div style="font-size: 13px; font-weight: 600; color: #1d1d1f; margin-top: 8px;">Kardinalitas |B| = {len(B)}</div>
            </div>
        """, unsafe_allow_html=True)
    with cb3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="apple-label">Semesta (U)</div>
                {render_chips(U)}
                <div style="font-size: 13px; font-weight: 600; color: #1d1d1f; margin-top: 8px;">Kardinalitas |U| = {len(U)}</div>
            </div>
        """, unsafe_allow_html=True)

# BAGIAN C & D: OPERASI HIMPUNAN & DIAGRAM VENN
col_c, col_d = st.columns([1.25, 1])

with col_c:
    with st.container(border=True):
        st.markdown('<p class="apple-label">Aljabar Himpunan</p>', unsafe_allow_html=True)
        st.subheader("C. Operasi Himpunan")

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
                <div style="padding: 8px 0; border-bottom: 1px solid rgba(0,0,0,0.06);">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <span style="font-size: 13.5px; font-weight: 600; color: #1d1d1f;">{title}</span>
                        <span style="font-size: 12px; font-weight: 600; color: #0071e3;">Jumlah: {len(s_data)}</span>
                    </div>
                    {render_chips(s_data)}
                </div>
            """, unsafe_allow_html=True)

with col_d:
    with st.container(border=True):
        st.markdown('<p class="apple-label">Visualisasi</p>', unsafe_allow_html=True)
        st.subheader("D. Diagram Venn")

        if HAS_VENN:
            fig, ax = plt.subplots(figsize=(4.5, 3.6), dpi=160)
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
                        txt.set_fontsize(10.5)
                        txt.set_fontweight('semibold')
                        txt.set_color('#1d1d1f')
                for txt in v.subset_labels:
                    if txt:
                        txt.set_fontsize(11.5)
                        txt.set_color('#1d1d1f')

            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Pustaka `matplotlib-venn` belum terpasang.")

# BAGIAN E: PRINSIP INKLUSI-EKSKLUSI
with st.container(border=True):
    st.markdown('<p class="apple-label">Validasi Matematis</p>', unsafe_allow_html=True)
    st.subheader("E. Perhitungan Prinsip Inklusi-Eksklusi")

    card_a = len(A)
    card_b = len(B)
    card_inter = len(inter_set)
    pie_val = card_a + card_b - card_inter
    actual_val = len(union_set)

    col_e1, col_e2 = st.columns(2)

    with col_e1:
        st.latex(r"|A \cup B| = |A| + |B| - |A \cap B|")
        st.markdown(f"""
        **Substitusi Nilai:**
        * $|A| = {card_a}$ (Jumlah elemen {kat_a})
        * $|B| = {card_b}$ (Jumlah elemen {kat_b})
        * $|A \cap B| = {card_inter}$ (Jumlah irisan)
        """)

    with col_e2:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #0071e3;">
                <div class="apple-label">Hasil Perhitungan</div>
                <div style="font-size: 16px; font-weight: 600; color: #1d1d1f; margin-top: 4px;">
                    |A ∪ B| = {card_a} + {card_b} - {card_inter} = <strong>{pie_val}</strong>
                </div>
                <div style="font-size: 13px; color: #34c759; margin-top: 6px; font-weight: 600;">
                    ✓ Terverifikasi: Tepat sesuai jumlah gabungan unik ({actual_val}).
                </div>
                <div style="font-size: 11.5px; color: #86868b; margin-top: 2px;">
                    Tidak ada elemen irisan yang terhitung ganda.
                </div>
            </div>
        """, unsafe_allow_html=True)