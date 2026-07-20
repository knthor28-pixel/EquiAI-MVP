import os
import pandas as pd
import streamlit as st
from core.math_engine import calculate_funnel_bias
from core.llama_agent import generate_compliance_prose

def run_local_test():
    print("🚀 Initializing EquiAudit AI Local Test Pipeline...\n")
    
    # 1. Load the mock data
    csv_path = "mock_hiring_data.csv"
    if not os.path.exists(csv_path):
        print(f"❌ Error: Could not find {csv_path}. Please create the file first.")
        return
        
    df = pd.read_csv(csv_path)
    print(f"📥 Successfully loaded {len(df)} candidate rows from CSV.")
    
    # 2. Execute your Math Engine
    print("🧮 Executing math engine funnel calculations...")
    metrics = calculate_funnel_bias(df)
    
    print("\n--- [Calculated Backend Metrics] ---")
    for group, data in metrics.items():
        print(f"Cohort: {group}")
        print(f"  - Total Applicants: {data['total_applicants']}")
        print(f"  - Passed Screen: {data['passed_screening']}")
        print(f"  - Screening Pass Rate: {round(data['screening_pass_rate'] * 100, 1)}%")
        print(f"  - Final Hired: {data['final_hired']}")
    print("------------------------------------\n")
    
    # Mocking streamlit secrets for local command line testing if required
    if "GROQ_API_KEY" not in st.secrets:
        # Fallback to system environment variable if running outside streamlit
        if "GROQ_API_KEY" in os.environ:
            st.secrets["GROQ_API_KEY"] = os.environ["GROQ_API_KEY"]
        else:
            print("❌ Error: GROQ_API_KEY not found in environment variables or .streamlit/secrets.toml")
            return

    # 3. Execute your Llama Diagnostic Prompt (Testing for Greenhouse)
    target_ats = "Greenhouse"
    print(f"🤖 Querying Llama 3.3 for {target_ats} diagnostic analysis and fixes...")
    
    report = generate_compliance_prose(metrics, target_ats)
    
    print("\n====================================================")
    print(f"📄 GENERATED EQUIAUDIT REPORT FOR: {target_ats}")
    print("====================================================")
    print(report)
    print("====================================================\n")
    print("✅ Test pipeline successfully completed.")

if __name__ == "__main__":
    run_local_test()
