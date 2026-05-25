import streamlit as st
import pandas as pd
import os, sys, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from utils import render_header, render_footer, save_almacen, load_meta_almacen
except Exception as _e:
    st.error(f"**ERROR IMPORTANDO UTILS:** `{type(_e).__name__}: {_e}`")
    st.code(traceback.format_exc())
    st.stop()

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

# ── CABECERA ADMIN ────────────────────────────────────────────────────────────
col_title, col_logout = st.columns([5, 1])
with col_logout:
    if st.button("Cerrar sesión"):
        st.session_state.admin_ok = False
        st.rerun()

st.markdown('<hr style="border:none;border-top:1px solid #EEE;margin:0 0 24px 0">',
            unsafe_allow_html=True)


# ── FUNCIÓN DE PARSEO ─────────────────────────────────────────────────────────
def parsear_excel(archivo):
    df = pd.read_excel(archivo)
    df.columns = df.columns.astype(str).str.strip()
    cols_up = [c.upper() for c in df.columns]

    tiene_color_col = any("COLOR" in c for c in cols_up)

    if tiene_color_col:
        modelo_col = next((df.columns[i] for i, c in enumerate(cols_up) if "MODELO" in c), df.columns[0])
        color_col  = next((df.columns[i] for i, c in enumerate(cols_up) if "COLOR" in c), None)
        qty_col    = next(
            (df.columns[i] for i, c in enumerate(cols_up)
             if any(k in c for k in ["DISPONIBLE", "CANTIDAD", "STOCK", "QTY"])),
            df.columns[-1]
        )
        agrupado = {}
        for _, row in df.iterrows():
            modelo = str(row[modelo_col]).strip()
            if not modelo or modelo.lower() in ("nan", "none", ""):
                continue
            color = str(row[color_col]).strip() if color_col else "—"
            try:
                cant = int(float(str(row[qty_col])))
            except (ValueError, TypeError):
                cant = 0
            if modelo not in agrupado:
                agrupado[modelo] = []
            agrupado[modelo].append({"color": color, "cantidad": cant})
        records = [{"modelo": m, "colores": c} for m, c in agrupado.items()
                   if any(x["cantidad"] > 0 for x in c)]
    else:
        modelo_col = df.columns[0]
        color_cols = df.columns[1:].tolist()
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

    return records


def _badge_meta(almacen_label, meta):
    if meta:
        return (
            f'<div style="background:#F0FFF4;border:1px solid #C6F6D5;border-radius:8px;'
            f'padding:10px 16px;font-size:0.84rem;color:#276221;margin-bottom:16px">'
            f'✅ Último stock: <b>{meta["last_upload"]}</b> — '
            f'{meta["filename"]} — <b>{meta["modelos"]} modelos</b></div>'
        )
    return (
        f'<div style="background:#FFF5F5;border:1px solid #FED7D7;border-radius:8px;'
        f'padding:10px 16px;font-size:0.84rem;color:#C53030;margin-bottom:16px">'
        f'⚠️ {almacen_label} aún no tiene stock cargado.</div>'
    )


def _seccion_carga(almacen_key, almacen_label):
    """Renderiza la sección de carga para un almacén."""
    meta = load_meta_almacen(almacen_key)
    st.markdown(_badge_meta(almacen_label, meta), unsafe_allow_html=True)

    archivo = st.file_uploader(
        f"Selecciona el Excel de {almacen_label}",
        type=["xlsx", "xls"],
        key=f"file_{almacen_key}",
    )

    if archivo:
        st.success(f"✅ **{archivo.name}** listo para cargar")

    st.markdown("<br>", unsafe_allow_html=True)
    btn_col = st.columns([1, 2, 1])[1]
    with btn_col:
        cargar = st.button(
            f"📂  CARGAR {almacen_label.upper()}",
            key=f"btn_{almacen_key}",
            disabled=not archivo,
        )

    if cargar and archivo:
        st.markdown('<hr style="border:none;border-top:1px solid #EEE;margin:20px 0">',
                    unsafe_allow_html=True)
        with st.spinner("Procesando Excel..."):
            try:
                records = parsear_excel(archivo)
                save_almacen(records, archivo.name, len(records), almacen_key)
            except Exception as e:
                st.error(f"❌ Error al procesar el archivo: {e}")
                render_footer()
                st.stop()

        total_und = sum(c["cantidad"] for r in records for c in r["colores"])
        total_col = sum(len(r["colores"]) for r in records)
        st.markdown(f"### ✅ Stock de {almacen_label} actualizado")
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
            st.markdown(f"""<div class="metric-card gray">
                <div class="metric-value">{total_col}</div>
                <div class="metric-label">Combinaciones color/modelo</div></div>""",
                unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Vista previa")
        filas = [
            {"Modelo": r["modelo"], "Color": c["color"], "Cantidad": c["cantidad"]}
            for r in records for c in r["colores"]
        ]
        st.dataframe(pd.DataFrame(filas), use_container_width=True, height=340)


# ── TABS POR ALMACÉN ──────────────────────────────────────────────────────────
tab_ate, tab_cjm = st.tabs(["🏪  Tienda Ate", "🏭  Cajamarquilla"])

with tab_ate:
    _seccion_carga("ate", "Tienda Ate")

with tab_cjm:
    _seccion_carga("cjm", "Cajamarquilla")

render_footer()
