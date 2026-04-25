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
st.markdown("Automated documentation for SAP Consultants. Upload an ABAP file or paste code below.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Configuration")
    model_version = st.selectbox(
        "AI Model", 
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-3-flash-preview"],
        index=0
    )
    st.divider()
    st.info("Supported files: .abap, .txt, .sap")

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Source")
    
    # 1. File Uploader Component
    uploaded_file = st.file_uploader("Upload ABAP File", type=['abap', 'txt', 'sap'])
    
    # 2. Text Area (as fallback)
    st.markdown("**OR** paste your code here:")
    abap_input = st.text_area("", height=300, placeholder="REPORT Z_SALES_ANALYSIS...")

    # Logic to decide which input to use
    final_code = ""
    if uploaded_file is not None:
        # Read the file and convert to string
        final_code = uploaded_file.read().decode("utf-8")
        st.success(f"File '{uploaded_file.name}' loaded successfully!")
    else:
        final_code = abap_input

with col2:
    st.subheader("Generated Specification")
    
    if st.button("Generate Spec & PDF"):
        if not final_code:
            st.warning("Please upload a file or paste code first!")
        else:
            with st.spinner("Analyzing ABAP logic..."):
                try:
                    model = genai.GenerativeModel(model_version)
                    
                    prompt = f"""
                    Act as a Lead SAP Functional Consultant. 
                    Analyze the following ABAP code and create a professional Functional Specification (FS).
                    
                    STRUCTURE:
                    1. DOCUMENT METADATA (Program Name, Date)
                    2. FUNCTIONAL OVERVIEW (Business purpose)
                    3. SELECTION CRITERIA (Parameters/Select-options)
                    4. BUSINESS LOGIC (Step-by-step processing)
                    5. TABLES & FIELDS (Data sources)
                    6. PM INSIGHT (Optimization suggestion)

                    ABAP CODE:
                    {final_code}
                    """
                    
                    response = model.generate_content(prompt)
                    fs_text = response.text
                    
                    st.markdown(fs_text)
                    
                    # PDF GENERATION
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=10)
                    
                    # Handle encoding for PDF
                    clean_text = fs_text.encode('latin-1', 'replace').decode('latin-1')
                    pdf.multi_cell(0, 8, txt=clean_text)
                    
                    # Convert to bytes for download
                    pdf_data = pdf.output()
                    pdf_bytes = bytes(pdf_data)
                    
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_bytes,
                        file_name=f"FS_Report_{datetime.date.today()}.pdf",
                        mime="application/pdf"
                    )
                    
                except Exception as e:
                    st.error(f"Error: {e}")
