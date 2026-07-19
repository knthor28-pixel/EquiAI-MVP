import streamlit as st
import pandas as pd
from core.math_engine import calculate_funnel_bias
from core.llama_agent import generate_compliance_prose

# 1. UI Page Canvas Settings
st.set_page_config(page_title="EquiAudit AI", page_icon="⚖️", layout="wide")
st.title("⚖️ EquiAudit AI")
st.subheader("Universal Fairness & Bias Optimization Platform")
st.markdown("---")

# 2. Sidebar Integration Settings
st.sidebar.header("🔌 Environment Setup")
selected_ats = st.sidebar.selectbox(
    "Target Screening Platform:",
    ["Workday Recruiting", "Greenhouse"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Ingestion Terminal")
uploaded_file = st.sidebar.file_uploader("Upload Job Requisition Outcome Log", type=["csv", "xlsx"])

# 3. Core Workspace Controller
if uploaded_file is not None:
    # Read files straight into transient memory (No persistent logging for data sovereignty)
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.success(f"Processing structural data from {selected_ats}...")
    
    # Trigger your background math logic block
    metrics = calculate_funnel_bias(df)
    
    if "error" in metrics:
        st.error(metrics["error"])
    else:
        # Layout Visual Data Panels
        tab1, tab2 = st.tabs(["📊 Audited Funnel Breakdown", "📋 Export Source Logs"])
        
        with tab2:
            st.dataframe(df, use_container_width=True)
            
        with tab1:
            st.markdown("### 📉 Candidate Conversion Analysis")
            
            # 1. Transform the backend math dictionary into a quick DataFrame for charting
            chart_records = []
            for group, data in metrics.items():
                chart_records.append({
                    "Demographic": group,
                    "Pass Rate (%)": round(data["screening_pass_rate"] * 100, 1)
                })
            
            chart_df = pd.DataFrame(chart_records).set_index("Demographic")
            
            # 2. Render an instant, beautiful visual bar chart
            st.bar_chart(chart_df, y="Pass Rate (%)", use_container_width=True)
            
            st.caption("💡 Look for steep drop-offs. A pass rate significantly lower than your highest-performing group indicates an active pipeline leak.")
            st.markdown("---")
            
            # 3. Display the interactive metric cards right below the chart
            st.markdown("### 🔍 Cohort Metrics Deep-Dive")
            c_left, c_right = st.columns(2)
            
            for i, (group, data) in enumerate(metrics.items()):
                # Alternate columns cleanly
                target_col = c_left if i % 2 == 0 else c_right
                with target_col:
                    with st.expander(f"📋 Status Log: {group}", expanded=True):
                        col1, col2 = st.columns(2)
                        col1.metric("Screening Pass Rate", f"{round(data['screening_pass_rate']*100, 1)}%")
                        col2.metric("Total Hired Count", data["final_hired"])
            
            st.markdown("---")
            
            # 4. Display the Llama action instructions at the bottom
            st.markdown(f"### 🛠️ {selected_ats} System Configuration Blueprint")
            with st.spinner(f"Querying specialized {selected_ats} mitigation rules..."):
                report = generate_compliance_prose(metrics, selected_ats)
                st.info(report)

else:
    st.info("💡 Ready for deployment tracking. Upload a pipeline outcome report in the sidebar menu to extract optimizations.")
