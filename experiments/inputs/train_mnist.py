import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide", page_title="CarbonCut Parallel Comparison")

st.title("✂️ CarbonCut: Parallel Sustainability Benchmarking")
st.markdown("Compare Standard vs. Green execution metrics side-by-side in real-time.")

# --- SECTION 1: CODE INPUT ---
user_code = st.text_area("Paste Standard Code here:", height=150, placeholder="model.fit(...)")
run_btn = st.button("🚀 Start Parallel Comparison")

if run_btn and user_code:
    # Preparation
    header = "# Injected by CarbonCut\nfrom green_lib.scheduler import GridScheduler\nfrom green_lib.governor import EROIGovernor\n\n"
    greened_body = user_code.replace("model.fit(", "GridScheduler().wait_for_green_window()\nmodel.fit(callbacks=[EROIGovernor()], ")
    
    st.markdown("---")
    
    # --- SECTION 2: LIVE METRICS SIDE-BY-SIDE ---
    col_std, col_grn = st.columns(2)
    
    with col_std:
        st.subheader("🔴 Standard Execution")
        std_p_stat = st.empty()
        std_c_stat = st.empty()
        
    with col_grn:
        st.subheader("🟢 CarbonCut Optimized")
        grn_p_stat = st.empty()
        grn_c_stat = st.empty()

    chart_placeholder = st.empty()
    
    # Data containers
    std_p_data, grn_p_data = [], []
    
    # --- SIMULATION LOOP ---
    for i in range(60):
        # 1. Simulate Power Draw (Watts)
        # Standard: High & Consistent | Green: Lower & Stops at i=35
        curr_std_p = 250 + np.random.randint(-15, 15)
        if i < 35:
            curr_grn_p = 175 + np.random.randint(-10, 10)
        else:
            curr_grn_p = 0 # Phase 2: EROI Gating triggered early stop
            
        std_p_data.append(curr_std_p)
        grn_p_data.append(curr_grn_p)
        
        # 2. Calculate Cumulative Carbon (Grams)
        # Standard Grid: 500g/kWh | Green Grid: 170g/kWh
        total_std_c = (sum(std_p_data) * 0.5) / 100
        total_grn_c = (sum(grn_p_data) * 0.17) / 100
        
        # 3. Update Real-time Metric Displays
        std_p_stat.metric("Current Power", f"{curr_std_p} W", "High Load", delta_color="inverse")
        std_c_stat.metric("Total CO2 Emitted", f"{total_std_c:.2f} g")
        
        grn_p_stat.metric("Current Power", f"{curr_grn_p} W", f"{(1-175/250)*100:.0f}% Less", delta_color="normal")
        grn_c_stat.metric("Total CO2 Emitted", f"{total_grn_c:.2f} g", f"-{total_std_c - total_grn_c:.2f}g saved")

        # 4. Update the Parallel Graph
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(std_p_data, color='#FF4B4B', label='Standard (Dirty Grid)', linewidth=2.5)
        ax.plot(grn_p_data, color='#00CC96', label='CarbonCut (Clean Grid)', linewidth=2.5)
        
        # Fill the "Carbon Gap" area
        ax.fill_between(range(len(std_p_data)), grn_p_data, std_p_data, color='gray', alpha=0.2, label='Energy Saved')
        
        ax.set_title("Live Power Consumption Comparison (Watts)")
        ax.set_xlabel("Elapsed Time (Seconds)")
        ax.set_ylabel("Power (W)")
        ax.set_ylim(0, 300)
        ax.legend(loc='upper right')
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        
        chart_placeholder.pyplot(fig)
        plt.close(fig)
        
        time.sleep(0.1) # Speed of comparison

    st.success(f"🏁 Comparison Finished. Total Carbon Reduction: {((total_std_c - total_grn_c)/total_std_c)*100:.1f}%")