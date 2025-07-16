import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List
import os

class ExportService:
    def __init__(self):
        self.exports_dir = Path("exports")
        self.exports_dir.mkdir(exist_ok=True)
    
    async def export_to_pdf(self, extraction) -> str:
        """Export bill data to PDF format"""
        try:
            # Create PDF file path
            pdf_path = self.exports_dir / f"bill_extraction_{extraction.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
            story = []
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            
            # Add title
            title = Paragraph("Bill Information Extraction Report", title_style)
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Extract data
            data = extraction.extracted_data
            
            # Invoice Information
            story.append(Paragraph("Invoice Information", styles['Heading2']))
            invoice_data = [
                ["Invoice Number", data.get('invoice_number', 'N/A')],
                ["Invoice Date", data.get('invoice_date', 'N/A')]
            ]
            invoice_table = Table(invoice_data, colWidths=[2*inch, 4*inch])
            invoice_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(invoice_table)
            story.append(Spacer(1, 20))
            
            # Seller Information
            story.append(Paragraph("Seller Information", styles['Heading2']))
            seller = data.get('seller', {})
            seller_data = [
                ["Name", seller.get('name', 'N/A')],
                ["Address", seller.get('address', 'N/A')],
                ["GSTIN", seller.get('gstin', 'N/A')],
                ["Contact Number", seller.get('contact_number', 'N/A')]
            ]
            seller_table = Table(seller_data, colWidths=[2*inch, 4*inch])
            seller_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(seller_table)
            story.append(Spacer(1, 20))
            
            # Buyer Information
            story.append(Paragraph("Buyer Information", styles['Heading2']))
            buyer = data.get('buyer', {})
            buyer_data = [
                ["Name", buyer.get('name', 'N/A')],
                ["Address", buyer.get('address', 'N/A')],
                ["GSTIN", buyer.get('gstin', 'N/A')],
                ["Contact Number", buyer.get('contact_number', 'N/A')]
            ]
            buyer_table = Table(buyer_data, colWidths=[2*inch, 4*inch])
            buyer_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(buyer_table)
            story.append(Spacer(1, 20))
            
            # Items Information
            story.append(Paragraph("Items Information", styles['Heading2']))
            items = data.get('items', [])
            if items:
                items_data = [["Item Name", "Quantity", "Price/Unit", "Tax Rate", "Total Amount"]]
                for item in items:
                    items_data.append([
                        item.get('name', 'N/A'),
                        str(item.get('quantity', 'N/A')),
                        str(item.get('price_per_unit', 'N/A')),
                        str(item.get('tax_rate', 'N/A')),
                        str(item.get('total_amount', 'N/A'))
                    ])
                
                items_table = Table(items_data, colWidths=[2*inch, 0.8*inch, 1*inch, 0.8*inch, 1*inch])
                items_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(items_table)
            else:
                story.append(Paragraph("No items found", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Summary Information
            story.append(Paragraph("Summary Information", styles['Heading2']))
            summary = data.get('summary', {})
            summary_data = [
                ["Subtotal", str(summary.get('subtotal', 'N/A'))],
                ["Tax Amount", str(summary.get('tax_amount', 'N/A'))],
                ["Discount", str(summary.get('discount', 'N/A'))],
                ["Net Payable Amount", str(summary.get('net_payable_amount', 'N/A'))]
            ]
            summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(summary_table)
            
            # Build PDF
            doc.build(story)
            
            return str(pdf_path)
            
        except Exception as e:
            raise Exception(f"Error creating PDF: {str(e)}")
    
    async def export_to_csv(self, extraction) -> str:
        """Export bill data to CSV format"""
        try:
            # Create CSV file path
            csv_path = self.exports_dir / f"bill_extraction_{extraction.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Extract data
            data = extraction.extracted_data
            
            # Prepare data for CSV
            csv_data = []
            
            # Invoice Information
            csv_data.append(["Invoice Information"])
            csv_data.append(["Invoice Number", data.get('invoice_number', 'N/A')])
            csv_data.append(["Invoice Date", data.get('invoice_date', 'N/A')])
            csv_data.append([])
            
            # Seller Information
            csv_data.append(["Seller Information"])
            seller = data.get('seller', {})
            csv_data.append(["Name", seller.get('name', 'N/A')])
            csv_data.append(["Address", seller.get('address', 'N/A')])
            csv_data.append(["GSTIN", seller.get('gstin', 'N/A')])
            csv_data.append(["Contact Number", seller.get('contact_number', 'N/A')])
            csv_data.append([])
            
            # Buyer Information
            csv_data.append(["Buyer Information"])
            buyer = data.get('buyer', {})
            csv_data.append(["Name", buyer.get('name', 'N/A')])
            csv_data.append(["Address", buyer.get('address', 'N/A')])
            csv_data.append(["GSTIN", buyer.get('gstin', 'N/A')])
            csv_data.append(["Contact Number", buyer.get('contact_number', 'N/A')])
            csv_data.append([])
            
            # Items Information
            csv_data.append(["Items Information"])
            items = data.get('items', [])
            if items:
                csv_data.append(["Item Name", "Quantity", "Price/Unit", "Tax Rate", "Total Amount"])
                for item in items:
                    csv_data.append([
                        item.get('name', 'N/A'),
                        item.get('quantity', 'N/A'),
                        item.get('price_per_unit', 'N/A'),
                        item.get('tax_rate', 'N/A'),
                        item.get('total_amount', 'N/A')
                    ])
            else:
                csv_data.append(["No items found"])
            csv_data.append([])
            
            # Summary Information
            csv_data.append(["Summary Information"])
            summary = data.get('summary', {})
            csv_data.append(["Subtotal", summary.get('subtotal', 'N/A')])
            csv_data.append(["Tax Amount", summary.get('tax_amount', 'N/A')])
            csv_data.append(["Discount", summary.get('discount', 'N/A')])
            csv_data.append(["Net Payable Amount", summary.get('net_payable_amount', 'N/A')])
            
            # Create DataFrame and save to CSV
            df = pd.DataFrame(csv_data)
            df.to_csv(csv_path, index=False, header=False)
            
            return str(csv_path)
            
        except Exception as e:
            raise Exception(f"Error creating CSV: {str(e)}")
    
    async def export_to_excel(self, extraction) -> str:
        """Export bill data to Excel format"""
        try:
            # Create Excel file path
            excel_path = self.exports_dir / f"bill_extraction_{extraction.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Extract data
            data = extraction.extracted_data
            
            # Create Excel writer
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                
                # Invoice Information
                invoice_data = {
                    'Field': ['Invoice Number', 'Invoice Date'],
                    'Value': [data.get('invoice_number', 'N/A'), data.get('invoice_date', 'N/A')]
                }
                pd.DataFrame(invoice_data).to_excel(writer, sheet_name='Invoice Info', index=False)
                
                # Seller Information
                seller = data.get('seller', {})
                seller_data = {
                    'Field': ['Name', 'Address', 'GSTIN', 'Contact Number'],
                    'Value': [
                        seller.get('name', 'N/A'),
                        seller.get('address', 'N/A'),
                        seller.get('gstin', 'N/A'),
                        seller.get('contact_number', 'N/A')
                    ]
                }
                pd.DataFrame(seller_data).to_excel(writer, sheet_name='Seller Info', index=False)
                
                # Buyer Information
                buyer = data.get('buyer', {})
                buyer_data = {
                    'Field': ['Name', 'Address', 'GSTIN', 'Contact Number'],
                    'Value': [
                        buyer.get('name', 'N/A'),
                        buyer.get('address', 'N/A'),
                        buyer.get('gstin', 'N/A'),
                        buyer.get('contact_number', 'N/A')
                    ]
                }
                pd.DataFrame(buyer_data).to_excel(writer, sheet_name='Buyer Info', index=False)
                
                # Items Information
                items = data.get('items', [])
                if items:
                    items_df = pd.DataFrame(items)
                    items_df.to_excel(writer, sheet_name='Items', index=False)
                else:
                    pd.DataFrame({'Message': ['No items found']}).to_excel(writer, sheet_name='Items', index=False)
                
                # Summary Information
                summary = data.get('summary', {})
                summary_data = {
                    'Field': ['Subtotal', 'Tax Amount', 'Discount', 'Net Payable Amount'],
                    'Value': [
                        summary.get('subtotal', 'N/A'),
                        summary.get('tax_amount', 'N/A'),
                        summary.get('discount', 'N/A'),
                        summary.get('net_payable_amount', 'N/A')
                    ]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
            
            return str(excel_path)
            
        except Exception as e:
            raise Exception(f"Error creating Excel file: {str(e)}") 