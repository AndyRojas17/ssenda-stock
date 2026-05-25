import streamlit as st
import base64, os
from utils import render_header, render_footer, load_meta

st.set_page_config(
    page_title="Ssenda — Panel de ventas",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_header("Panel de ventas")

def _svg_b64(filename):
    path = os.path.join(os.path.dirname(__file__), "assets", filename)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

icon_stock = _svg_b64("icon_stock.svg")
icon_carga = _svg_b64("icon_carga.svg")
img_stock = f'<img src="data:image/svg+xml;base64,{icon_stock}" style="height:52px;width:auto">' if icon_stock else "🔍"
img_carga = f'<img src="data:image/svg+xml;base64,{icon_carga}" style="height:52px;width:auto">' if icon_carga else "📂"

st.markdown("## Bienvenido al panel de Ssenda")
st.markdown('<p style="color:#666;margin-top:-12px">Selecciona una herramienta para comenzar</p>',
            unsafe_allow_html=True)

meta = load_meta()
if meta:
    st.markdown(
        f'<p style="color:#888;font-size:0.82rem">📦 Último stock cargado: '
        f'<b>{meta["last_upload"]}</b> — {meta["filename"]} — {meta["modelos"]} modelos</p>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(f"""
<style>
.s-card {{
    display: block; text-decoration: none;
    background: #1A1A1A; border-radius: 12px;
    padding: 28px 24px; min-height: 170px;
    transition: all 0.18s ease; cursor: pointer;
    border: 2px solid #2A2A2A;
}}
.s-card:hover {{
    background: #222222; box-shadow: 0 8px 28px rgba(0,0,0,0.25);
    transform: translateY(-3px); border-color: #F5C200;
    text-decoration: none;
}}
.s-card, .s-card:link, .s-card:visited, .s-card:hover, .s-card:active,
.s-card *, .s-card *:link, .s-card *:visited, .s-card *:hover {{
    text-decoration: none !important;
}}
.s-card-icon  {{ font-size: 2.2rem; margin-bottom: 12px; }}
.s-card-title {{ font-size: 1.2rem; font-weight: 800; color: #FFFFFF; }}
.s-card-desc  {{ color: #AAAAAA; font-size: 0.88rem; margin-top: 8px; line-height: 1.6; }}
.s-card-arrow {{
    display: inline-block; margin-top: 18px; font-size: 0.88rem;
    font-weight: 800; color: #F5C200; letter-spacing: 0.3px;
}}
.s-cards-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 720px; }}
@media (max-width: 640px) {{
    .s-cards-grid {{ grid-template-columns: 1fr; gap: 14px; }}
}}
</style>

<div class="s-cards-grid">

  <a href="/Stock" class="s-card">
    <div class="s-card-icon">{img_stock}</div>
    <div class="s-card-title">Consultar Stock</div>
    <div class="s-card-desc">
      Busca cualquier modelo de moto y consulta la disponibilidad
      por color en tiempo real.
    </div>
    <div class="s-card-arrow">Ir a Stock →</div>
  </a>

  <a href="/Admin" class="s-card">
    <div class="s-card-icon">{img_carga}</div>
    <div class="s-card-title">Cargar Stock</div>
    <div class="s-card-desc">
      Panel de administración. Carga el Excel de stock diario
      para actualizar la disponibilidad del equipo.
    </div>
    <div class="s-card-arrow">Ir a Admin →</div>
  </a>

</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
render_footer()
