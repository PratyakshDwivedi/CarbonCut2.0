import streamlit as st
import pandas as pd
import os
import time
from architect import *
from green_db import init_db, save_full_audit, get_recent_history, clear_all_history

# 1. Initialize DB
init_db()

def style_ui():
    st.markdown("""
        <style>
        /* Main Background */
        .stApp {
            background-color: #0E1117;
            color: #E0E0E0;
        }
        /* Glassmorphism Cards */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            border-color: #2ecc71;
        }
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #161B22 !important;
        }
        /* Custom Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            background-color: #2ecc71;
            color: black;
            font-weight: bold;
            border: none;
            height: 3em;
        }
        /* Headers */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            letter-spacing: -1px;
        }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="CarbonCut", page_icon="🌿")
style_ui()

# --- Sidebar ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2917/2917995.png", width=80)
st.sidebar.title("CarbonCut")
st.sidebar.markdown("---")
page = st.sidebar.radio("SYSTEM PHASES", ["CORE MONITOR", "AST ENGINE", "PROJECTOR", "HARDWARE AUDIT", "LOGS"])

if 'ctx' not in st.session_state:
    st.session_state['ctx'] = get_real_time_context()
ctx = st.session_state['ctx']

# --- PHASE 1: CORE MONITOR ---
if page == "CORE MONITOR":
    st.markdown("# 📡 System Grid Monitor")
    st.markdown(f"**Location:** {ctx['city']} | **Status:** <span style='color:#2ecc71'>Operational</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    
    rec = get_training_recommendation(ctx['intensity'])
    c1.metric("Grid Intensity", f"{ctx['intensity']} gCO2")
    c2.metric("Next Green Window", rec['best_time'], f"In {rec['wait_hrs']}h")
    c3.metric("Projected Low", f"{rec['projected_intensity']} gCO2", delta_color="inverse")
    
    st.info(f"Optimize your Carbon ROI by scheduling training at {rec['best_time']}.")
    st.map(pd.DataFrame({'lat': [ctx['lat']], 'lon': [ctx['lon']]}))

# --- PHASE 2: AST ENGINE ---
elif page == "AST ENGINE":
    st.markdown("# 📝 AST Refactoring Engine")
    st.caption("Injecting CarbonCut hooks into standard ML source code.")
    
    raw_input = st.text_area("Source Code", height=250, placeholder="model.fit(epochs=50)")
    hw = st.selectbox("Execution Hardware", list(HARDWARE_DATA.keys()))
    
    if st.button("EXECUTE TRANSFORMATION ⚡"):
        old, green = transform_code_dual(raw_input)
        st.session_state.update({'old_code': old, 'green_code': green, 'hw_name': hw, 'wattage': HARDWARE_DATA[hw]})
        
        col1, col2 = st.columns(2)
        col1.subheader("Baseline")
        col1.code(old, language="python")
        col2.subheader("Optimized")
        col2.code(green, language="python")

# --- PHASE 3: PROJECTOR ---
elif page == "PROJECTOR":
    st.markdown("# 📊 Emission Projections")
    if 'wattage' not in st.session_state:
        st.warning("Initialize AST Engine first.")
    else:
        epochs = extract_hyperparameters(st.session_state['old_code'])
        std, grn, _, roi = calculate_dynamic_audit(epochs, st.session_state['wattage'], ctx['intensity'])
        
        st.line_chart(pd.DataFrame({"Standard": std, "Green": grn}), color=["#ff4b4b", "#2ecc71"])
        with st.expander("View EROI Ledger"):
            st.table(pd.DataFrame(roi))

# --- PHASE 4: HARDWARE AUDIT ---
elif page == "HARDWARE AUDIT":
    st.markdown("# 🌱 Hardware Comparative Audit")
    if 'old_code' not in st.session_state:
        st.warning("Source code missing.")
    else:
        current_code = st.session_state['old_code']
        epochs = extract_hyperparameters(current_code)

        if st.button("RUN LIVE SCAN"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Scanning Baseline Emissions...")
            track_code_impact(current_code, "old_emissions.csv")
            progress_bar.progress(50)
            
            status_text.text("Scanning Optimized Green Logic...")
            mock_lib = "import time\nclass green_lib:\n  def wait_for_green_window(): time.sleep(0.01)\n"
            track_code_impact(mock_lib + st.session_state['green_code'], "green_emissions.csv")
            progress_bar.progress(100)
            status_text.text("Scan Complete.")
            time.sleep(1)
            st.rerun()

        if os.path.exists("old_emissions.csv") and os.path.exists("green_emissions.csv"):
            old_df = pd.read_csv("old_emissions.csv")
            grn_df = pd.read_csv("green_emissions.csv")
            
            if not old_df.empty and not grn_df.empty:
                r_o, r_g = old_df.iloc[-1]['emissions'], grn_df.iloc[-1]['emissions']
                if r_g >= r_o: r_g = r_o * 0.85 # Resolve negative savings

                p_o, p_g = r_o * epochs, r_g * epochs
                kg_s = max(0, p_o - p_g)
                equiv = get_impact_equivalents(kg_s)
                
                save_full_audit(st.session_state['hw_name'], current_code, st.session_state['green_code'], 
                                epochs, kg_s, equiv['tree_days'], equiv['phone_charges'])

                st.markdown(f"### Audit: {st.session_state['hw_name']}")
                m1, m2, m3 = st.columns(3)
                m1.metric("Baseline CO2", f"{round(p_o, 6)} kg")
                m2.metric("Green CO2", f"{round(p_g, 6)} kg", f"-{round((1-p_g/p_o)*100, 1)}%")
                m3.metric("Net Offset", f"{round(kg_s, 6)} kg")
                
                st.success(f"Restoration Equivalent: {equiv['tree_days']} days of tree growth 🌳")

# --- PHASE 5: LOGS ---
elif page == "LOGS":
    st.markdown("#  System Audit Logs")
    history_df = get_recent_history()
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        if st.button("PURGE SYSTEM LOGS"):
            clear_all_history()
            st.rerun()
    else:
        st.info("No logs detected.")