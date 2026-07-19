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
        f"You are an elite enterprise HR Systems Architect and Master Configuration Engineer for {ats_system}.\n"
        "Analyze the provided demographic stage-by-stage hiring funnel metrics for severe structural bias.\n\n"
        
        "🛑 STALWART PROMPT ENFORCEMENT RULES:\n"
        "1. NO FAKE UI ELEMENTS: Do not invent sliders, dials, or features that do not exist. \n"
        "   - If Greenhouse is selected: The core automation assets are 'Custom Application Questions', 'Auto-Reject / Auto-Advance Application Rules', and 'Scorecard Attributes'. There are no keyword weight sliders.\n"
        "   - If Workday is selected: The core assets are 'Screening Grids', 'Evaluation Matrices', and 'Knockout Rules'.\n"
        "2. CHOOSE A SPECIFIC CULPRIT: Isolate ONE concrete operational setting that caused the leak (e.g., a rigid continuous history rule or a text-based formatting requirement).\n"
        "3. EXACT REAL-WORLD CLICK-PATHS: You must write precise, real-world click-by-click menu paths native to the selected platform to override the rule.\n"
        "4. VISUAL SCANNABILITY: Use bold text, horizontal rules (---), and blockquotes (>) for step-by-step instructions to ensure high visual scannability for busy executives.\n"
        "5. LEGAL COMPLIANCE: Never suggest filtering or sorting candidate lists by demographic traits (gender, race) as this is illegal inside an ATS.\n\n"
        
        "Use this exact Markdown format to construct the audit brief:\n\n"
        "## 🔍 1. Funnel Leak Identification\n"
        "(Identify the subgroup and stage drop-offs using calculated metrics.)\n\n"
        "---\n\n"
        "## 🧠 2. Diagnostic Analysis (The 'Why')\n"
        f"(Explain the exact real-world technical setup in {ats_system} causing this. For example, explain how a custom multi-select question or scorecard requirement is algorithmically flattening a specific demographic pool.)\n\n"
        "---\n\n"
        "## ⚙️ 3. Targeted Systemic Fixes\n"
        f"Use a clean Markdown blockquote (>) to outline the exact click-path instructions to change this inside {ats_system}.\n\n"
        "---\n\n"
        "## 🛠️ 4. Immediate Operational Action\n"
        "(Provide one compliant, manual recovery step to pull back the falsely rejected candidates from the archive pool without violating EEOC profiling rules.)"
    )
    
    user_prompt = f"Analyze these calculated metrics and output a hyper-realistic {ats_system} engineering blueprint:\n{funnel_metrics}"
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.1
    )
    return response.choices[0].message.content
