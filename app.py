from __future__ import annotations

from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

try:
    from matplotlib_venn import venn2
    VENN_AVAILABLE = True
except ImportError:
    VENN_AVAILABLE = False


# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Sistem Klasifikasi Data - Operasi Himpunan",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sistem Klasifikasi Data Berbasis Himpunan")
st.caption(
    "Proyek Mini #2 | Union, Intersection, Difference, Complement, "
    "Diagram Venn, dan Prinsip Inklusi-Eksklusi"
)


# ============================================================
# DATASET CONTOH
# Format data: satu baris untuk satu anggota dan satu kategori.
# Anggota boleh muncul di beberapa kategori.
# ============================================================
SAMPLE_DATASETS = {
    "Dataset Contoh 1 - Minat Mahasiswa": {
        "data": pd.DataFrame(
            [
                ("Andi", "Python"),
                ("Budi", "Python"),
                ("Citra", "Python"),
                ("Dina", "Python"),
                ("Budi", "Web"),
                ("Dina", "Web"),
                ("Eka", "Web"),
            ],
            columns=["nama", "kategori"],
        ),
        "universe": ["Andi", "Budi", "Citra", "Dina", "Eka", "Fajar", "Gita"],
        "description": "Mengelompokkan mahasiswa berdasarkan minat Python dan Web.",
    },
    "Dataset Contoh 2 - Keikutsertaan UKM": {
        "data": pd.DataFrame(
            [
                ("Ali", "Olahraga"),
                ("Budi", "Olahraga"),
                ("Citra", "Olahraga"),
                ("Dedi", "Olahraga"),
                ("Ema", "Olahraga"),
                ("Budi", "Seni"),
                ("Ema", "Seni"),
                ("Fani", "Seni"),
                ("Gilang", "Seni"),
            ],
            columns=["nama", "kategori"],
        ),
        "universe": [
            "Ali", "Budi", "Citra", "Dedi", "Ema", "Fani", "Gilang",
            "Hana", "Irfan", "Joko",
        ],
        "description": "Mengelompokkan mahasiswa berdasarkan keikutsertaan UKM Olahraga dan Seni.",
    },
}


def clean_values(values: Iterable[object]) -> set[str]:
    """Ubah nilai menjadi himpunan teks yang bersih dan tanpa duplikasi."""
    cleaned: set[str] = set()
    for value in values:
        if pd.isna(value):
            continue
        item = str(value).strip()
        if item:
            cleaned.add(item)
    return cleaned


def parse_universe(raw_text: str) -> set[str]:
    """Baca anggota semesta dari input yang dipisahkan koma/baris baru/titik koma."""
    normalized = raw_text.replace(";", "\n").replace(",", "\n")
    return {item.strip() for item in normalized.splitlines() if item.strip()}


def show_members(label: str, members: set[str]) -> None:
    """Tampilkan isi himpunan secara konsisten."""
    ordered = sorted(members, key=str.casefold)
    st.markdown(f"**{label}** ({len(ordered)} anggota)")
    if ordered:
        st.code("{ " + ", ".join(ordered) + " }", language=None)
    else:
        st.info("Himpunan kosong: ∅")


def create_venn_diagram(set_a: set[str], set_b: set[str], label_a: str, label_b: str):
    """Buat diagram Venn dua himpunan."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    only_a = len(set_a - set_b)
    only_b = len(set_b - set_a)
    both = len(set_a & set_b)

    if VENN_AVAILABLE:
        venn2(
            subsets=(only_a, only_b, both),
            set_labels=(label_a, label_b),
            ax=ax,
        )
    else:
        # Fallback sederhana apabila matplotlib-venn belum terpasang.
        from matplotlib.patches import Circle

        ax.add_patch(Circle((0.42, 0.5), 0.28, alpha=0.35, label=label_a))
        ax.add_patch(Circle((0.58, 0.5), 0.28, alpha=0.35, label=label_b))
        ax.text(0.28, 0.5, str(only_a), ha="center", va="center", fontsize=14)
        ax.text(0.50, 0.5, str(both), ha="center", va="center", fontsize=14)
        ax.text(0.72, 0.5, str(only_b), ha="center", va="center", fontsize=14)
        ax.text(0.30, 0.86, label_a, ha="center", fontsize=11)
        ax.text(0.70, 0.86, label_b, ha="center", fontsize=11)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")

    ax.set_title("Diagram Venn: Hubungan Himpunan A dan B")
    fig.tight_layout()
    return fig


# ============================================================
# 1. PILIH SUMBER DATASET
# ============================================================
st.sidebar.header("1. Sumber Dataset")
source = st.sidebar.radio(
    "Pilih sumber data",
    ["Dataset Contoh 1 - Minat Mahasiswa", "Dataset Contoh 2 - Keikutsertaan UKM", "Upload CSV sendiri"],
)

source_description = ""
source_key = source

if source in SAMPLE_DATASETS:
    selected_sample = SAMPLE_DATASETS[source]
    df = selected_sample["data"].copy()
    default_universe = selected_sample["universe"]
    source_description = selected_sample["description"]
    member_column = "nama"
    category_column = "kategori"
else:
    uploaded_file = st.sidebar.file_uploader("Unggah file dataset (.csv)", type=["csv"])
    if uploaded_file is None:
        st.info(
            "Silakan unggah file CSV. Format minimal memiliki dua kolom: "
            "kolom anggota (misalnya `nama`) dan kolom kategori (misalnya `kategori`)."
        )
        st.markdown("**Contoh format CSV:**")
        st.code("nama,kategori\nAndi,Python\nBudi,Python\nBudi,Web\nCitra,Web", language="csv")
        st.stop()

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"File CSV tidak dapat dibaca: {exc}")
        st.stop()

    if len(df.columns) < 2:
        st.error("Dataset harus memiliki minimal dua kolom: anggota dan kategori.")
        st.stop()

    st.sidebar.caption("Tentukan kolom yang berisi nama anggota dan kategori.")
    member_column = st.sidebar.selectbox("Kolom anggota", options=list(df.columns), index=0)
    category_default_index = 1 if len(df.columns) > 1 else 0
    category_column = st.sidebar.selectbox(
        "Kolom kategori",
        options=list(df.columns),
        index=category_default_index,
    )
    if member_column == category_column:
        st.error("Kolom anggota dan kolom kategori harus berbeda.")
        st.stop()

    df = df[[member_column, category_column]].copy()
    df[member_column] = df[member_column].astype("string").str.strip()
    df[category_column] = df[category_column].astype("string").str.strip()
    default_universe = sorted(clean_values(df[member_column].tolist()), key=str.casefold)
    source_description = f"Dataset dari file {uploaded_file.name}."
    source_key = f"upload_{uploaded_file.name}"

st.info(source_description)

# Bersihkan data sebelum dimodelkan sebagai himpunan.
df = df.dropna(subset=[member_column, category_column]).copy()
df[member_column] = df[member_column].astype(str).str.strip()
df[category_column] = df[category_column].astype(str).str.strip()
df = df[(df[member_column] != "") & (df[category_column] != "")]

if df.empty:
    st.error("Dataset tidak memiliki baris anggota-kategori yang valid.")
    st.stop()

categories = sorted(clean_values(df[category_column].tolist()), key=str.casefold)
if len(categories) < 2:
    st.error("Dataset harus memiliki minimal dua kategori berbeda untuk membandingkan himpunan A dan B.")
    st.stop()

# ============================================================
# 2. PEMODELAN HIMPUNAN A, B, DAN SEMESTA U
# ============================================================
st.sidebar.header("2. Pengaturan Himpunan")
col_a, col_b = st.sidebar.columns(2)
category_a = col_a.selectbox("Kategori A", categories, index=0)
category_b = col_b.selectbox("Kategori B", categories, index=1)

if category_a == category_b:
    st.error("Kategori A dan B harus berbeda.")
    st.stop()

set_a = clean_values(df.loc[df[category_column] == category_a, member_column].tolist())
set_b = clean_values(df.loc[df[category_column] == category_b, member_column].tolist())

st.sidebar.markdown("**Anggota Semesta (U)**")
st.sidebar.caption("Pisahkan anggota dengan koma, titik koma, atau baris baru. Semesta harus mencakup semua anggota A dan B.")
raw_universe = st.sidebar.text_area(
    "Daftar anggota semesta",
    value="\n".join(default_universe),
    height=150,
    key=f"universe_{source_key}",
    label_visibility="collapsed",
)
universe = parse_universe(raw_universe)

# Pastikan A dan B merupakan bagian dari semesta. Jika ada yang tertinggal,
# tambahkan otomatis dan beri tahu pengguna agar operasi complement tetap valid.
missing_from_universe = (set_a | set_b) - universe
if missing_from_universe:
    st.warning(
        "Ada anggota A/B yang belum ditulis di semesta U. Anggota tersebut "
        "ditambahkan otomatis ke U agar complement dihitung dengan benar: "
        + ", ".join(sorted(missing_from_universe, key=str.casefold))
    )
    universe |= missing_from_universe

# Operasi himpunan
union_ab = set_a | set_b
intersection_ab = set_a & set_b
difference_a_b = set_a - set_b
difference_b_a = set_b - set_a
complement_a = universe - set_a
complement_b = universe - set_b

# ============================================================
# 3. TAMPILKAN DATASET DAN RINGKASAN HIMPUNAN
# ============================================================
st.subheader("A. Dataset yang Digunakan")
st.dataframe(df.rename(columns={member_column: "Anggota", category_column: "Kategori"}), use_container_width=True, hide_index=True)

st.subheader("B. Pemodelan Himpunan")
metric1, metric2, metric3 = st.columns(3)
metric1.metric(f"Jumlah anggota A ({category_a})", len(set_a))
metric2.metric(f"Jumlah anggota B ({category_b})", len(set_b))
metric3.metric("Jumlah anggota semesta (U)", len(universe))

set_col1, set_col2, set_col3 = st.columns(3)
with set_col1:
    show_members(f"A - {category_a}", set_a)
with set_col2:
    show_members(f"B - {category_b}", set_b)
with set_col3:
    show_members("U - Semesta", universe)

# ============================================================
# 4. OPERASI HIMPUNAN
# ============================================================
st.subheader("C. Hasil Operasi Himpunan")
operations = [
    ("Union (A ∪ B)", union_ab, "Semua anggota yang ada di A atau B."),
    ("Intersection (A ∩ B)", intersection_ab, "Anggota yang terdapat di A dan B."),
    ("Difference (A − B)", difference_a_b, "Anggota A yang tidak terdapat di B."),
    ("Difference (B − A)", difference_b_a, "Anggota B yang tidak terdapat di A."),
    ("Complement (Aᶜ = U − A)", complement_a, "Anggota semesta yang tidak terdapat di A."),
    ("Complement (Bᶜ = U − B)", complement_b, "Anggota semesta yang tidak terdapat di B."),
]

for start in range(0, len(operations), 2):
    left, right = st.columns(2)
    for col, item in zip((left, right), operations[start:start + 2]):
        title, members, explanation = item
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(explanation)
                if members:
                    st.write("{ " + ", ".join(sorted(members, key=str.casefold)) + " }")
                else:
                    st.write("∅ (himpunan kosong)")
                st.caption(f"Kardinalitas: {len(members)}")

# ============================================================
# 5. DIAGRAM VENN
# ============================================================
st.subheader("D. Visualisasi Diagram Venn")
fig = create_venn_diagram(set_a, set_b, f"A: {category_a}", f"B: {category_b}")
st.pyplot(fig, use_container_width=False)
plt.close(fig)
st.caption(
    f"A saja: {len(difference_a_b)} | "
    f"B saja: {len(difference_b_a)} | "
    f"Irisan A ∩ B: {len(intersection_ab)}"
)

# ============================================================
# 6. PRINSIP INKLUSI-EKSKLUSI
# ============================================================
st.subheader("E. Perhitungan Prinsip Inklusi-Eksklusi")
count_a = len(set_a)
count_b = len(set_b)
count_intersection = len(intersection_ab)
count_union_ie = count_a + count_b - count_intersection
count_union_actual = len(union_ab)

st.latex(r"|A \cup B| = |A| + |B| - |A \cap B|")
st.latex(
    rf"|A \cup B| = {count_a} + {count_b} - {count_intersection} = {count_union_ie}"
)
result_col1, result_col2 = st.columns(2)
result_col1.metric("Jumlah unik (hasil rumus)", count_union_ie)
result_col2.metric("Jumlah unik (hasil union langsung)", count_union_actual)

if count_union_ie == count_union_actual:
    st.success("Validasi berhasil: hasil Inklusi-Eksklusi sama dengan jumlah anggota union.")
else:
    st.error("Validasi gagal: periksa kembali data dan operasi himpunan.")

# ============================================================
# 7. RINGKASAN DAN UNDUHAN HASIL
# ============================================================
st.subheader("F. Ringkasan Hasil Pengujian")
summary_rows = [
    {"Operasi": "A", "Jumlah anggota": len(set_a), "Anggota": ", ".join(sorted(set_a, key=str.casefold))},
    {"Operasi": "B", "Jumlah anggota": len(set_b), "Anggota": ", ".join(sorted(set_b, key=str.casefold))},
    {"Operasi": "A ∪ B", "Jumlah anggota": len(union_ab), "Anggota": ", ".join(sorted(union_ab, key=str.casefold))},
    {"Operasi": "A ∩ B", "Jumlah anggota": len(intersection_ab), "Anggota": ", ".join(sorted(intersection_ab, key=str.casefold))},
    {"Operasi": "A − B", "Jumlah anggota": len(difference_a_b), "Anggota": ", ".join(sorted(difference_a_b, key=str.casefold))},
    {"Operasi": "B − A", "Jumlah anggota": len(difference_b_a), "Anggota": ", ".join(sorted(difference_b_a, key=str.casefold))},
    {"Operasi": "Aᶜ", "Jumlah anggota": len(complement_a), "Anggota": ", ".join(sorted(complement_a, key=str.casefold))},
    {"Operasi": "Bᶜ", "Jumlah anggota": len(complement_b), "Anggota": ", ".join(sorted(complement_b, key=str.casefold))},
]
summary_df = pd.DataFrame(summary_rows)
st.dataframe(summary_df, use_container_width=True, hide_index=True)

csv_bytes = summary_df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="⬇️ Unduh Ringkasan Hasil (CSV)",
    data=csv_bytes,
    file_name="hasil_operasi_himpunan.csv",
    mime="text/csv",
)

st.divider()
st.caption(
    "Catatan: setiap anggota dihitung satu kali dalam himpunan, meskipun muncul "
    "berulang kali pada file CSV. Complement selalu dihitung terhadap semesta U "
    "yang ditentukan pada panel sebelah kiri."
)
