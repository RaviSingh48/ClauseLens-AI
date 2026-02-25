import os
import json
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from utils import extract_text_from_pdf, chunk_text

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a senior legal contract analyst AI.

Return ONLY valid JSON.
Do not explain reasoning.
If information missing return "Not Found".

Extract:

1. Key Parties:
- Party A
- Party B
- Additional Parties

2. Contract Overview:
- Contract Type
- Effective Date
- Duration
- Renewal Terms

3. Payment Terms:
- Payment Amount
- Payment Frequency
- Late Fees

4. Termination:
- Termination Conditions
- Notice Period
- Exit Rights

5. Confidentiality Clause:
- Present (Yes/No)
- Summary

6. Risk Flags:
For each:
- risk_level (Low/Medium/High)
- explanation
- exact_clause_excerpt

Categories:
- Auto-Renewal Risk
- Liability & Indemnity Risk
- Missing Exit Clause Risk
- Intellectual Property Ownership Risk

7. Plain English Summary (5–7 sentences)

Return JSON in this structure:
{
  "key_parties": {},
  "contract_overview": {},
  "payment_terms": {},
  "termination": {},
  "confidentiality_clause": {},
  "risk_flags": {},
  "plain_english_summary": ""
}
"""

def analyze_contract(text):
    chunks = chunk_text(text)
    combined_text = " ".join(chunks)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # Free & Stable Model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": combined_text}
            ],
            temperature=0.2,
            max_tokens=2000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"API Error: {str(e)}"


# ================= STREAMLIT UI =================

st.title("📄 ClauseLens AI - Contract Review Bot")

uploaded_file = st.file_uploader("Upload Contract PDF", type=["pdf"])
text_input = st.text_area("Or Paste Contract Text")

if st.button("Analyze Contract"):

    if uploaded_file:
        contract_text = extract_text_from_pdf(uploaded_file)
    elif text_input:
        contract_text = text_input
    else:
        st.error("Please upload or paste contract text.")
        st.stop()

    with st.spinner("Analyzing contract using LLaMA 3..."):
        result = analyze_contract(contract_text)

    # If API returned error
    if result.startswith("API Error"):
        st.error(result)
        st.stop()

    # Try parsing JSON safely
    try:
        data = json.loads(result)
    except:
        st.error("Model did not return valid JSON. Please try again.")
        st.write("Raw Output:")
        st.code(result)
        st.stop()

    # Display structured output
    st.header("Key Parties")
    st.write(data.get("key_parties", {}))

    st.header("Contract Overview")
    st.write(data.get("contract_overview", {}))

    st.header("Payment Terms")
    st.write(data.get("payment_terms", {}))

    st.header("Termination")
    st.write(data.get("termination", {}))

    st.header("Confidentiality")
    st.write(data.get("confidentiality_clause", {}))

    st.header("Risk Flags")

    risk_flags = data.get("risk_flags", {})
    for risk, details in risk_flags.items():
        level = details.get("risk_level", "Low")

        if level == "High":
            st.error(f"{risk}: {details.get('explanation')}")
        elif level == "Medium":
            st.warning(f"{risk}: {details.get('explanation')}")
        else:
            st.success(f"{risk}: {details.get('explanation')}")

    st.header("Plain English Summary")
    st.write(data.get("Plain_english_summary", ""))

    st.download_button(
        "Download Full JSON Report",
        json.dumps(data, indent=2),
        file_name="contract_analysis.json"
    )