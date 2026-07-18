"""
2. The Context-Aware AI Generator (core/llama_agent.py)
This script pulls our Groq key directly from Streamlit’s native server environment and wraps our metrics inside platform-specific software fixes.
"""

import streamlit as st
from groq import Groq

def generate_compliance_prose(funnel_metrics: dict, ats_system: str) -> str:
    if "GROQ_API_KEY" not in st.secrets:
        return "Error: Groq API key configuration missing from host settings."
        
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    system_prompt = (
        f"You are an elite enterprise HR data scientist and certified audit specialist in {ats_system}.\n"
        "Analyze the provided demographic stage-by-stage hiring funnel metrics for systemic bias.\n\n"
        "Your output must follow this strict 4-section format using clean Markdown layout:\n\n"
        "### 🔍 1. Funnel Leak Identification\n"
        "(Clearly identify which protected subgroup is dropping off and at what specific stage of the hiring pipeline based on the numbers.)\n\n"
        "### 🧠 2. Diagnostic Analysis (The 'Why')\n"
        f"Identify and explain the highly probable technical or systemic reasons *why* this bias is occurring inside {ats_system}.\n"
        f"- If the leak is at the Screening stage, explain how {ats_system}'s specific screening mechanisms (e.g., historical calibration weights in Workday, semantic text prompt calibration in Greenhouse, or rigid knockout criteria in Oracle) translate the data patterns into biased outcomes.\n"
        "- If the leak is at the Interview stage, explain how human bias or unstructured evaluation criteria are overriding the initial software recommendations.\n"
        "- Provide realistic examples of what features (like employment gaps, non-traditional education, or keyword over-weighting) are triggering this drop-off.\n\n"
        "### ⚙️ 3. Targeted Systemic Fixes\n"
        f"(Provide concrete, step-by-step instructions on how to adjust parameters *specifically inside {ats_system}* to mathematically correct this error for future job descriptions. Use native platform menu paths and terminology.)\n\n"
        "### 🛠️ 4. Immediate Operational Action\n"
        "(Give one single, high-priority manual task the recruiting team can run today to retrieve impacted candidates from this specific cohort.)"
    )
    
    user_prompt = f"Analyze these metrics and generate the comprehensive {ats_system} diagnostic report:\n{funnel_metrics}"
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.2 # Kept low to ensure it cross-references the data accurately without hallucinating outside patterns
    )
    return response.choices[0].message.content
