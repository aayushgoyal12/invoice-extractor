import streamlit as st
import pandas as pd
import os
from parser import extract_invoice_data

st.set_page_config(
    page_title="GST Invoice Extractor for CA Firms",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
    <style>
    .main {
        background-color: #0b0f19;
        color: #e5e7eb;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: #ffffff;
        border-radius: 10px;
        font-weight: 600;
        border: 1px solid rgba(96, 165, 250, 0.45);
        padding: 0.6rem 1rem;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.28);
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("GST Extractor Pro")
    st.markdown("---")
    st.markdown("### 📌 Scope & Limitations")
    st.info("✅ **Supported:** Text-selectable digital GST PDFs.\n\n❌ **Not Supported:** Scanned, blurry, handwritten, or image-only PDFs.")

st.title("⚡ GST Invoice PDF to Excel Converter")
st.markdown("Convert text-based digital GST invoice PDFs into a clean, review-ready Excel register for CA firms and accounting teams.")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_files = st.file_uploader(
        "Upload Digital GST Invoices (PDF)", 
        type=["pdf"], 
        accept_multiple_files=True
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    load_sample = st.button("🧪 Load Sample Data Demo")

if load_sample:
    st.session_state['use_sample'] = True

if 'use_sample' in st.session_state and st.session_state['use_sample']:
    st.success("📁 Loaded Sample Data Demo")
    sample_data = {
        "File_Name": ["Invoice_001.pdf", "Invoice_002.pdf", "Invoice_003.pdf"],
        "GSTIN": ["27AAAAA0000A1Z5", "29BBBBB1111B2Z4", "07CCCCC2222C3Z3"],
        "Invoice_No": ["INV-2026-01", "INV-2026-02", "INV-2026-03"],
        "Date": ["12/05/2026", "14/05/2026", "15/05/2026"],
        "Total_Amount": [12500.50, 45200.00, 8900.25],
        "Review_Status": ["OK", "Needs Review (Missing Tax Split)", "OK"]
    }
    df_sample = pd.DataFrame(sample_data)
    st.dataframe(df_sample, use_container_width=True)
    
    csv_sample = df_sample.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Sample Master Excel",
        data=csv_sample,
        file_name="Sample_Master_Invoice_Register.csv",
        mime="text/csv"
    )
    if st.button("🔄 Clear Sample View"):
        st.session_state['use_sample'] = False
        st.rerun()

elif uploaded_files:
    st.success(f"📁 Total {len(uploaded_files)} files uploaded successfully.")
    
    if st.button("🚀 Run Batch Extraction"):
        with st.spinner("Processing digital invoice batch..."):
            extracted_results = []
            
            for uploaded_file in uploaded_files:
                temp_path = os.path.join(".", uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                data = extract_invoice_data(temp_path)
                
                if not data["GSTIN"] or not data["Total_Amount"] or data["Total_Amount"] == 0.0:
                    data["Review_Status"] = "Needs Review (Missing Fields)"
                else:
                    data["Review_Status"] = "OK"
                
                extracted_results.append(data)
                
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
            df_master = pd.DataFrame(extracted_results)
            
            st.markdown("---")
            st.subheader("📊 Extracted Data Preview & Review Status")
            st.dataframe(df_master, use_container_width=True)
            
            csv_data = df_master.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Master Excel Register",
                data=csv_data,
                file_name="Master_Invoice_Register.csv",
                mime="text/csv"
            )
else:
    st.warning("⚠️ Please upload digital PDF invoices or click 'Load Sample Data Demo' to preview the workflow.")