import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# --- CONFIGURATION ---
st.set_page_config(
    page_title="ABAP AI Architect", 
    page_icon="🚀", 
    layout="wide"
)

# Load API Key from Streamlit Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing GOOGLE_API_KEY. Please add it to your Streamlit Secrets.")

# --- UI HEADER ---
st.title("🚀 ABAP-to-Functional Spec AI")
st.markdown("""
**Documentation Agent for Product Managers & SAP Consultants.** Paste your ABAP code below to generate a professional Business-Ready Functional Specification.
""")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    model_version = st.selectbox(
        "AI Model", 
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-3-flash-preview"],
        help="2.5-Flash is the standard stable workhorse. 2.5-Pro is better for deep logic."
    )
    st.info("Ensure your code follows company privacy policies before pasting.")

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Source Code")
    abap_input = st.text_area(
        "Paste ABAP Code Here:", 
        height=500, 
        placeholder="REPORT Z_SALES_ANALYSIS..."
    )

with col2:
    st.subheader("Generated Specification")
    
    if st.button("Analyze & Generate"):
        if not abap_input:
            st.warning("Please paste some code first!")
        else:
            with st.spinner("AI is reverse-engineering the logic..."):
                try:
                    # 1. Initialize Gemini
                    model = genai.GenerativeModel(model_version)
                    
                    # 2. Structured Prompt
                    prompt = f"""
                    Act as a Lead SAP Functional Consultant and Product Manager. 
                    Analyze the following ABAP code and create a professional Functional Specification (FS).
                    
                    The document must include:
                    - DOCUMENT METADATA: Program Name, Purpose, and Date.
                    - FUNCTIONAL OVERVIEW: A high-level business explanation (No technical jargon).
                    - SELECTION CRITERIA: List of all parameters and select-options.
                    - BUSINESS LOGIC: Step-by-step breakdown of how data is processed.
                    - DATA ARCHITECTURE: Identify all source tables (e.g., MARA, VBAK) and fields.
                    - PM INSIGHT: Suggest one way this code could be optimized for business ROI.

                    ABAP CODE:
                    {abap_input}
                    """
                    
                    # 3. Generate Content
                    response = model.generate_content(prompt)
                    fs_text = response.text
                    
                    # 4. Display Result
                    st.markdown(fs_text)
                    
                    # --- PDF GENERATION ---
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=11)
                    
                    # Format text for PDF compatibility
                    # We use 'replace' to handle non-latin characters Gemini might output
                    clean_text = fs_text.encode('latin-1', 'replace').decode('latin-1')
                    
                    # Add Title to PDF
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(0, 10, "Functional Specification Document", ln=True, align='C')
                    pdf.ln(5)
                    pdf.set_font("Arial", size=10)
                    pdf.multi_cell(0, 10, txt=clean_text)
                    
                    # CRITICAL FIX: Convert bytearray to bytes for Streamlit
                    pdf_data = pdf.output()
                    pdf_bytes = bytes(pdf_data)
                    
                    st.download_button(
                        label="📥 Download as PDF",
                        data=pdf_bytes,
                        file_name=f"FS_Report_{datetime.date.today()}.pdf",
                        mime="application/pdf"
                    )
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.info("The generated spec will appear here.")

# --- FOOTER ---
st.divider()
st.caption("Powered by Google Gemini | Built for the SAP Ecosystem")
