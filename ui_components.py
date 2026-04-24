import streamlit as st


def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* ── Base ─────────────────────────────────────────────────── */
    html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

    .stApp {
        background: #05070f;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(79,172,254,0.12) 0%, transparent 70%),
            radial-gradient(ellipse 60% 40% at 90% 80%, rgba(120,60,255,0.08) 0%, transparent 60%);
        min-height: 100vh;
    }

    section[data-testid="stSidebar"] { background: rgba(8,10,22,0.95) !important; border-right: 1px solid rgba(79,172,254,0.12); }
    header { visibility: hidden; }

    /* ── Typography ───────────────────────────────────────────── */
    h1, h2, h3 { font-family: 'Outfit', sans-serif !important; }

    /* ── Sidebar metrics ─────────────────────────────────────── */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: #4facfe !important;
        font-size: 1.9rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    [data-testid="metric-container"] {
        background: rgba(15,23,42,0.5);
        border: 1px solid rgba(79,172,254,0.15);
        border-radius: 12px;
        padding: 14px 18px;
    }

    /* ── Glassmorphic card ──────────────────────────────────── */
    .glass-card {
        background: rgba(13,18,35,0.7);
        border: 1px solid rgba(79,172,254,0.18);
        border-radius: 20px;
        padding: 28px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
        margin-bottom: 20px;
    }

    /* ── Section heading ─────────────────────────────────────── */
    .section-heading {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #4facfe;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-heading::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(79,172,254,0.4), transparent);
    }

    /* ── Text area / input ───────────────────────────────────── */
    .stTextArea textarea {
        background: rgba(8,12,28,0.8) !important;
        border: 1px solid rgba(79,172,254,0.25) !important;
        border-radius: 14px !important;
        color: #e2e8f0 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1rem !important;
        padding: 16px !important;
        transition: border-color 0.25s, box-shadow 0.25s;
        resize: none;
    }
    .stTextArea textarea:focus {
        border-color: #4facfe !important;
        box-shadow: 0 0 0 3px rgba(79,172,254,0.12) !important;
    }
    .stTextInput input {
        background: rgba(8,12,28,0.8) !important;
        border: 1px solid rgba(79,172,254,0.25) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-family: 'Outfit', sans-serif !important;
    }
    .stTextInput input:focus {
        border-color: #4facfe !important;
        box-shadow: 0 0 0 3px rgba(79,172,254,0.12) !important;
    }
    .stFileUploader {
        background: rgba(8,12,28,0.6) !important;
        border: 1px dashed rgba(79,172,254,0.3) !important;
        border-radius: 14px !important;
    }

    /* ── CTA Button ──────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: #05070f !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 28px !important;
        box-shadow: 0 8px 24px rgba(79,172,254,0.35) !important;
        transition: all 0.25s ease !important;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 32px rgba(79,172,254,0.5) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }

    /* ── Label label ─────────────────────────────────────────── */
    .label-badge {
        display: inline-block;
        padding: 6px 18px;
        border-radius: 999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }
    .label-TRUE        { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.4); }
    .label-MOSTLY_TRUE { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.35); }
    .label-MIXED       { background: rgba(245,158,11,0.12); color: #f59e0b; border: 1px solid rgba(245,158,11,0.35); }
    .label-MOSTLY_FALSE{ background: rgba(249,115,22,0.12); color: #f97316; border: 1px solid rgba(249,115,22,0.35); }
    .label-FALSE       { background: rgba(239,68,68,0.12);  color: #ef4444; border: 1px solid rgba(239,68,68,0.35); }
    .label-UNVERIFIABLE{ background: rgba(148,163,184,0.12);color: #94a3b8; border: 1px solid rgba(148,163,184,0.3); }

    /* ── Verdict box ─────────────────────────────────────────── */
    .verdict-container {
        border-radius: 20px;
        padding: 32px;
        position: relative;
        overflow: hidden;
        text-align: center;
        margin-top: 24px;
    }
    .verdict-TRUE        { background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(5,150,105,0.18)); border: 1px solid rgba(16,185,129,0.4); }
    .verdict-MOSTLY_TRUE { background: linear-gradient(135deg, rgba(52,211,153,0.07), rgba(16,185,129,0.15)); border: 1px solid rgba(52,211,153,0.35); }
    .verdict-MIXED       { background: linear-gradient(135deg, rgba(245,158,11,0.07), rgba(217,119,6,0.15));  border: 1px solid rgba(245,158,11,0.35); }
    .verdict-MOSTLY_FALSE{ background: linear-gradient(135deg, rgba(249,115,22,0.07), rgba(234,88,12,0.15));  border: 1px solid rgba(249,115,22,0.35); }
    .verdict-FALSE       { background: linear-gradient(135deg, rgba(239,68,68,0.08),  rgba(220,38,38,0.18));  border: 1px solid rgba(239,68,68,0.4); }
    .verdict-UNVERIFIABLE{ background: linear-gradient(135deg, rgba(100,116,139,0.08),rgba(71,85,105,0.15));  border: 1px solid rgba(100,116,139,0.3); }

    .verdict-icon { font-size: 3.5rem; margin-bottom: 12px; }
    .verdict-text {
        font-size: 1.05rem;
        line-height: 1.8;
        color: rgba(255,255,255,0.88);
        max-width: 680px;
        margin: 0 auto;
    }

    /* ── Source pill ─────────────────────────────────────────── */
    .source-pill {
        display: inline-block;
        background: rgba(79,172,254,0.08);
        border: 1px solid rgba(79,172,254,0.25);
        border-radius: 8px;
        padding: 8px 14px;
        margin: 5px 5px 5px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #4facfe;
        text-decoration: none;
        transition: background 0.2s;
    }
    .source-pill:hover { background: rgba(79,172,254,0.18); }

    /* ── History item ────────────────────────────────────────── */
    .history-item {
        background: rgba(15,23,42,0.5);
        border: 1px solid rgba(79,172,254,0.1);
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: border-color 0.2s;
    }
    .history-item:hover { border-color: rgba(79,172,254,0.35); }
    .history-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; }
    .history-claim { font-size: 0.82rem; color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    /* ── Pulse dot ───────────────────────────────────────────── */
    @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(1.4)} }
    .pulse-dot {
        display: inline-block;
        width: 8px; height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 1.8s infinite;
        margin-right: 6px;
    }

    /* ── Awaiting state ──────────────────────────────────────── */
    .awaiting-box {
        height: 280px;
        border: 1px dashed rgba(79,172,254,0.25);
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #475569;
        gap: 14px;
        font-size: 0.95rem;
    }
    .awaiting-icon { font-size: 2.5rem; opacity: 0.4; }

    /* ── Progress/status ─────────────────────────────────────── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #4facfe, #00f2fe) !important;
    }

    /* ── Spinner ─────────────────────────────────────────────── */
    .stSpinner > div { border-top-color: #4facfe !important; }

    /* ── Scrollbar ───────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(79,172,254,0.3); border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)


# ── Label metadata ────────────────────────────────────────────────────────────
LABEL_META = {
    "TRUE":         {"icon": "✅", "color": "#10b981", "text": "VERIFIED TRUE"},
    "MOSTLY TRUE":  {"icon": "🟢", "color": "#34d399", "text": "MOSTLY TRUE"},
    "MIXED":        {"icon": "⚖️", "color": "#f59e0b", "text": "MIXED / DISPUTED"},
    "MOSTLY FALSE": {"icon": "🟠", "color": "#f97316", "text": "MOSTLY FALSE"},
    "FALSE":        {"icon": "❌", "color": "#ef4444", "text": "VERIFIED FALSE"},
    "UNVERIFIABLE": {"icon": "❓", "color": "#94a3b8", "text": "UNVERIFIABLE"},
}


def render_verdict(verdict: str, label: str, confidence: int, sources: list):
    meta = LABEL_META.get(label.upper(), LABEL_META["UNVERIFIABLE"])
    css_label = label.upper().replace(" ", "_")
    icon = meta["icon"]
    color = meta["color"]
    label_text = meta["text"]

    st.markdown(f"""
    <div class="verdict-container verdict-{css_label}">
        <div class="verdict-icon">{icon}</div>
        <div class="label-badge label-{css_label}">{label_text}</div>
        <div class="verdict-text">{verdict}</div>
    </div>
    """, unsafe_allow_html=True)

    # Confidence gauge
    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:6px;">
            <span style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#64748b; letter-spacing:2px; text-transform:uppercase;">Confidence Score</span>
        </div>
        <div style="text-align:center; margin-bottom:10px;">
            <span style="font-family:'JetBrains Mono',monospace; font-size:2.8rem; font-weight:800; color:{color};">{confidence}<span style="font-size:1.2rem; color:#64748b;">%</span></span>
        </div>
        """, unsafe_allow_html=True)
        st.progress(confidence / 100)

    # Sources
    if sources:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📎 Cited Sources</div>', unsafe_allow_html=True)
        pills_html = ""
        for url in sources[:6]:
            if url and url.startswith("http"):
                domain = url.split("/")[2] if len(url.split("/")) > 2 else url
                pills_html += f'<a href="{url}" target="_blank" class="source-pill">🔗 {domain}</a>'
        if pills_html:
            st.markdown(pills_html, unsafe_allow_html=True)


def render_history_sidebar(history: list):
    """Renders the analysis history in the sidebar."""
    if not history:
        st.markdown('<p style="color:#475569; font-size:0.8rem; text-align:center;">No analyses yet.</p>', unsafe_allow_html=True)
        return

    for i, item in enumerate(reversed(history[-8:])):
        label = item.get("label", "UNVERIFIABLE")
        meta = LABEL_META.get(label.upper(), LABEL_META["UNVERIFIABLE"])
        claim_preview = item.get("claim", "")[:55] + ("…" if len(item.get("claim", "")) > 55 else "")
        css_label = label.upper().replace(" ", "_")
        st.markdown(f"""
        <div class="history-item">
            <div class="history-label label-{css_label}" style="color:{meta['color']};">{meta['icon']} {meta['text']}</div>
            <div class="history-claim">{claim_preview}</div>
        </div>
        """, unsafe_allow_html=True)
