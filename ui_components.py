import streamlit as st

def apply_custom_css():
    """Applies ultra-premium, futuristic CSS styling to the Streamlit app."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* Base Theme */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
            background-color: #050505;
            color: #e2e8f0;
        }
        
        .stApp {
            background: radial-gradient(circle at top right, #1a1025 0%, #050505 50%, #0a0a0a 100%);
        }
        
        /* Headers */
        h1 {
            background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe, #00f2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            font-size: 3rem !important;
            animation: gradient-shift 5s ease infinite;
            background-size: 200% 200%;
        }
        
        h2, h3 {
            color: #4facfe;
            font-weight: 600;
        }
        
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Glassmorphic Agent Cards */
        .agent-card {
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid rgba(79, 172, 254, 0.2);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: slideIn 0.5s ease-out forwards;
            opacity: 0;
            transform: translateY(20px);
        }
        
        .agent-card:hover {
            transform: translateY(-5px) scale(1.01);
            border-color: rgba(79, 172, 254, 0.6);
            box-shadow: 0 15px 40px 0 rgba(79, 172, 254, 0.15);
        }
        
        @keyframes slideIn {
            to { opacity: 1; transform: translateY(0); }
        }
        
        .agent-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #00f2fe;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Monospace reasoning text */
        .agent-reasoning {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: #94a3b8;
            white-space: pre-wrap;
            background: rgba(0, 0, 0, 0.5);
            padding: 16px;
            border-radius: 8px;
            border-left: 3px solid #4facfe;
            line-height: 1.6;
        }
        
        /* Verdict Box */
        .verdict-box {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.3) 100%);
            border: 1px solid rgba(16, 185, 129, 0.5);
            color: #ecfdf5;
            padding: 40px 30px;
            border-radius: 24px;
            text-align: center;
            box-shadow: 0 20px 50px rgba(16, 185, 129, 0.15);
            margin-top: 40px;
            position: relative;
            overflow: hidden;
        }
        
        .verdict-box::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%; width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, transparent 70%);
            animation: pulse-glow 4s infinite alternate;
        }
        
        .verdict-box.fake {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.3) 100%);
            border-color: rgba(239, 68, 68, 0.5);
            color: #fef2f2;
            box-shadow: 0 20px 50px rgba(239, 68, 68, 0.15);
        }
        
        .verdict-box.fake::before {
            background: radial-gradient(circle, rgba(239,68,68,0.1) 0%, transparent 70%);
        }
        
        @keyframes pulse-glow {
            0% { transform: scale(0.9); opacity: 0.5; }
            100% { transform: scale(1.1); opacity: 1; }
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            color: white !important;
            border-radius: 12px;
            border: none;
            padding: 12px 30px;
            font-weight: 800;
            font-size: 1.1rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            box-shadow: 0 10px 20px rgba(0, 242, 254, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(0, 242, 254, 0.5);
        }
        
        /* Metrics styling */
        [data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace;
            color: #00f2fe;
            font-size: 2.5rem;
            font-weight: 800;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 1rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Text areas and inputs */
        .stTextArea textarea, .stTextInput input {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(79, 172, 254, 0.3) !important;
            color: #e2e8f0 !important;
            border-radius: 12px !important;
            font-size: 1.1rem;
            padding: 16px !important;
            transition: border-color 0.3s;
        }
        
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #00f2fe !important;
            box-shadow: 0 0 0 1px #00f2fe !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_agent_log(agent_name: str, icon: str, content: str):
    """Renders a visually stunning card for an agent's reasoning/output."""
    st.markdown(f"""
        <div class="agent-card">
            <div class="agent-title">
                <span style="font-size: 1.8rem;">{icon}</span> {agent_name}
            </div>
            <div class="agent-reasoning">{content}</div>
        </div>
    """, unsafe_allow_html=True)

def render_final_verdict(verdict_text: str, confidence: int = 95):
    """Renders the final verdict box with high-end styling."""
    is_fake = "manipulated" in verdict_text.lower() or "fake" in verdict_text.lower() or "questionable" in verdict_text.lower()
    
    class_name = "verdict-box fake" if is_fake else "verdict-box"
    icon = "⚠️" if is_fake else "🛡️"
    title = "MANIPULATION DETECTED" if is_fake else "VERIFIED AUTHENTIC"
    color = "#ef4444" if is_fake else "#10b981"
    
    st.markdown(f"""
        <div class="{class_name}">
            <h2 style="color: {color}; margin-bottom: 20px; font-size: 2.5rem; font-weight: 800; display: flex; align-items: center; justify-content: center; gap: 15px; position: relative; z-index: 10;">
                {icon} {title}
            </h2>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; color: #fff; margin-bottom: 20px; position: relative; z-index: 10;">
                Confidence Score: {confidence}%
            </div>
            <div style="font-size: 1.2rem; line-height: 1.8; color: rgba(255,255,255,0.9); max-width: 800px; margin: 0 auto; position: relative; z-index: 10;">
                {verdict_text}
            </div>
        </div>
    """, unsafe_allow_html=True)
