import streamlit as st
from groq import Groq

def generate_compliance_prose(funnel_metrics: dict, ats_system: str) -> str:
    # Production Safeguard: Read API credentials securely from Streamlit secrets
    if "GROQ_API_KEY" not in st.secrets:
        return "Error: Groq API key configuration missing from host settings."
        
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    system_prompt = (
        f"You are a master enterprise configuration consultant specializing in {ats_system} Recruiting.\n"
        "Analyze the provided demographic stage-by-stage hiring funnel metrics for systemic bias.\n\n"
        "Your output must follow this 3-section format using clean Markdown text layout:\n\n"
        "### 🔍 1. Funnel Leak Identification\n"
        "(Identify exactly which subgroup is dropping off and at what stage of the pipeline.)\n\n"
        "### ⚙️ Targeted Systemic Fixes\n"
        f"(Provide concrete, step-by-step instructions on how to adjust parameters *specifically inside {ats_system}* "
        "to fix this error for future job descriptions. Use native platform vocabulary. "
        "For example, if Greenhouse is selected, reference Calibration, Application Rules, or Scorecards. "
        "If Workday is selected, reference Job Requisition Parameters, Screening Grids, or Disposition Reasons.)\n\n"
        "### 🛠️ Immediate Operational Action\n"
        "(Give one single, manual task the recruiting team can run today to save top candidate files.)"
    )
    
    user_prompt = f"Analyze these metrics and generate the tailored {ats_system} optimization brief:\n{funnel_metrics}"
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.15
    )
    return response.choices[0].message.content