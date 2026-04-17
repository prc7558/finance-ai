from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import os

def generate_pdf_report(user, accounts, metrics, insights, df):
    """
    Generate a comprehensive PDF financial report
    """
    # Create temporary folder for PDFs
    pdf_folder = 'temporary'
    os.makedirs(pdf_folder, exist_ok=True)
    
    filename = f"financial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(pdf_folder, filename)
    
    # Create PDF
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    story.append(Paragraph("Financial Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # User Information
    story.append(Paragraph("Personal Information", heading_style))
    user_data = [
        ["Name:", user.get('name', 'N/A')],
        ["Email:", user.get('email', 'N/A')],
        ["Phone:", user.get('phone', 'N/A')],
        ["Report Date:", datetime.now().strftime('%B %d, %Y')]
    ]
    user_table = Table(user_data, colWidths=[2*inch, 4*inch])
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f4ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(user_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Financial Summary
    story.append(Paragraph("Financial Summary", heading_style))
    summary_data = [
        ["Metric", "Amount"],
        ["Total Income", f"Rs. {metrics.get('total_income', 0):,.2f}"],
        ["Total Expenses", f"Rs. {metrics.get('total_expenses', 0):,.2f}"],
        ["Net Change", f"Rs. {metrics.get('net_change', 0):,.2f}"],
        ["Current Balance", f"Rs. {metrics.get('total_balance', 0):,.2f}"]
    ]
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Connected Accounts
    story.append(Paragraph("Connected Accounts", heading_style))
    account_data = [["#", "Bank/Platform", "Type", "Balance"]]
    for i, acc in enumerate(accounts, 1):
        account_data.append([
            str(i),
            acc.get('bank_name', 'Unknown'),
            acc.get('account_type', 'Bank'),
            f"Rs. {acc.get('balance', 0):,.2f}"
        ])
    
    account_table = Table(account_data, colWidths=[0.5*inch, 2.5*inch, 1.5*inch, 1.5*inch])
    account_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    story.append(account_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Spending by Category
    if 'categories' in metrics and metrics['categories']:
        story.append(Paragraph("Spending by Category", heading_style))
        category_data = [["Category", "Amount", "Percentage"]]
        total_spending = sum(metrics['categories'].values())
        
        for category, amount in sorted(metrics['categories'].items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_spending * 100) if total_spending > 0 else 0
            category_data.append([
                category,
                f"₹{amount:,.2f}",
                f"{percentage:.1f}%"
            ])
        
        category_table = Table(category_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        category_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        story.append(category_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Insights
    if insights:
        story.append(Paragraph("Key Insights", heading_style))
        for insight in insights:
            insight_text = f"<b>{insight.get('title', '')}:</b> {insight.get('message', '')}"
            story.append(Paragraph(insight_text, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        story.append(Spacer(1, 0.2*inch))
    
    # Recent Transactions
    story.append(Paragraph("Recent Transactions", heading_style))
    recent_df = df.tail(15)
    transaction_data = [["Date", "Description", "Amount", "Bank"]]
    
    for _, row in recent_df.iterrows():
        transaction_data.append([
            str(row['date'].date()) if hasattr(row['date'], 'date') else str(row['date']),
            str(row['description'])[:40],  # Truncate long descriptions
            f"Rs. {row['amount']:,.2f}",
            str(row.get('bank_name', 'N/A'))[:15]
        ])
    
    transaction_table = Table(transaction_data, colWidths=[1*inch, 2.5*inch, 1.2*inch, 1.3*inch])
    transaction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
    ]))
    story.append(transaction_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Generated by Finance AI - Your Personal Financial Assistant", footer_style))
    story.append(Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", footer_style))
    
    # Build PDF
    doc.build(story)
    
    return filepath
