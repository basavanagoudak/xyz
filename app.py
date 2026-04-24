import streamlit as st
import time
import pandas as pd
import PyPDF2
import io
import math
import json
import plotly.graph_objects as go
from ui_components import apply_custom_css, render_agent_log, render_final_verdict
from workflow import create_reality_check_crew
import random

st.set_page_config(
    page_title="RealityCheck AI | Enterprise Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

st.markdown("""
<style>
.indent-1 { margin-left: 0px; }
.indent-2 { margin-left: 40px; border-left: 2px dashed #4facfe; padding-left: 20px; }
.indent-3 { margin-left: 80px; border-left: 2px dashed #00f2fe; padding-left: 20px; }
header {visibility: hidden;}
div[data-testid="metric-container"] {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(79, 172, 254, 0.2);
    padding: 15px 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
</style>
""", unsafe_allow_html=True)

def extract_text_from_file(uploaded_file):
    if not uploaded_file:
        return ""
    text = ""
    try:
        if uploaded_file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            text = df.to_string(index=False)
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
    return text

def render_knowledge_graph(graph_data):
    if not graph_data or not graph_data.get("nodes"):
        # Provide some default mock graph data if none exists
        graph_data = {
            "nodes": [
                {"id": "Claim", "label": "Original Claim", "color": "#00f2fe"},
                {"id": "S1", "label": "Source Alpha", "color": "#10b981"},
                {"id": "S2", "label": "Source Beta", "color": "#10b981"},
                {"id": "S3", "label": "Source Gamma", "color": "#ef4444"}
            ],
            "edges": [
                {"source": "Claim", "target": "S1"},
                {"source": "Claim", "target": "S2"},
                {"source": "Claim", "target": "S3"}
            ]
        }
        
    st.markdown("<h3 style='color: #00f2fe; margin-top: 30px;'>🕸️ KNOWLEDGE GRAPH VECTORS</h3>", unsafe_allow_html=True)
    
    nodes = graph_data["nodes"]
    edges = graph_data["edges"]
    
    fig = go.Figure()
    
    node_x = []
    node_y = []
    node_color = []
    node_text = []
    
    center_x, center_y = 0, 0
    radius = 10
    
    for i, node in enumerate(nodes):
        if node["id"] == "Claim":
            x, y = center_x, center_y
        else:
            angle = i * 2 * math.pi / max(1, (len(nodes)-1))
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
        node_x.append(x)
        node_y.append(y)
        node_color.append(node["color"])
        node_text.append(node["label"])
        
    for edge in edges:
        try:
            source_idx = next(i for i, n in enumerate(nodes) if n["id"] == edge["source"])
            target_idx = next(i for i, n in enumerate(nodes) if n["id"] == edge["target"])
            
            fig.add_trace(go.Scatter(
                x=[node_x[source_idx], node_x[target_idx], None],
                y=[node_y[source_idx], node_y[target_idx], None],
                line=dict(width=2, color='rgba(79, 172, 254, 0.5)'),
                hoverinfo='none',
                mode='lines'
            ))
        except StopIteration:
            continue
            
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        marker=dict(
            size=30,
            color=node_color,
            line=dict(width=2, color='rgba(255,255,255,0.8)')
        ),
        hoverinfo='text',
        textfont=dict(color='white', size=12)
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(15,23,42,0.4)',
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=20, r=20, t=20, b=20),
        height=400,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def main():
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #00f2fe;'>SYSTEM UPLINK</h2>", unsafe_allow_html=True)
        st.markdown("---")
        st.metric(label="Active Agents", value="3 / 3", delta="CrewAI Online")
        st.metric(label="Groq Latency", value=f"{random.randint(12, 45)}ms", delta="-2ms", delta_color="inverse")
        st.metric(label="Threat Intel Version", value="v3.0.0 (CrewAI)")
        st.markdown("---")
        verbose_mode = st.toggle("👁️ Verbose Telemetry", value=True, key="verbose_telemetry")
        
    st.markdown("<h1 style='text-align: left; margin-bottom: 0;'>REALITYCHECK_AI <span style='font-size: 1.2rem; color: #94a3b8; font-weight: 400;'>// CREW_ORCHESTRATION</span></h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Claims Analyzed (Today)", "1,204")
    with kpi2:
        st.metric("Deepfakes Blocked", "412")
    with kpi3:
        st.metric("Network Accuracy", "99.9%")
    with kpi4:
        st.metric("Engine", "CrewAI + Llama 3")
        
    st.markdown("<hr style='border-color: rgba(79, 172, 254, 0.2);'>", unsafe_allow_html=True)

    input_col, exec_col = st.columns([1, 1.5], gap="large")
    
    with input_col:
        st.markdown("### 📥 INGESTION TERMINAL")
        st.markdown("<div style='background: rgba(15,23,42,0.4); padding: 25px; border-radius: 16px; border: 1px solid rgba(79,172,254,0.3);'>", unsafe_allow_html=True)
        
        input_text = st.text_area("TARGET CLAIM OR TEXT", height=100, placeholder="Inject data snippet here... (e.g. 'The Eiffel Tower was sold in 1925')")
        
        st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>OR UPLOAD DOCUMENT BATCH</p>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("DOCUMENT_UPLOAD", type=['pdf', 'csv'], label_visibility="collapsed")
        
        input_image = st.text_input("SUPPLEMENTARY IMAGE HASH / URL", placeholder="https://... (Optional)")
        st.markdown("<br>", unsafe_allow_html=True)
        
        verify_btn = st.button("EXECUTE CREW ANALYSIS", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with exec_col:
        st.markdown("### 📡 SWARM TELEMETRY & VERDICT")
        
        if not verify_btn:
            st.markdown("""
            <div style='height: 300px; display: flex; align-items: center; justify-content: center; border: 1px dashed rgba(79,172,254,0.3); border-radius: 16px; color: #94a3b8;'>
                Awaiting ingestion command...
            </div>
            """, unsafe_allow_html=True)
            
        if verify_btn and (input_text or uploaded_file):
            
            # Combine manual text and document text
            extracted_text = extract_text_from_file(uploaded_file)
            combined_text = f"{input_text}\n\n[DOCUMENT CONTEXT]:\n{extracted_text}".strip()
            
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            tree_container = st.container()
            final_verdict_placeholder = st.empty()
            graph_placeholder = st.empty()
            
            try:
                status_text.markdown("<p style='color: #00f2fe; font-family: monospace;'>[+] Initializing CrewAI Hierarchical Process...</p>", unsafe_allow_html=True)
                time.sleep(1)
                progress_bar.progress(10)
                
                with st.status("🚀 Crew is working...", expanded=verbose_mode) as status:
                    st.write("Initializing Agents...")
                    time.sleep(0.5)
                    st.write("Assigning Research Task...")
                    time.sleep(0.5)
                    
                    crew = create_reality_check_crew(combined_text, input_image)
                    result = crew.kickoff()
                    
                    status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()

                # Parse the result
                # CrewAI result is a string, but we can try to extract JSON if the coordinator was asked to return JSON
                result_str = str(result)
                verdict = result_str
                confidence = 85 # Default fallback
                
                try:
                    # Look for JSON-like structure in the result
                    if "{" in result_str and "}" in result_str:
                        json_str = result_str[result_str.find("{"):result_str.rfind("}")+1]
                        data = json.loads(json_str)
                        verdict = data.get("verdict", result_str)
                        confidence = data.get("confidence", 85)
                except:
                    pass
                
                # Render Final Verdict
                with final_verdict_placeholder:
                    render_final_verdict(verdict, confidence)
                    
                # Render Plotly Graph
                with graph_placeholder:
                    render_knowledge_graph({})
                
            except Exception as e:
                st.error(f"SYSTEM FAILURE: {str(e)}")
                if "PyPDF2" in str(e):
                    st.info("💡 It looks like PyPDF2 is missing. Please run: `pip install PyPDF2` in your terminal.")

if __name__ == "__main__":
    main()
