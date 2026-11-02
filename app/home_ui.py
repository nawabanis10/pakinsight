"""
PakInsight - UI helpers (dark theme, sidebar navigation, new Home page).
Keep this file in the SAME folder as app.py.

Optional images (put them in an "assets" folder next to app.py):
    hero.jpg      -> Faisal Mosque / Margalla banner
    weather.jpg   -> Weather Analysis card background
    cost.jpg      -> Cost of Living card background
    economic.jpg  -> Economic Analysis card background
    compare.jpg   -> City Comparison card background
If an image is missing, a nice gradient is used instead.
"""

import base64
from pathlib import Path
from urllib.parse import quote

import streamlit as st

ASSETS_DIR = Path(__file__).resolve().parent / "assets"

PAGES = [
    "Home",
    "Weather Analysis",
    "Cost of Living",
    "Economic Analysis",
    "City Comparison",
]

NAV_ICONS = {
    "Home": "🏠",
    "Weather Analysis": "☁️",
    "Cost of Living": "🏷️",
    "Economic Analysis": "📊",
    "City Comparison": "🔁",
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
.stApp { background: #061a2e; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1250px; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: #071a2c;
    border-right: 1px solid rgba(255,255,255,0.06);
}
.pk-logo { display:flex; align-items:center; gap:12px; margin: 4px 0 26px 0; }
.pk-flag {
    width:46px; height:32px; border-radius:4px; display:flex; align-items:center;
    justify-content:center; color:#fff; font-size:18px;
    background: linear-gradient(90deg, #ffffff 25%, #01411c 25%);
    padding-left: 10px; box-sizing: border-box;
}
.pk-logo-text { font-size:1.7rem; font-weight:700; color:#fff; letter-spacing:-0.5px; }
.pk-logo-text span { color:#19d3a2; }
.nav-label { color:#8fa3b8; font-size:.9rem; margin-bottom:8px; }

section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 4px; }
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    width:100%; padding:11px 14px; border-radius:9px; cursor:pointer;
    transition: background .2s;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background: rgba(255,255,255,0.05); }
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child { display:none; }
section[data-testid="stSidebar"] div[role="radiogroup"] label p { font-size:.97rem; color:#d6e2ee; }
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) { background:#0d4a42; }
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p { color:#fff; font-weight:600; }

.pk-tagline { margin-top: 38vh; color:#cfd9e4; font-size:.95rem; line-height:1.6; }
.pk-tagline .arrow { color:#19d3a2; font-size:2rem; line-height:1; }
.pk-tagline .line { width:40px; height:2px; background:#19d3a2; margin-top:14px; opacity:.6; }

/* ---------- Hero ---------- */
.pk-hero {
    border-radius: 18px; padding: 44px 48px; min-height: 340px;
    background-size: cover; background-position: right center;
    border: 1px solid rgba(255,255,255,0.06);
}
.pk-hero h1 { font-size: 4rem; font-weight: 800; color:#fff; margin:0 0 8px 0; letter-spacing:-1.5px; line-height:1.05; padding:0; }
.pk-hero h1 span { color:#19d3a2; }
.pk-hero h2 { font-size: 2.1rem; font-weight: 700; color:#fff; margin: 14px 0 12px 0; padding:0; }
.pk-hero p { max-width: 560px; color:#dbe6f0; font-size:1.08rem; line-height:1.6; margin:0; }

/* ---------- Section headings ---------- */
.pk-section { display:flex; align-items:center; gap:12px; margin: 34px 0 4px 0; }
.pk-section .ico { font-size:1.5rem; }
.pk-section h3 { margin:0; padding:0; color:#fff; font-size:1.55rem; font-weight:700; }
.pk-sub { color:#9db0c3; margin: 0 0 18px 38px; font-size:.95rem; }

/* ---------- Stat cards ---------- */
.stat-grid { display:grid; grid-template-columns: repeat(4, 1fr); gap:20px; }
.stat-card {
    background: linear-gradient(180deg, #0b2742 0%, #08203a 100%);
    border: 1px solid rgba(255,255,255,0.07); border-bottom: 4px solid var(--c);
    border-radius: 14px; padding: 20px 22px;
}
.stat-ico {
    width:48px; height:48px; border-radius:50%; display:flex; align-items:center;
    justify-content:center; font-size:1.4rem; margin-bottom:12px;
    background: color-mix(in srgb, var(--c) 22%, transparent);
}
.stat-label { color:#d3deea; font-size:.98rem; font-weight:500; }
.stat-value { color:#fff; font-size:2.3rem; font-weight:700; margin-top:2px; }

/* ---------- Explore cards ---------- */
.ex-grid { display:grid; grid-template-columns: repeat(2, 1fr); gap:20px; }
a.pk-link, a.pk-link:hover { text-decoration:none !important; color:inherit !important; }
.ex-card {
    position:relative; display:flex; gap:16px; align-items:flex-start;
    border: 1.5px solid var(--c); border-radius: 14px; padding: 22px;
    min-height: 140px; background-size: cover; background-position: right center;
    transition: transform .2s, box-shadow .2s;
}
.ex-card:hover { transform: translateY(-3px); box-shadow: 0 8px 26px color-mix(in srgb, var(--c) 35%, transparent); }
.ex-ico {
    flex: 0 0 56px; height:56px; border-radius:50%; background: var(--c);
    display:flex; align-items:center; justify-content:center; font-size:1.6rem;
}
.ex-body h4 { margin:0 0 6px 0; padding:0; color:#fff; font-size:1.2rem; font-weight:700; }
.ex-body p { margin:0 0 14px 0; color:#dbe6f0; font-size:.95rem; line-height:1.5; max-width: 330px; }
.ex-tags { font-size:.85rem; color: var(--c); font-weight:500; }
.ex-arrow {
    position:absolute; right:16px; bottom:16px; width:36px; height:36px; border-radius:8px;
    background: rgba(8,20,36,.85); color:#fff; display:flex; align-items:center;
    justify-content:center; font-size:1.2rem;
}

.pk-footer { text-align:center; color:#9db0c3; font-size:.8rem; letter-spacing:.5px;
    margin-top: 34px; padding-top: 14px; }

@media (max-width: 900px) {
    .stat-grid, .ex-grid { grid-template-columns: 1fr; }
    .pk-hero h1 { font-size: 2.8rem; }
}
</style>
"""


@st.cache_data(show_spinner=False)
def _img(name: str):
    """Return a base64 data-URI for assets/<name>, or None if it doesn't exist."""
    path = ASSETS_DIR / name
    if not path.exists():
        return None
    ext = path.suffix.lower().lstrip(".")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return f"data:image/{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def render_sidebar() -> str:
    """Draws the sidebar and returns the selected page name."""
    # Cards on the Home page link to ?page=<name>; handle that here.
    if "page" in st.query_params:
        target = st.query_params["page"]
        if target in PAGES:
            st.session_state["nav"] = target
        st.query_params.clear()

    with st.sidebar:
        st.markdown(
            '<div class="pk-logo"><div class="pk-flag">☪</div>'
            '<div class="pk-logo-text">Pak<span>Insight</span></div></div>'
            '<div class="nav-label">Navigation</div>',
            unsafe_allow_html=True,
        )

        page = st.radio(
            "Navigation",
            PAGES,
            key="nav",
            format_func=lambda p: f"{NAV_ICONS[p]}  {p}",
            label_visibility="collapsed",
        )

        st.markdown(
            '<div class="pk-tagline"><div class="arrow">↗</div>'
            "Better Data<br>Better Decisions<br>A Brighter Pakistan"
            '<div class="line"></div></div>',
            unsafe_allow_html=True,
        )
    return page


def _stat_card(icon, label, value, color):
    return (
        f'<div class="stat-card" style="--c:{color}">'
        f'<div class="stat-ico">{icon}</div>'
        f'<div class="stat-label">{label}</div>'
        f'<div class="stat-value">{value}</div></div>'
    )


def _explore_card(page, icon, title, desc, tags, color, base_rgb, image_name):
    img = _img(image_name)
    r, g, b = base_rgb
    if img:
        bg = (
            f"linear-gradient(90deg, rgba({r},{g},{b},.97) 0%, "
            f"rgba({r},{g},{b},.85) 45%, rgba({r},{g},{b},.2) 100%), url('{img}')"
        )
    else:
        bg = f"linear-gradient(135deg, rgba({r},{g},{b},1) 0%, #071a2c 100%)"

    tags_html = " &nbsp;·&nbsp; ".join(tags)
    href = "?page=" + quote(page)
    return (
        f'<a class="pk-link" href="{href}" target="_self">'
        f'<div class="ex-card" style="--c:{color}; background-image:{bg}">'
        f'<div class="ex-ico">{icon}</div>'
        f'<div class="ex-body"><h4>{title}</h4><p>{desc}</p>'
        f'<div class="ex-tags">{tags_html}</div></div>'
        f'<div class="ex-arrow">›</div></div></a>'
    )


def render_home(weather_df, cost_df, economic_df):
    # ---------- Hero ----------
    hero = _img("hero.jpg")
    if hero:
        hero_bg = (
            "linear-gradient(90deg, rgba(6,26,46,.96) 0%, rgba(6,26,46,.72) 50%, "
            f"rgba(6,26,46,.1) 100%), url('{hero}')"
        )
    else:
        hero_bg = "linear-gradient(120deg, #06182b 0%, #0b3d5c 60%, #0f6a6a 100%)"

    st.markdown(
        f'<div class="pk-hero" style="background-image:{hero_bg}">'
        '<h1>Pak<span>Insight</span></h1>'
        '<h2>Discover Pakistan Through Data.</h2>'
        '<p>Explore city-wise weather, essential prices and economic insights '
        'to understand how life differs across Pakistan.</p></div>',
        unsafe_allow_html=True,
    )

    # ---------- Data at a Glance ----------
    stats = "".join(
        [
            _stat_card("⛅", "Cities Covered", "5", "#1e90ff"),
            _stat_card("🌧️", "Weather Records", f"{len(weather_df):,}", "#19d3a2"),
            _stat_card("🏷️", "Essential Items", f"{len(cost_df):,}", "#f5a623"),
            _stat_card("📈", "Economic Cities", f"{len(economic_df):,}", "#8b5cf6"),
        ]
    )
    st.markdown(
        '<div class="pk-section"><span class="ico">📊</span><h3>Data at a Glance</h3></div>'
        '<div class="pk-sub">Key statistics from our Pakistan city datasets.</div>'
        f'<div class="stat-grid">{stats}</div>',
        unsafe_allow_html=True,
    )

    # ---------- Explore Analytics ----------
    cards = "".join(
        [
            _explore_card(
                "Weather Analysis", "⛅", "Weather Analysis",
                "Explore temperature trends, rainfall and climate patterns across five cities.",
                ["Climate", "Temperature", "Rainfall"],
                "#1e90ff", (10, 47, 102), "weather.jpg",
            ),
            _explore_card(
                "Cost of Living", "🛒", "Cost of Living",
                "Compare essential item prices and understand price differences between cities.",
                ["Prices", "Essential Items", "Affordability"],
                "#19d3a2", (9, 58, 44), "cost.jpg",
            ),
            _explore_card(
                "Economic Analysis", "📊", "Economic Analysis",
                "Analyze business establishments and workforce distribution across cities.",
                ["Business", "Workforce", "Economy"],
                "#a78bfa", (42, 27, 94), "economic.jpg",
            ),
            _explore_card(
                "City Comparison", "🔁", "City Comparison",
                "Compare two cities through weather, prices and economic indicators.",
                ["Comparison", "Insights", "City Data"],
                "#f5a623", (61, 42, 12), "compare.jpg",
            ),
        ]
    )
    st.markdown(
        '<div class="pk-section"><span class="ico">🧭</span><h3>Explore Analytics</h3></div>'
        '<div class="pk-sub">Select a section from the sidebar to explore detailed insights.</div>'
        f'<div class="ex-grid">{cards}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="pk-footer">PAKINSIGHT &nbsp;|&nbsp; DATA-DRIVEN UNDERSTANDING OF PAKISTAN</div>',
        unsafe_allow_html=True,
    )