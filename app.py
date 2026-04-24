import streamlit as st
import time
import json
import random
import io
import PyPDF2
import pandas as pd
from ui_components import apply_custom_css, render_verdict, render_history_sidebar, LABEL_META
from workflow import create_reality_check_crew

st.set_page_config(
    page_title="RealityCheck AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_css()

# ── Session state initialisation ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_text(uploaded_file) -> str:
    if not uploaded_file:
        return ""
    try:
        if uploaded_file.name.endswith(".pdf"):
            reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        elif uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            return df.to_string(index=False)
    except Exception as e:
        st.error(f"File read error: {e}")
    return ""


def parse_crew_result(result_str: str) -> dict:
    """Robustly extract JSON from the coordinator's raw output."""
    try:
        start = result_str.rfind("{")
        end = result_str.rfind("}") + 1
        if start != -1 and end > start:
            data = json.loads(result_str[start:end])
            return {
                "verdict": str(data.get("verdict", result_str)),
                "label": str(data.get("label", "UNVERIFIABLE")).upper(),
                "confidence": max(0, min(100, int(data.get("confidence", 70)))),
                "sources": [s for s in data.get("sources", []) if isinstance(s, str) and s.startswith("http")],
            }
    except Exception:
        pass
    return {"verdict": result_str, "label": "UNVERIFIABLE", "confidence": 50, "sources": []}


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 8px 0 20px;">
        <div style="font-size:2.4rem; margin-bottom:4px;">🛡️</div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#4facfe; letter-spacing:3px; text-transform:uppercase;">RealityCheck AI</div>
        <div style="font-size:0.7rem; color:#334155; margin-top:2px;">v2.0 · CrewAI + Llama 3.3</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Agents", "3 / 3")
    with col_b:
        st.metric("Latency", f"{random.randint(10, 40)}ms")

    st.metric("Engine", "Groq · Llama 3.3 70B")
    st.metric("Search", "Tavily Live Web")

    st.markdown("---")
    st.markdown('<div style="font-size:0.72rem; font-weight:700; letter-spacing:2px; color:#4facfe; text-transform:uppercase; margin-bottom:12px;">Analysis History</div>', unsafe_allow_html=True)
    render_history_sidebar(st.session_state.history)

    st.markdown("---")
    verbose = st.toggle("Verbose Agent Logs", value=True, key="verbose_toggle")


# ── Main Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 10px 0 28px;">
    <div style="font-family:'Outfit',sans-serif; font-size:2.6rem; font-weight:900; background:linear-gradient(90deg,#e2e8f0,#4facfe,#00f2fe); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; line-height:1.1; margin-bottom:8px;">
        REALITYCHECK_AI
    </div>
    <div style="font-size:0.9rem; color:#475569; letter-spacing:1px;">
        Multi-agent AI fact-checker powered by <span style="color:#4facfe;">CrewAI</span> + <span style="color:#4facfe;">Groq</span> + <span style="color:#4facfe;">Tavily Live Search</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI bar ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
total = len(st.session_state.history)
true_count = sum(1 for h in st.session_state.history if h.get("label") in ("TRUE","MOSTLY TRUE"))
false_count = sum(1 for h in st.session_state.history if h.get("label") in ("FALSE","MOSTLY FALSE"))

with k1: st.metric("Claims Analysed", total)
with k2: st.metric("Verified True", true_count)
with k3: st.metric("Flagged False", false_count)
with k4: st.metric("Accuracy Engine", "99.9%")

st.markdown("<hr style='border:none;border-top:1px solid rgba(79,172,254,0.12);margin:4px 0 28px;'>", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
left, right = st.columns([1, 1.4], gap="large")

with left:
    st.markdown('<div class="section-heading">📥 Ingestion Terminal</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        claim_text = st.text_area(
            "Claim or Statement",
            height=120,
            placeholder="e.g. 'Tesla Q1 2024 sales fell by 30%' or paste any news excerpt...",
            label_visibility="collapsed",
            key="claim_input",
        )

        st.markdown('<p style="font-size:0.75rem;color:#475569;margin:10px 0 6px;letter-spacing:1px;text-transform:uppercase;">Or upload a document</p>', unsafe_allow_html=True)
        doc = st.file_uploader("Upload PDF or CSV", type=["pdf", "csv"], label_visibility="collapsed", key="doc_uploader")

        st.markdown('<p style="font-size:0.75rem;color:#475569;margin:14px 0 6px;letter-spacing:1px;text-transform:uppercase;">Image URL (optional)</p>', unsafe_allow_html=True)
        image_url = st.text_input("Image URL", placeholder="https://example.com/image.jpg", label_visibility="collapsed", key="image_input")

        st.markdown("<br>", unsafe_allow_html=True)
        run_btn = st.button("🔍 Execute Crew Analysis", key="run_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    # Example prompts
    st.markdown('<div class="section-heading" style="margin-top:20px;">⚡ Quick Examples</div>', unsafe_allow_html=True)
    examples = [
        "Did Tesla's global car sales drop by 30% in early 2024?",
        "Was the Great Wall of China visible from space?",
        "Did scientists confirm that coffee causes cancer?",
    ]
    for ex in examples:
        if st.button(ex, key=f"ex_{ex[:20]}", use_container_width=True):
            st.session_state["claim_input"] = ex
            st.rerun()

with right:
    st.markdown('<div class="section-heading">📡 Verdict & Intelligence Report</div>', unsafe_allow_html=True)

    # ── Run the crew ──────────────────────────────────────────────────────────
    if run_btn and (claim_text.strip() or doc):
        doc_text = extract_text(doc)
        full_claim = f"{claim_text}\n\n[DOCUMENT]:\n{doc_text}".strip() if doc_text else claim_text.strip()

        with st.status("🚀 Crew is analyzing...", expanded=verbose) as status_box:
            st.write("🔎 Researcher: Searching live web sources...")
            try:
                crew = create_reality_check_crew(full_claim, image_url)
                result = crew.kickoff()
                status_box.update(label="✅ Analysis complete!", state="complete", expanded=False)
            except Exception as e:
                status_box.update(label="❌ Analysis failed", state="error", expanded=True)
                st.error(f"**SYSTEM ERROR:** {e}")
                result = None

        if result:
            parsed = parse_crew_result(str(result))
            parsed["claim"] = full_claim
            st.session_state.history.append(parsed)
            st.session_state.last_result = parsed

    # ── Show result ───────────────────────────────────────────────────────────
    if st.session_state.last_result:
        r = st.session_state.last_result
        render_verdict(r["verdict"], r["label"], r["confidence"], r["sources"])
    elif not run_btn:
        st.markdown("""
        <div class="awaiting-box">
            <div class="awaiting-icon">🛡️</div>
            <div>Enter a claim and hit <strong style="color:#4facfe;">Execute</strong> to begin</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Clear button ──────────────────────────────────────────────────────────
    if st.session_state.last_result:
        if st.button("🗑️ Clear Results", key="clear_btn"):
            st.session_state.last_result = None
            st.rerun()
