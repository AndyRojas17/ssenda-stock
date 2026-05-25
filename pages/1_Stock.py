import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import render_header, render_footer, load_stock, load_meta, color_badge

st.set_page_config(
    page_title="Stock — Ssenda",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_header("Consultar Stock de Motos")

# ── INFO ÚLTIMA CARGA ─────────────────────────────────────────────────────────
meta = load_meta()
if meta:
    st.markdown(
        f'<p style="color:#888;font-size:0.82rem;margin-top:-10px">📦 Stock actualizado: '
        f'<b>{meta["last_upload"]}</b> — {meta["modelos"]} modelos cargados</p>',
        unsafe_allow_html=True,
    )

st.markdown('<hr style="border:none;border-top:1px solid #EEE;margin:0 0 20px 0">',
            unsafe_allow_html=True)

# ── BUSCADOR ──────────────────────────────────────────────────────────────────
stock = load_stock()

if not stock:
    st.info("⚠️ No hay stock cargado. Pídele al encargado que suba el Excel desde el panel Admin.")
    render_footer()
    st.stop()

query = st.text_input(
    "",
    placeholder="🔍  Buscar modelo...  ej: X7 200, CBF 125, AKT TT",
    key="search_query",
    label_visibility="collapsed",
)

st.markdown('<div style="margin-bottom:20px"></div>', unsafe_allow_html=True)

# ── RESULTADOS ────────────────────────────────────────────────────────────────
if not query.strip():
    st.markdown(
        '<p style="color:#A0AEC0;text-align:center;margin-top:40px;font-size:1rem">'
        'Escribe el nombre de un modelo para ver su stock</p>',
        unsafe_allow_html=True,
    )
    render_footer()
    st.stop()

q = query.strip().lower()
import unicodedata

def normalizar(texto):
    nfkd = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")

resultados = [
    item for item in stock
    if q in normalizar(item["modelo"]) or normalizar(q) in normalizar(item["modelo"])
]

if not resultados:
    st.markdown(
        f'<div style="text-align:center;color:#A0AEC0;padding:50px 0">'
        f'<div style="font-size:2rem">🏍️</div>'
        f'<p>No se encontraron modelos con <b>"{query}"</b></p>'
        f'</div>',
        unsafe_allow_html=True,
    )
    render_footer()
    st.stop()

# Métrica rápida
total_und = sum(
    c["cantidad"] for item in resultados for c in item["colores"] if c["cantidad"] > 0
)
m1, m2 = st.columns(2)
with m1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-value">{len(resultados)}</div>
        <div class="metric-label">Modelos encontrados</div></div>""",
        unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class="metric-card green">
        <div class="metric-value">{total_und}</div>
        <div class="metric-label">Unidades disponibles</div></div>""",
        unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tarjetas de resultados
for item in resultados:
    colores_disp = [c for c in item["colores"] if c["cantidad"] > 0]
    if not colores_disp:
        continue
    total = sum(c["cantidad"] for c in colores_disp)
    badges = "".join(color_badge(c["color"], c["cantidad"]) for c in colores_disp)
    total_label = f"Total: {total} unidad{'es' if total != 1 else ''}"

    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:22px 26px;
                margin-bottom:12px;border:1.5px solid #E2E8F0;
                box-shadow:0 1px 4px rgba(0,0,0,0.06)">
        <div style="font-size:1.1rem;font-weight:700;color:#1A202C;margin-bottom:14px;
                    border-left:3px solid #1A56DB;padding-left:10px">
            {item['modelo']}
        </div>
        <div style="flex-wrap:wrap">{badges}</div>
        <div style="margin-top:12px;font-size:0.75rem;color:#A0AEC0;
                    text-transform:uppercase;letter-spacing:0.8px">
            {total_label}
        </div>
    </div>
    """, unsafe_allow_html=True)

render_footer()
