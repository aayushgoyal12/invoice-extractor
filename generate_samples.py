import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_sample_invoice(filename, vendor_name, gstin, inv_no, date, total_amt):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, vendor_name)
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"GSTIN: {gstin}")
    c.drawString(50, height - 85, "Tax Invoice / Bill of Supply")
    
    # Invoice Meta
    c.drawString(400, height - 50, f"Invoice No: {inv_no}")
    c.drawString(400, height - 65, f"Date: {date}")
    
    # Line items table simulation
    c.line(50, height - 110, 560, height - 110)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 130, "Description")
    c.drawString(300, height - 130, "Qty")
    c.drawString(400, height - 130, "Rate")
    c.drawString(480, height - 130, "Amount")
    c.line(50, height - 140, 560, height - 140)
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 160, "Cloud Software Subscription / Services")
    c.drawString(300, height - 160, "1")
    c.drawString(400, height - 160, str(total_amt))
    c.drawString(480, height - 160, str(total_amt))
    
    # Total
    c.line(50, height - 200, 560, height - 200)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, height - 220, "Grand Total:")
    c.drawString(480, height - 220, f"INR {total_amt}")
    
    c.save()
    print(f"Generated: {filename}")

if __name__ == "__main__":
    os.makedirs("test_invoices", exist_ok=True)
    
    # Generate 3 sample ERP digital invoices
    create_sample_invoice(
        "test_invoices/vendor_alpha.pdf", 
        "Alpha Technologies Pvt Ltd", 
        "27AAAAA0000A1Z5", 
        "INV-2026-901", 
        "18/05/2026", 
        "15400.00"
    )
    
    create_sample_invoice(
        "test_invoices/vendor_beta.pdf", 
        "Beta Enterprise Solutions", 
        "29BBBBB1111B2Z4", 
        "BETA/26-27/042", 
        "20/05/2026", 
        "48250.50"
    )
    
    create_sample_invoice(
        "test_invoices/vendor_gamma.pdf", 
        "Gamma Digital Services", 
        "07CCCCC2222C3Z3", 
        "GDS-8812", 
        "22/05/2026", 
        "9999.00"
    )
    
    print("✅ All test digital invoices generated successfully inside 'test_invoices/' folder!")