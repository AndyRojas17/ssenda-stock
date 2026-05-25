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
.stButton > button {
    background: #F5C200 !important;
    color: #1A1A1A !important; border: none !important; border-radius: 8px !important;
    font-size: 1rem !important; font-weight: 800 !important;
    padding: 14px 40px !important; width: 100% !important;
    letter-spacing: 0.5px !important; transition: all 0.2s !important;
}
.stButton > button:hover {
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
    "negro": "#2D3748", "negr": "#2D3748", "neg": "#2D3748", "black": "#2D3748",
    # Rojos
    "rojo": "#E53E3E", "roj": "#E53E3E", "red": "#E53E3E",
    # Blancos
    "blanco": "#EDF2F7", "blan": "#EDF2F7", "bla": "#EDF2F7", "white": "#EDF2F7",
    # Azules
    "azul": "#3182CE", "azu": "#3182CE", "blue": "#3182CE", "azul met": "#2B6CB0",
    "celeste": "#63B3ED",
    # Verdes
    "verde": "#38A169", "verd": "#38A169", "green": "#38A169",
    # Amarillos
    "amarillo": "#D69E2E", "ama": "#D69E2E", "yellow": "#D69E2E",
    # Naranja
    "naranja": "#DD6B20", "nar": "#DD6B20", "orange": "#DD6B20",
    # Grises
    "gris": "#718096", "gri": "#718096", "gray": "#718096", "grey": "#718096",
    "plateado": "#A0AEC0", "silver": "#A0AEC0",
    # Rosas
    "rosa": "#D53F8C", "ros": "#D53F8C", "rosa sak": "#ED64A6", "pink": "#D53F8C",
    # Morados
    "morado": "#805AD5", "purple": "#805AD5",
    # Dorados / Marrones
    "dorado": "#B7791F", "gold": "#B7791F",
    "marron": "#744210", "cafe": "#744210", "brown": "#744210",
    "vinotinto": "#822727",
    "beige": "#C8A97E", "crema": "#FEFCBF",
}

DATA_DIR   = os.path.join(os.path.dirname(__file__), "data")
STOCK_FILE = os.path.join(DATA_DIR, "stock.json")
META_FILE  = os.path.join(DATA_DIR, "meta.json")


def load_stock():
    if not os.path.exists(STOCK_FILE):
        return []
    with open(STOCK_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_stock(records, filename, count):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(STOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    from datetime import datetime, timezone, timedelta
    peru = timezone(timedelta(hours=-5))
    meta = {
        "last_upload": datetime.now(peru).strftime("%d/%m/%Y %H:%M"),
        "filename": filename,
        "modelos": count,
    }
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)


def load_meta():
    if not os.path.exists(META_FILE):
        return None
    with open(META_FILE, encoding="utf-8") as f:
        return json.load(f)


def _resolver_color(nombre):
    """Devuelve el color CSS para un nombre de color (simple o combinado como NEGR-AZU)."""
    import unicodedata
    def normalizar(t):
        t = t.lower().strip()
        return "".join(c for c in unicodedata.normalize("NFD", t)
                       if unicodedata.category(c) != "Mn")

    key = normalizar(nombre)
    if key in COLOR_MAP:
        return COLOR_MAP[key]
    # Buscar por prefijo (ej: "negr-azu" → buscar "negr")
    partes = key.replace("-", " ").split()
    for parte in partes:
        if parte in COLOR_MAP:
            return COLOR_MAP[parte]
        # Buscar por inicio de clave
        for map_key, map_val in COLOR_MAP.items():
            if map_key.startswith(parte) or parte.startswith(map_key):
                return map_val
    return "#CBD5E0"


def color_badge(color, cantidad):
    dot = _resolver_color(color)
    es_claro = dot in ("#EDF2F7", "#FEFCBF", "#CBD5E0")
    border = "1px solid #CBD5E0" if es_claro else "1px solid rgba(0,0,0,0.15)"
    sin_stock = cantidad == 0
    bg = "#F7FAFC" if not sin_stock else "#F7FAFC"
    opacity = "opacity:0.45;" if sin_stock else ""
    cant_label = str(cantidad) if not sin_stock else "Sin stock"
    cant_color = "#718096" if not sin_stock else "#CBD5E0"
    return (
        f'<span style="display:inline-flex;align-items:center;gap:8px;'
        f'background:{bg};border-radius:20px;padding:7px 16px;margin:4px;'
        f'font-size:0.88rem;border:1px solid #E2E8F0;{opacity}">'
        f'<span style="width:13px;height:13px;border-radius:50%;background:{dot};'
        f'display:inline-block;border:{border};flex-shrink:0"></span>'
        f'<strong style="color:#2D3748">{color}</strong>'
        f'<span style="color:{cant_color};font-weight:600">{cant_label}</span>'
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
