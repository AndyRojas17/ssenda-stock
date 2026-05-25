import streamlit as st
import pandas as pd
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import render_header, render_footer, save_stock, load_meta

st.set_page_config(
    page_title="Admin — Ssenda",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_header("Panel de Administración — Carga de Stock")

# ── CLAVE DE ACCESO ───────────────────────────────────────────────────────────
try:
    ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]
except Exception:
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ssenda2024")

if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

if not st.session_state.admin_ok:
    st.markdown("### 🔒 Acceso restringido")
    st.markdown('<p style="color:#666;margin-top:-10px">Ingresa la clave para continuar</p>',
                unsafe_allow_html=True)
    with st.form("login_form"):
        pwd = st.text_input("Contraseña", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Ingresar")
    if submitted:
        if pwd == ADMIN_PASSWORD:
            st.session_state.admin_ok = True
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta")
    render_footer()
    st.stop()

# ── PANEL ADMIN ───────────────────────────────────────────────────────────────
col_title, col_logout = st.columns([5, 1])
with col_logout:
    if st.button("Cerrar sesión"):
        st.session_state.admin_ok = False
        st.rerun()

meta = load_meta()
if meta:
    st.markdown(
        f'<div style="background:#F0FFF4;border:1px solid #C6F6D5;border-radius:8px;'
        f'padding:12px 18px;margin-bottom:20px;font-size:0.88rem;color:#276221">'
        f'✅ Último stock cargado: <b>{meta["last_upload"]}</b> — '
        f'{meta["filename"]} — <b>{meta["modelos"]} modelos</b>'
        f'</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div style="background:#FFF5F5;border:1px solid #FED7D7;border-radius:8px;'
        'padding:12px 18px;margin-bottom:20px;font-size:0.88rem;color:#C53030">'
        '⚠️ No hay stock cargado aún. Sube el primer Excel para activar la plataforma.'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr style="border:none;border-top:1px solid #EEE;margin:0 0 24px 0">',
            unsafe_allow_html=True)

# ── ZONA DE CARGA ─────────────────────────────────────────────────────────────
st.markdown("### 📊 Cargar nuevo stock")
st.markdown("""
<div class="upload-card">
    <h4>📋 Formato esperado del Excel</h4>
    <p>Primera columna: nombre del modelo &nbsp;|&nbsp;
       Columnas siguientes: un color por columna con la cantidad como valor</p>
    <p style="margin-top:6px">Ejemplo: &nbsp;
       <code>Modelo | Rojo | Negro | Blanco | Azul</code> &nbsp;—&nbsp;
       cada celda = cantidad disponible</p>
</div>
""", unsafe_allow_html=True)

archivo = st.file_uploader(
    "",
    type=["xlsx", "xls"],
    key="stock_file",
    label_visibility="collapsed",
)

if archivo:
    st.success(f"✅ Archivo seleccionado: **{archivo.name}**")

st.markdown("<br>", unsafe_allow_html=True)
btn_col = st.columns([1, 2, 1])[1]
with btn_col:
    cargar = st.button("📂  CARGAR STOCK", disabled=not archivo)

if cargar and archivo:
    st.markdown('<hr style="border:none;border-top:1px solid #EEE;margin:20px 0">',
                unsafe_allow_html=True)
    with st.spinner("Procesando Excel..."):
        try:
            df = pd.read_excel(archivo)
            df.columns = df.columns.astype(str).str.strip()

            modelo_col  = df.columns[0]
            color_cols  = df.columns[1:].tolist()

            records = []
            for _, row in df.iterrows():
                modelo = str(row[modelo_col]).strip()
                if not modelo or modelo.lower() in ("nan", "none", ""):
                    continue
                colores = []
                for col in color_cols:
                    try:
                        cant = int(float(str(row[col])))
                    except (ValueError, TypeError):
                        cant = 0
                    if cant > 0:
                        colores.append({"color": col, "cantidad": cant})
                if colores:
                    records.append({"modelo": modelo, "colores": colores})

            save_stock(records, archivo.name, len(records))

        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {e}")
            render_footer()
            st.stop()

    # Resumen post-carga
    total_und = sum(c["cantidad"] for r in records for c in r["colores"])
    st.markdown("### ✅ Stock actualizado correctamente")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{len(records)}</div>
            <div class="metric-label">Modelos cargados</div></div>""",
            unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-card green">
            <div class="metric-value">{total_und}</div>
            <div class="metric-label">Unidades en stock</div></div>""",
            unsafe_allow_html=True)
    with m3:
        total_colores = sum(len(r["colores"]) for r in records)
        st.markdown(f"""<div class="metric-card gray">
            <div class="metric-value">{total_colores}</div>
            <div class="metric-label">Combinaciones modelo/color</div></div>""",
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Vista previa del stock cargado")

    filas = []
    for r in records:
        for c in r["colores"]:
            filas.append({"Modelo": r["modelo"], "Color": c["color"], "Cantidad": c["cantidad"]})

    import pandas as pd
    df_prev = pd.DataFrame(filas)
    st.dataframe(df_prev, use_container_width=True, height=380)

render_footer()
