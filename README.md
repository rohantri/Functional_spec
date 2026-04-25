# ABAP-to-FS AI Agent 🚀

An automated documentation agent that converts SAP ABAP code into professional Functional Specifications (FS) using Google's Gemini AI.

## 🌟 Overview
As teams transition toward S/4HANA or agile methodologies, documenting legacy ABAP code becomes a bottleneck. This tool automates that process, allowing Product Managers and Consultants to generate high-quality documentation in seconds.

## 🛠️ Tech Stack
- **Brain:** Google Gemini 2.5 Flash (via Google AI Studio)
- **Frontend:** Streamlit
- **Export:** FPDF2 (Python PDF Library)
- **Hosting:** Optimized for Streamlit Cloud / Hugging Face Spaces

## 🚀 Deployment Instructions

### 1. Get Your API Key
Generate a free API key at [Google AI Studio](https://aistudio.google.com/).

### 2. GitHub Setup
1. Create a new repository on GitHub.
2. Upload `app.py` and `requirements.txt`.

### 3. Hosting (Hugging Face / Streamlit Cloud)
1. Link your GitHub repo to the hosting service.
2. **Crucial:** Go to the "Secrets" or "Environment Variables" section of your host.
3. Add: `GOOGLE_API_KEY = "your_actual_key_here"`.

## 📖 How to Use
1. Paste your ABAP code (Reports, Classes, or Function Modules) into the app.
2. The AI identifies:
   - **Functional Overview:** The business purpose of the code.
   - **Selection Criteria:** User inputs and parameters.
   - **Business Logic:** Plain-English process steps.
   - **Tables & Fields:** Data sources used.
3. Download the generated **Functional_Spec.pdf**.

## 📄 License
MIT License - Free to use and modify for personal or professional projects.
