import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# 1. Page Configuration
st.set_page_config(page_title="CreatorSync Pro | Ultra Contrast", layout="wide")

# 2. Ultra-Contrast Glassmorphism CSS
st.markdown("""
    <style>
    /* Darkest possible background for maximum contrast */
    .stApp { 
        background: #000000; 
        color: #FFFFFF; 
    }
    
    /* Metrics with glowing neon borders */
    div[data-testid="stMetric"] {
        background: #0a0a0a;
        border: 2px solid #7d33ff;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 0 15px rgba(125, 51, 255, 0.2);
    }
    
    /* Neon Blue for Labels, Pure White for Values */
    div[data-testid="stMetricLabel"] { color: #00d4ff !important; font-weight: bold !important; font-size: 1.1rem !important; }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 2.5rem !important; }

    /* Button with high-contrast gradient and glow */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #7d33ff 0%, #00d4ff 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        font-weight: 800;
        text-transform: uppercase;
        padding: 1rem;
        box-shadow: 0 5px 20px rgba(0, 212, 255, 0.3);
    }
    
    /* Table Visibility Enhancements */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Terminal Sidebar
with st.sidebar:
    st.markdown("## 🛠️ SYSTEM LOGS")
    st.code(f"SYS_TIME: {time.strftime('%H:%M:%S')}\nSTATUS: READY\nENV: PRODUCTION")
    st.divider()
    
    if st.button("🚀 EXECUTE OPTIMIZATION"):
        start = time.perf_counter()
        with st.status("Computing engagement vectors...", expanded=False):
            try:
                response = requests.get("http://127.0.0.1:8000/run-optimizer")
                latency = round(time.perf_counter() - start, 3)
                if response.status_code == 200:
                    st.success(f"PROCESSED IN {latency}s")
                    st.rerun()
            except:
                st.error("BACKEND_OFFLINE")

    st.divider()
    search_id = st.text_input("🔍 SEARCH CREATOR_ID", placeholder="Enter ID...")

# 4. Dashboard Header
st.title("💠 CREATORSYNC ULTRA-LITE")
st.markdown("##### *Strategic Posting Intelligence | Version 2.0*")
st.divider()

# 5. Data Visualization Logic
try:
    data_response = requests.get("http://127.0.0.1:8000/get-results")
    if data_response.status_code == 200:
        df = pd.DataFrame(data_response.json())

        # Main KPI Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("CONTENT_TOTAL", len(df))
        c2.metric("TOP_PLATFORM", df['platform'].mode()[0].upper())
        c3.metric("PEAK_SLOT", f"{df['time_slot'].mode()[0]}:00")
        c4.metric("SYSTEM_SYNC", time.strftime("%H:%M"))

        # Analytics Row
        st.markdown("### 📊 PERFORMANCE ANALYTICS")
        left, right = st.columns([1, 1])

        with left:
            # High-contrast Donut Chart
            fig_pie = px.pie(df, names='platform', hole=0.7, 
                             color_discrete_sequence=['#7d33ff', '#00d4ff'])
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", 
                                  legend=dict(orientation="h", yanchor="bottom", y=-0.2))
            st.plotly_chart(fig_pie, use_container_width=True)

        with right:
            # High-contrast Histogram
            fig_hist = px.histogram(df, x="time_slot", nbins=24, color_discrete_sequence=['#00d4ff'])
            fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                   font_color="white", xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                                   yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
            st.plotly_chart(fig_hist, use_container_width=True)

        # High-visibility Data Explorer
        st.markdown("### 🔍 RECENT RECOMMENDATIONS")
        if search_id:
            display_df = df[df['content_id'].astype(str).str.contains(search_id)]
        else:
            display_df = df.head(15)
            
        st.dataframe(display_df, use_container_width=True)

except:
    st.warning("⚠️ ENGINE DATA NOT FOUND. PLEASE EXECUTE OPTIMIZATION TO GENERATE THE SUBMISSION_CSV.")