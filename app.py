import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# 1. Setup Gemini API Key from Streamlit Secrets
# (You will set this up in Hugging Face or Streamlit Cloud settings)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Missing GOOGLE_API_KEY. Please add it to your secrets.")

st.set_page_config(page_title="ABAP FS Generator", layout="wide")

st.title("📊 ABAP Functional Spec Agent")
st.write("Professional documentation tool for SAP Consultants & PMs.")

# Selection for Model
model_choice = st.sidebar.selectbox("Select Model", ["gemini-2.5-flash", "gemini-2.5-pro"])

# User Input
abap_code = st.text_area("Paste your ABAP Code here:", height=400, placeholder="REPORT Z_TEST...")

if st.button("Generate Spec & Export PDF"):
    if abap_code:
        with st.spinner("Gemini is analyzing your ABAP logic..."):
            try:
                model = genai.GenerativeModel(model_choice)
                
                prompt = f"""
                Act as a Senior SAP Functional Consultant. Analyze the provided ABAP code and generate a 
                comprehensive Functional Specification (FS) document.
                
                STRUCTURE:
                1. Functional Overview (Business purpose)
                2. Selection Screen (Input parameters)
                3. Detailed Process Logic (Step-by-step business rules)
                4. Tables & Fields (Identify MARA, VBAK, etc.)
                5. Output/UI (ALV, File, or Form details)
                
                ABAP CODE:
                {abap_code}
                """
                
                response = model.generate_content(prompt)
                fs_text = response.text
                
                # Display Result
                st.success("Analysis Complete!")
                st.markdown(fs_text)
                
                # PDF Generation
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=11)
                
                # Handle potential encoding issues from AI text
                clean_text = fs_text.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 10, txt=clean_text)
                
                pdf_bytes = pdf.output(dest='S')
                
                st.download_button(
                    label="📥 Download Functional Spec (PDF)",
                    data=pdf_bytes,
                    file_name="ABAP_Functional_Spec.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please paste your code to proceed.")