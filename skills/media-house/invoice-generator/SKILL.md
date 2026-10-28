---
name: invoice-generator
description: "Use when the user wants to generate professional invoices, quotes, estimates, or billing documents. Covers invoice templates, line items with calculations, tax/VAT handling, multi-currency support, PDF export, and automated delivery. Also use when the user mentions 'invoice', 'quote', 'estimate', 'bill', 'billing document', 'proforma invoice', or 'generate an invoice'. Can produce .pdf, .docx, or .xlsx deliverables."
argument-hint: "[client_name] [amount] [currency] [optional: line_items_json]"
metadata:
  category: office-productivity
  tools: reportlab, python-docx, openpyxl, weasyprint
---

# Invoice Generator Skill

## Triggers
- "Generate an invoice for..."
- "Create a quote/estimate..."
- "Make a billing document..."
- "Proforma invoice..."
- "Invoice with line items..."
- "Generate invoice PDF..."
- "Calculate taxes on invoice..."

## Invoice Structure

### Standard Invoice Fields
| Field | Description |
|-------|-------------|
| Invoice # | Unique identifier (e.g., INV-2026-001) |
| Date | Issue date |
| Due Date | Payment deadline |
| From | Sender/biller info |
| To | Client/buyer info |
| Line Items | Description, qty, unit price, total |
| Subtotal | Sum of line items |
| Tax/VAT | Tax rate and amount |
| Discount | Optional discount |
| Grand Total | Final amount due |
| Payment Terms | Net 30, Net 60, etc. |
| Notes | Additional terms or messages |

### Multi-Currency Support
```python
CURRENCIES = {
    'USD': {'symbol': '$', 'code': 'USD', 'decimals': 2},
    'EUR': {'symbol': '€', 'code': 'EUR', 'decimals': 2},
    'GBP': {'symbol': '£', 'code': 'GBP', 'decimals': 2},
    'JPY': {'symbol': '¥', 'code': 'JPY', 'decimals': 0},
    'CAD': {'symbol': 'C$', 'code': 'CAD', 'decimals': 2},
    'AUD': {'symbol': 'A$', 'code': 'AUD', 'decimals': 2},
    'CHF': {'symbol': 'Fr', 'code': 'CHF', 'decimals': 2},
    'CNY': {'symbol': '¥', 'code': 'CNY', 'decimals': 2},
    'INR': {'symbol': '₹', 'code': 'INR', 'decimals': 2},
    'BRL': {'symbol': 'R$', 'code': 'BRL', 'decimals': 2},
}
```

## Implementation: Python Invoice Generator

### PDF Invoice (reportlab)
```python
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

def generate_invoice_pdf(output_path, invoice_data):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, spaceAfter=20)
    label_style = ParagraphStyle('Label', parent=styles['Normal'], fontSize=10, textColor=colors.grey)
    
    elements = []
    
    # Header
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 20))
    
    # From/To section
    header_data = [
        [Paragraph("<b>From:</b>", styles['Normal']), 
         Paragraph(invoice_data['from_name'], styles['Normal']),
         Paragraph("<b>To:</b>", styles['Normal']),
         Paragraph(invoice_data['to_name'], styles['Normal'])],
        [Paragraph(invoice_data['from_address'], styles['Normal']), '',
         Paragraph(invoice_data['to_address'], styles['Normal']), ''],
    ]
    elements.append(Table(header_data, colWidths=[1.5*cm, 3*cm, 1.5*cm, 3*cm]))
    elements.append(Spacer(1, 20))
    
    # Invoice details
    details = [
        [Paragraph(f"<b>Invoice #:</b> {invoice_data['invoice_number']}", styles['Normal']),
         Paragraph(f"<b>Date:</b> {invoice_data['date']}", styles['Normal']),
         Paragraph(f"<b>Due Date:</b> {invoice_data['due_date']}", styles['Normal'])],
    ]
    elements.append(Table(details, colWidths=[3*cm, 3*cm, 3*cm]))
    elements.append(Spacer(1, 20))
    
    # Line items table
    items = invoice_data['items']
    table_data = [['Description', 'Qty', 'Unit Price', 'Total']]
    subtotal = 0
    for item in items:
        total = item['qty'] * item['price']
        subtotal += total
        table_data.append([
            item['description'],
            str(item['qty']),
            f"{invoice_data['currency']['symbol']}{item['price']:.2f}",
            f"{invoice_data['currency']['symbol']}{total:.2f}"
        ])
    
    # Totals
    tax = subtotal * invoice_data.get('tax_rate', 0)
    discount = subtotal * invoice_data.get('discount_rate', 0)
    grand_total = subtotal + tax - discount
    
    table_data += [
        ['', '', 'Subtotal:', f"{invoice_data['currency']['symbol']}{subtotal:.2f}"],
        ['', '', f"Tax ({invoice_data.get('tax_rate',0)*100:.0f}%):", f"{invoice_data['currency']['symbol']}{tax:.2f}"],
        ['', '', f"Discount ({invoice_data.get('discount_rate',0)*100:.0f}%):", f"-{invoice_data['currency']['symbol']}{discount:.2f}"],
        ['', '', '<b>Grand Total:</b>', f"<b>{invoice_data['currency']['symbol']}{grand_total:.2f}</b>"],
    ]
    
    table = Table(table_data, colWidths=[4*cm, 1.5*cm, 2.5*cm, 2.5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, -4), (-1, -4), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, -3), (-1, -3), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, -2), (-1, -2), colors.HexColor('#f8f9fa')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f4f8')),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 30))
    
    # Payment info
    payment_text = f"""<b>Payment Terms:</b> {invoice_data.get('payment_terms', 'Net 30')}
<b>Payment Method:</b> {invoice_data.get('payment_method', 'Bank Transfer')}
<b>Bank:</b> {invoice_data.get('bank_name', '')}
<b>Account:</b> {invoice_data.get('account_number', '')}
"""
    elements.append(Paragraph(payment_text, styles['Normal']))
    
    # Footer
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Thank you for your business!", styles['Normal']))
    
    doc.build(elements)
    return output_path
```

### Word Invoice (python-docx)
```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generate_invoice_docx(output_path, invoice_data):
    doc = Document()
    
    # Title
    title = doc.add_heading('INVOICE', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # From/To
    doc.add_paragraph(f"<b>From:</b> {invoice_data['from_name']}")
    doc.add_paragraph(invoice_data['from_address'])
    doc.add_paragraph(f"<b>To:</b> {invoice_data['to_name']}")
    doc.add_paragraph(invoice_data['to_address'])
    
    # Invoice info
    doc.add_paragraph(f"Invoice #: {invoice_data['invoice_number']}")
    doc.add_paragraph(f"Date: {invoice_data['date']}")
    doc.add_paragraph(f"Due Date: {invoice_data['due_date']}")
    
    # Table
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Light Grid Accent 1'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Description'
    hdr_cells[1].text = 'Qty'
    hdr_cells[2].text = 'Unit Price'
    hdr_cells[3].text = 'Total'
    
    subtotal = 0
    for item in invoice_data['items']:
        row_cells = table.add_row().cells
        row_cells[0].text = item['description']
        row_cells[1].text = str(item['qty'])
        row_cells[2].text = f"{invoice_data['currency']['symbol']}{item['price']:.2f}"
        total = item['qty'] * item['price']
        row_cells[3].text = f"{invoice_data['currency']['symbol']}{total:.2f}"
        subtotal += total
    
    doc.add_paragraph()
    doc.add_paragraph(f"Subtotal: {invoice_data['currency']['symbol']}{subtotal:.2f}")
    
    return doc
```

## Common Workflows

### Workflow: Quick Invoice
1. Collect client details (name, address, email)
2. Collect line items (description, quantity, rate)
3. Set tax rate and discount (if any)
4. Choose currency and format (PDF/DOCX/XLSX)
5. Generate and save invoice
6. Optionally email to client

### Workflow: Recurring Invoice
1. Create invoice template with client defaults
2. Set recurring schedule (monthly/quarterly)
3. Auto-generate new invoice with updated date/number
4. Apply any new line items or price changes
5. Send automatically via email

### Workflow: Quote → Invoice Conversion
1. Generate quote with same structure
2. Client approves quote
3. Convert quote to invoice (update status, add invoice number)
4. Track quote-to-invoice conversion rate

## Integration with Other Skills
- `xlsx` — generate invoices as Excel for editable formats
- `docx` — generate invoices as Word documents
- `pdf` — export invoices as PDF for delivery
- `email-templates` — generate invoice email copy
- `meeting-notes` — invoice line items from meeting scope
