import streamlit as st
import json
import os

PRIMARY   = "#F5C200"
DARK      = "#1A1A1A"

STYLES = """
<style>
.stApp { background-color: #FFFFFF; }

/* ── Métricas ── */
.metric-card {
    background: #FAFAFA; border-radius: 10px; padding: 18px 22px;
    border: 1px solid #EEEEEE; border-left: 4px solid #F5C200;
    text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.metric-card.green { border-left-color: #00A651; }
.metric-card.gray  { border-left-color: #888888; }
.metric-value { font-size: 2rem; font-weight: 800; color: #1A1A1A; line-height: 1; }
.metric-label { font-size: 0.75rem; color: #888888; text-transform: uppercase;
                letter-spacing: 0.8px; margin-top: 6px; }

/* ── Botones ── */
.stButton > button,
.stFormSubmitButton > button {
    background: #F5C200 !important;
    color: #1A1A1A !important; border: none !important; border-radius: 8px !important;
    font-size: 1rem !important; font-weight: 800 !important;
    padding: 14px 40px !important; width: 100% !important;
    letter-spacing: 0.5px !important; transition: all 0.2s !important;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #E0AE00 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(245,194,0,0.5) !important;
}

/* ── Upload card ── */
.upload-card {
    background: #FAFAFA; border: 1.5px solid #E0E0E0; border-radius: 10px;
    padding: 20px; margin-bottom: 12px;
}
.upload-card h4 {
    color: #1A1A1A; font-size: 0.85rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; margin: 0 0 4px 0;
}
.upload-card p { color: #888888; font-size: 0.78rem; margin: 0; }

/* ── Footer ── */
.ssenda-footer {
    text-align: center; color: #AAAAAA; font-size: 0.75rem;
    margin-top: 40px; padding-top: 16px; border-top: 1px solid #EEEEEE;
}
</style>
"""

COLOR_MAP = {
    # Negros
    "negro": "#2D3748", "negr": "#2D3748", "neg": "#2D3748",
    "nrg": "#2D3748", "ngr": "#2D3748", "ng": "#2D3748", "black": "#2D3748",
    # Rojos
    "rojo": "#E53E3E", "roj": "#E53E3E", "rj": "#E53E3E", "red": "#E53E3E",
    # Blancos
    "blanco": "#EDF2F7", "blan": "#EDF2F7", "blc": "#EDF2F7",
    "bla": "#EDF2F7", "bl": "#EDF2F7", "white": "#EDF2F7",
    # Azules
    "azul": "#3182CE", "azu": "#3182CE", "az": "#3182CE",
    "blue": "#3182CE", "azul met": "#2B6CB0", "celeste": "#63B3ED",
    # Verdes
    "verde": "#38A169", "verd": "#38A169", "ver": "#38A169",
    "vrd": "#38A169", "green": "#38A169",
    # Amarillos
    "amarillo": "#D69E2E", "ama": "#D69E2E", "yellow": "#D69E2E",
    # Naranja
    "naranja": "#DD6B20", "nar": "#DD6B20", "anar": "#DD6B20",
    "anrj": "#DD6B20", "ana": "#DD6B20", "an": "#DD6B20", "orange": "#DD6B20",
    # Grises
    "gris": "#718096", "gri": "#718096", "gr": "#718096",
    "gray": "#718096", "grey": "#718096", "plateado": "#A0AEC0", "silver": "#A0AEC0",
    # Rosas
    "rosa": "#D53F8C", "ros": "#D53F8C", "rosa sak": "#ED64A6", "pink": "#D53F8C",
    # Morados
    "morado": "#805AD5", "purple": "#805AD5",
    # Bronce / Dorado / Marrones
    "bronce": "#CD7F32", "br": "#CD7F32", "bron": "#CD7F32",
    "dorado": "#B7791F", "gold": "#B7791F",
    "marron": "#744210", "cafe": "#744210", "brown": "#744210",
    "vinotinto": "#822727",
    "beige": "#C8A97E", "crema": "#FEFCBF",
}

DATA_DIR      = os.path.join(os.path.dirname(__file__), "data")
STOCK_FILE    = os.path.join(DATA_DIR, "stock.json")
META_FILE     = os.path.join(DATA_DIR, "meta.json")
ATE_FILE      = os.path.join(DATA_DIR, "stock_ate.json")
CJM_FILE      = os.path.join(DATA_DIR, "stock_cjm.json")
META_ATE_FILE = os.path.join(DATA_DIR, "meta_ate.json")
META_CJM_FILE = os.path.join(DATA_DIR, "meta_cjm.json")


def load_stock():
    if not os.path.exists(STOCK_FILE):
        return []
    with open(STOCK_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_meta():
    if not os.path.exists(META_FILE):
        return None
    with open(META_FILE, encoding="utf-8") as f:
        return json.load(f)


def load_meta_almacen(almacen):
    """Carga meta de un almacén específico: 'ate' o 'cjm'."""
    path = META_ATE_FILE if almacen == "ate" else META_CJM_FILE
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _combine_stocks(ate_records, cjm_records):
    """Combina los stocks de Tienda Ate y Cajamarquilla sumando por modelo+color."""
    combined = {}  # modelo -> {color -> {ate, cjm}}

    for item in ate_records:
        modelo = item["modelo"]
        if modelo not in combined:
            combined[modelo] = {}
        for c in item["colores"]:
            color = c["color"]
            if color not in combined[modelo]:
                combined[modelo][color] = {"ate": 0, "cjm": 0}
            combined[modelo][color]["ate"] += c.get("cantidad", 0)

    for item in cjm_records:
        modelo = item["modelo"]
        if modelo not in combined:
            combined[modelo] = {}
        for c in item["colores"]:
            color = c["color"]
            if color not in combined[modelo]:
                combined[modelo][color] = {"ate": 0, "cjm": 0}
            combined[modelo][color]["cjm"] += c.get("cantidad", 0)

    result = []
    for modelo, colores_dict in combined.items():
        colores = []
        for color, vals in colores_dict.items():
            ate = vals["ate"]
            cjm = vals["cjm"]
            colores.append({
                "color": color,
                "cantidad": ate + cjm,
                "ate": ate,
                "cjm": cjm,
            })
        result.append({"modelo": modelo, "colores": colores})

    return result


def _commit_to_github(path, content_str):
    """Guarda un archivo en el repo de GitHub para que persista entre redeploys."""
    import requests, base64
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        repo  = st.secrets.get("GITHUB_REPO", "AndyRojas17/ssenda-stock")
        if not token:
            return
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        r = requests.get(url, headers=headers, timeout=10)
        sha = r.json().get("sha") if r.status_code == 200 else None
        payload = {
            "message": f"Auto: actualizar {path}",
            "content": base64.b64encode(content_str.encode()).decode(),
        }
        if sha:
            payload["sha"] = sha
        requests.put(url, headers=headers, json=payload, timeout=10)
    except Exception:
        pass


def save_almacen(records, filename, count, almacen):
    """
    Guarda el stock de un almacén ('ate' o 'cjm'), recombina ambos
    y actualiza stock.json + meta.json globales.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    from datetime import datetime, timezone, timedelta
    peru = timezone(timedelta(hours=-5))

    stock_path = ATE_FILE      if almacen == "ate" else CJM_FILE
    meta_path  = META_ATE_FILE if almacen == "ate" else META_CJM_FILE
    other_path = CJM_FILE      if almacen == "ate" else ATE_FILE

    # Guardar stock del almacén
    stock_str = json.dumps(records, ensure_ascii=False, indent=2)
    with open(stock_path, "w", encoding="utf-8") as f:
        f.write(stock_str)

    meta = {
        "last_upload": datetime.now(peru).strftime("%d/%m/%Y %H:%M"),
        "filename": filename,
        "modelos": count,
    }
    meta_str = json.dumps(meta, ensure_ascii=False)
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(meta_str)

    # Cargar el otro almacén para combinar
    other_records = []
    if os.path.exists(other_path):
        with open(other_path, encoding="utf-8") as f:
            other_records = json.load(f)

    if almacen == "ate":
        combined = _combine_stocks(records, other_records)
    else:
        combined = _combine_stocks(other_records, records)

    combined_str = json.dumps(combined, ensure_ascii=False, indent=2)
    with open(STOCK_FILE, "w", encoding="utf-8") as f:
        f.write(combined_str)

    # Meta combinada
    combined_meta = {
        "last_upload": datetime.now(peru).strftime("%d/%m/%Y %H:%M"),
        "filename": filename,
        "modelos": len(combined),
        "ate": load_meta_almacen("ate"),
        "cjm": load_meta_almacen("cjm"),
    }
    combined_meta_str = json.dumps(combined_meta, ensure_ascii=False)
    with open(META_FILE, "w", encoding="utf-8") as f:
        f.write(combined_meta_str)

    # Persistir todo en GitHub
    _commit_to_github(f"data/stock_{almacen}.json", stock_str)
    _commit_to_github(f"data/meta_{almacen}.json", meta_str)
    _commit_to_github("data/stock.json", combined_str)
    _commit_to_github("data/meta.json", combined_meta_str)


def _resolver_colores(nombre):
    """Devuelve lista de colores CSS. Si el nombre tiene guion (NRG-ROJ) retorna uno por parte."""
    import unicodedata
    def norm(t):
        t = t.lower().strip()
        return "".join(c for c in unicodedata.normalize("NFD", t)
                       if unicodedata.category(c) != "Mn")

    def buscar(key):
        if key in COLOR_MAP:
            return COLOR_MAP[key]
        for mk, mv in COLOR_MAP.items():
            if mk.startswith(key) or key.startswith(mk):
                return mv
        return None

    if "-" in nombre:
        colores = []
        for parte in nombre.split("-"):
            c = buscar(norm(parte))
            if c and c not in colores:
                colores.append(c)
        if colores:
            return colores

    color_full = buscar(norm(nombre))
    if color_full:
        return [color_full]

    return ["#CBD5E0"]


def _dot_style(colores_css):
    """Genera el CSS de background para el círculo (sólido o gradiente)."""
    if len(colores_css) == 1:
        return f"background:{colores_css[0]}"
    stops = []
    step = 100 // len(colores_css)
    for i, c in enumerate(colores_css):
        ini = i * step
        fin = (i + 1) * step if i < len(colores_css) - 1 else 100
        stops.append(f"{c} {ini}% {fin}%")
    return f"background:linear-gradient(135deg, {', '.join(stops)})"


def color_badge(color, cantidad, ate=0, cjm=0):
    colores_css = _resolver_colores(color)
    dot_bg     = _dot_style(colores_css)
    es_claro   = all(c in ("#EDF2F7", "#FEFCBF", "#CBD5E0") for c in colores_css)
    border     = "1px solid #CBD5E0" if es_claro else "1px solid rgba(0,0,0,0.15)"
    sin_stock  = cantidad == 0
    opacity    = "opacity:0.45;" if sin_stock else ""
    cant_label = str(cantidad) if not sin_stock else "Sin stock"
    cant_color = "#718096" if not sin_stock else "#CBD5E0"

    # Desglose por almacén
    breakdown_html = ""
    if not sin_stock and (ate != 0 or cjm != 0):
        parts = []
        if ate > 0:
            parts.append(f"Ate&nbsp;{ate}")
        if cjm > 0:
            parts.append(f"Cajam&nbsp;{cjm}")
        if parts:
            breakdown_html = (
                f'<span style="font-size:0.72rem;color:#A0AEC0;'
                f'padding-left:6px;border-left:1px solid #E2E8F0;">'
                f'{" · ".join(parts)}</span>'
            )

    return (
        f'<span style="display:inline-flex;align-items:center;gap:8px;'
        f'background:#F7FAFC;border-radius:20px;padding:7px 16px;margin:4px;'
        f'font-size:0.88rem;border:1px solid #E2E8F0;{opacity}">'
        f'<span style="width:14px;height:14px;border-radius:50%;{dot_bg};'
        f'display:inline-block;border:{border};flex-shrink:0"></span>'
        f'<strong style="color:#2D3748">{color}</strong>'
        f'<span style="color:{cant_color};font-weight:600">{cant_label}</span>'
        f'{breakdown_html}'
        f"</span>"
    )


def render_header(subtitle=""):
    import base64
    st.markdown(STYLES, unsafe_allow_html=True)
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    logo_html = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{b64}" style="height:48px;width:auto">'
    else:
        logo_html = '<span style="font-size:1.7rem;font-weight:900;color:#F5C200;font-style:italic">S·SENDA</span>'

    st.markdown(f"""
    <div style="background:#1A1A1A;border-radius:10px;padding:16px 24px;
                display:flex;align-items:center;gap:20px;margin-bottom:24px">
        {logo_html}
        <div style="width:1px;height:36px;background:#3A3A3A"></div>
        <div style="font-size:0.88rem;color:#CCCCCC;font-weight:500">
            {subtitle if subtitle else 'Panel interno de ventas'}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="ssenda-footer">
        Ssenda — Panel interno de ventas
    </div>
    """, unsafe_allow_html=True)
