import streamlit as st
import json
import os

PRIMARY   = "#1A56DB"
PRIMARY_D = "#1040A0"

STYLES = """
<style>
.stApp { background-color: #FFFFFF; }
.metric-card {
    background: #FAFAFA; border-radius: 10px; padding: 18px 22px;
    border: 1px solid #EEEEEE; border-left: 4px solid #1A56DB;
    text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.metric-card.green  { border-left-color: #00A651; }
.metric-card.gray   { border-left-color: #888888; }
.metric-value { font-size: 2rem; font-weight: 800; color: #1A1A1A; line-height: 1; }
.metric-label { font-size: 0.75rem; color: #888888; text-transform: uppercase;
                letter-spacing: 0.8px; margin-top: 6px; }
.stButton > button {
    background: linear-gradient(135deg, #1A56DB, #1040A0) !important;
    color: white !important; border: none !important; border-radius: 8px !important;
    font-size: 1.1rem !important; font-weight: 700 !important;
    padding: 14px 40px !important; width: 100% !important;
    letter-spacing: 0.5px !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563EB, #1A56DB) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(26,86,219,0.4) !important;
}
.upload-card {
    background: #FAFAFA; border: 1.5px solid #E0E0E0; border-radius: 10px;
    padding: 20px; margin-bottom: 12px;
}
.upload-card h4 {
    color: #1A56DB; font-size: 0.85rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; margin: 0 0 4px 0;
}
.upload-card p { color: #888888; font-size: 0.78rem; margin: 0; }
.ssenda-footer {
    text-align: center; color: #AAAAAA; font-size: 0.75rem;
    margin-top: 40px; padding-top: 16px; border-top: 1px solid #EEEEEE;
}
</style>
"""

COLOR_MAP = {
    "rojo": "#E53E3E", "red": "#E53E3E",
    "negro": "#2D3748", "black": "#2D3748",
    "blanco": "#EDF2F7", "white": "#EDF2F7",
    "azul": "#3182CE", "blue": "#3182CE",
    "celeste": "#63B3ED",
    "verde": "#38A169", "green": "#38A169",
    "amarillo": "#D69E2E", "yellow": "#D69E2E",
    "naranja": "#DD6B20", "orange": "#DD6B20",
    "plateado": "#A0AEC0", "silver": "#A0AEC0",
    "gris": "#718096", "gray": "#718096", "grey": "#718096",
    "morado": "#805AD5", "purple": "#805AD5",
    "dorado": "#B7791F", "gold": "#B7791F",
    "rosa": "#D53F8C", "pink": "#D53F8C",
    "marron": "#744210", "cafe": "#744210", "brown": "#744210",
    "vinotinto": "#822727",
    "beige": "#C8A97E", "crema": "#FFFACD",
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
    from datetime import datetime
    meta = {
        "last_upload": datetime.now().strftime("%d/%m/%Y %H:%M"),
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


def color_badge(color, cantidad):
    key = color.lower().strip()
    import unicodedata
    key = "".join(c for c in unicodedata.normalize("NFD", key)
                  if unicodedata.category(c) != "Mn")
    dot = COLOR_MAP.get(key, "#CBD5E0")
    border = "1px solid rgba(0,0,0,0.15)" if key not in ("blanco", "white", "crema", "beige") else "1px solid #CBD5E0"
    return (
        f'<span style="display:inline-flex;align-items:center;gap:8px;'
        f'background:#F7FAFC;border-radius:20px;padding:7px 16px;margin:4px;'
        f'font-size:0.88rem;border:1px solid #E2E8F0">'
        f'<span style="width:13px;height:13px;border-radius:50%;background:{dot};'
        f'display:inline-block;border:{border};flex-shrink:0"></span>'
        f'<strong style="color:#2D3748">{color}</strong>'
        f'<span style="color:#718096;font-weight:600">{cantidad}</span>'
        f"</span>"
    )


def render_header(subtitle=""):
    st.markdown(STYLES, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:20px;padding-bottom:0">
        <div style="font-size:2rem;font-weight:900;color:#1A56DB;letter-spacing:-1px;line-height:1">
            Ssenda
        </div>
        <div style="font-size:0.9rem;color:#555555;padding-top:6px">
            {subtitle if subtitle else 'Panel de herramientas'}
        </div>
    </div>
    <div style="border-top:2.5px solid #1A56DB;margin:14px 0 24px 0"></div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="ssenda-footer">
        Ssenda — Panel interno de ventas
    </div>
    """, unsafe_allow_html=True)
