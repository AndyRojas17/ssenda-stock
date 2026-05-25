import streamlit as st
from utils import render_header, render_footer, load_meta

st.set_page_config(
    page_title="Ssenda — Panel de ventas",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_header("Panel de ventas")

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

st.markdown("""
<style>
.s-card {
    display: block; text-decoration: none;
    background: #FAFAFA; border: 1.5px solid #E0E0E0;
    border-radius: 12px; padding: 28px 24px; min-height: 170px;
    transition: all 0.18s ease; cursor: pointer;
}
.s-card:hover {
    background: #FFFFFF; box-shadow: 0 6px 24px rgba(0,0,0,0.10);
    transform: translateY(-3px); border-color: #BBBBBB; text-decoration: none;
}
.s-card.blue  { border-top: 4px solid #1A56DB; }
.s-card.green { border-top: 4px solid #2E7D32; }
.s-card, .s-card:link, .s-card:visited, .s-card:hover, .s-card:active,
.s-card *, .s-card *:link, .s-card *:visited, .s-card *:hover {
    text-decoration: none !important;
}
.s-card-icon  { font-size: 2.2rem; margin-bottom: 10px; }
.s-card-title { font-size: 1.2rem; font-weight: 800; color: #1A1A1A; }
.s-card-desc  { color: #666; font-size: 0.9rem; margin-top: 8px; line-height: 1.5; }
.s-card-arrow { display: inline-block; margin-top: 16px; font-size: 0.9rem;
                font-weight: 700; color: #1A56DB; }
.s-card.green .s-card-arrow { color: #2E7D32; }
.s-cards-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; max-width: 760px; }
@media (max-width: 640px) {
    .s-cards-grid { grid-template-columns: 1fr; gap: 16px; }
}
</style>

<div class="s-cards-grid">

  <a href="/Stock" class="s-card blue">
    <div class="s-card-icon">🔍</div>
    <div class="s-card-title">Consultar Stock</div>
    <div class="s-card-desc">
      Busca cualquier modelo de moto y consulta la disponibilidad
      por color en tiempo real.
    </div>
    <div class="s-card-arrow">Ir a Stock →</div>
  </a>

  <a href="/Admin" class="s-card green">
    <div class="s-card-icon">📂</div>
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
