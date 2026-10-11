import io
import pandas as pd
from datetime import datetime


def to_excel(df: pd.DataFrame, sheet_name: str = "Report") -> bytes:
    """Convert DataFrame to Excel bytes for download."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()


def to_csv(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to CSV bytes for download."""
    return df.to_csv(index=False).encode('utf-8')


def to_pdf(df: pd.DataFrame, title: str = "Report") -> bytes:
    """Convert DataFrame to PDF bytes for download."""
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors

    output = io.BytesIO()
    doc = SimpleDocTemplate(
        output,
        pagesize=landscape(letter),
        rightMargin=30, leftMargin=30,
        topMargin=30, bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_para = Paragraph(f"<b>IntelliBank — {title}</b>", styles['Title'])
    elements.append(title_para)

    # Timestamp
    ts = Paragraph(
        f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}",
        styles['Normal']
    )
    elements.append(ts)
    elements.append(Spacer(1, 12))

    # Table data
    data = [list(df.columns)] + df.astype(str).values.tolist()

    # Column widths (auto-fit)
    col_width = (landscape(letter)[0] - 60) / max(len(df.columns), 1)

    table = Table(data, colWidths=[col_width] * len(df.columns))
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#00d4ff")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f0f4f8")]),
    ]))

    elements.append(table)
    doc.build(elements)
    return output.getvalue()