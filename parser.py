import pdfplumber
import re

def extract_invoice_data(pdf_path):
    extracted_data = {
        "File_Name": pdf_path.split("/")[-1],
        "GSTIN": None,
        "Invoice_No": None,
        "Date": None,
        "Total_Amount": 0.0
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        
        # Micro-Step 4: Scanned PDF Error Guard
        if len(full_text.strip()) < 20:
            # Indicates image-based scan with no selectable text layer
            extracted_data["Review_Status"] = "Error: Scanned/Image PDF (Unsupported)"
            return extracted_data

        # 1. Extract GSTIN (15 character standard regex)
        gstin_pattern = r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}'
        gstin_match = re.search(gstin_pattern, full_text)
        if gstin_match:
            extracted_data["GSTIN"] = gstin_match.group(0)
            
        # 2. Extract Invoice Number
        inv_pattern = r'(?:Invoice\s*No\.?|Inv\s*No\.?|Bill\s*No\.?)\s*[:\-]?\s*([A-Za-z0-9\-/]+)'
        inv_match = re.search(inv_pattern, full_text, re.IGNORECASE)
        if inv_match:
            extracted_data["Invoice_No"] = inv_match.group(1)
            
        # 3. Extract Date
        date_pattern = r'\b(0[1-9]|[12][0-9]|3[01])[-/](0[1-9]|1[0-2])[-/](20\d{2})\b'
        date_match = re.search(date_pattern, full_text)
        if date_match:
            extracted_data["Date"] = date_match.group(0)
            
        # 4. Extract Total Amount
        total_pattern = r'(?:Grand\s*Total|Total\s*Amount|Total|Balance\s*Due)\s*[:\-]?\s*(?:INR|Rs\.?)?\s*([\d,]+\.\d{2})'
        total_match = re.search(total_pattern, full_text, re.IGNORECASE)
        if total_match:
            amt_str = total_match.group(1).replace(',', '')
            extracted_data["Total_Amount"] = float(amt_str)
            
    return extracted_data