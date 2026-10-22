"""Generate sample invoice PDFs for testing and demonstration."""

from pathlib import Path
import sys

def generate_invoices():
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    out_dir = Path(__file__).resolve().parent / "sample_invoices"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Invoice 1: Standard Supplier Invoice (Aggarwal Wholesale Traders)
    inv1_path = out_dir / "invoice_aggarwal_traders.pdf"
    c1 = canvas.Canvas(str(inv1_path), pagesize=letter)
    c1.setFont("Helvetica-Bold", 18)
    c1.drawString(50, 740, "TAX INVOICE")

    c1.setFont("Helvetica", 10)
    c1.drawString(50, 715, "Vendor: Aggarwal Wholesale Traders")
    c1.drawString(50, 700, "GSTIN: 07AAAAA0000A1Z5")
    c1.drawString(50, 685, "Invoice No: AGG/2026/089")
    c1.drawString(50, 670, "Date: 2026-07-15")

    c1.drawString(350, 715, "Billed To: Kumar General Store")
    c1.drawString(350, 700, "Address: Shop 12, Main Market")
    c1.drawString(350, 685, "New Delhi, 110001")

    # Table Header
    c1.line(50, 640, 550, 640)
    c1.setFont("Helvetica-Bold", 10)
    c1.drawString(50, 625, "Item Description")
    c1.drawString(280, 625, "Qty")
    c1.drawString(360, 625, "Rate (INR)")
    c1.drawString(460, 625, "Amount (INR)")
    c1.line(50, 615, 550, 615)

    # Line Items
    c1.setFont("Helvetica", 10)
    c1.drawString(50, 595, "Basmati Rice 25kg Bag")
    c1.drawString(280, 595, "4")
    c1.drawString(360, 595, "2000.00")
    c1.drawString(460, 595, "8000.00")

    c1.drawString(50, 570, "Toor Dal Premium 10kg")
    c1.drawString(280, 570, "5")
    c1.drawString(360, 570, "1300.00")
    c1.drawString(460, 570, "6500.00")

    c1.drawString(50, 545, "Mustard Oil 15L Tin")
    c1.drawString(280, 545, "2")
    c1.drawString(360, 545, "2100.00")
    c1.drawString(460, 545, "4200.00")

    # Totals
    c1.line(50, 520, 550, 520)
    c1.drawString(360, 500, "Subtotal:")
    c1.drawString(460, 500, "18700.00")

    c1.drawString(360, 480, "GST (5%):")
    c1.drawString(460, 480, "935.00")

    c1.setFont("Helvetica-Bold", 11)
    c1.drawString(360, 455, "Total Amount:")
    c1.drawString(460, 455, "19635.00")
    c1.line(350, 445, 550, 445)

    c1.showPage()
    c1.save()
    print(f"[OK] Generated {inv1_path}")

    # 2. Invoice 2: Farm Produce Receipt (Sharma Vegetable Mandi)
    inv2_path = out_dir / "invoice_sharma_mandi.pdf"
    c2 = canvas.Canvas(str(inv2_path), pagesize=letter)
    c2.setFont("Helvetica-Bold", 16)
    c2.drawString(50, 740, "ESTIMATE / MANDI SLIP")

    c2.setFont("Helvetica", 10)
    c2.drawString(50, 715, "Supplier: Sharma Farm Produce")
    c2.drawString(50, 700, "Date: 2026-07-20")
    c2.drawString(50, 685, "Bill No: SH-4412")

    c2.drawString(350, 715, "Customer: Kumar General Store")

    c2.line(50, 650, 550, 650)
    c2.setFont("Helvetica-Bold", 10)
    c2.drawString(50, 635, "Item")
    c2.drawString(250, 635, "Quantity (kg)")
    c2.drawString(350, 635, "Rate (INR/kg)")
    c2.drawString(450, 635, "Total (INR)")
    c2.line(50, 625, 550, 625)

    c2.setFont("Helvetica", 10)
    c2.drawString(50, 605, "Fresh Red Onion")
    c2.drawString(250, 605, "100")
    c2.drawString(350, 605, "28.00")
    c2.drawString(450, 605, "2800.00")

    c2.drawString(50, 580, "Potato (Jyoti)")
    c2.drawString(250, 580, "80")
    c2.drawString(350, 580, "22.00")
    c2.drawString(450, 580, "1760.00")

    c2.line(50, 555, 550, 555)
    c2.setFont("Helvetica-Bold", 11)
    c2.drawString(350, 535, "Net Payable:")
    c2.drawString(450, 535, "4560.00")

    c2.showPage()
    c2.save()
    print(f"[OK] Generated {inv2_path}")


if __name__ == "__main__":
    generate_invoices()
