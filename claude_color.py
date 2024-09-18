import os
import sys
from reportlab.lib.pagesizes import A0, A1, A2, A3, A4, letter, LEDGER, LEGAL
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Global variables
FILE_OUTPUT = "affirmations.pdf"
SPACE_BETWEEN_LINES = 2 * mm
CELL_BORDER_SPACE = 3 * mm
CARD_FONT = os.path.expanduser("~/.fonts/Anton-Regular.ttf")
CELL_FONT_COLOR = "#6c757d"  # Black

# Background colors for cells
background_colors = ['#caf0f8', '#90e0ef', '#a2d2ff', '#a2d2ff']

# Register the Anton font
pdfmetrics.registerFont(TTFont('Anton', CARD_FONT))

# Define available page sizes and their corresponding font sizes
PAGE_SIZES = {
    'letter': {'size': letter, 'font_size': 18},
    'legal': {'size': LEGAL, 'font_size': 18},
    'a4': {'size': A4, 'font_size': 24},
    'a3': {'size': A3, 'font_size': 34},
    'a2': {'size': A2, 'font_size': 44},
    'a1': {'size': A1, 'font_size': 54},
    'a0': {'size': A0, 'font_size': 64},
    'leger': {'size': LEDGER, 'font_size': 34}
}

def create_dynamic_table_pdf(filename, data_file, page_size_key):
    page_size = PAGE_SIZES[page_size_key]['size']
    font_size = PAGE_SIZES[page_size_key]['font_size']

    # Define 5 mm margins
    margin = 5 * mm
    
    # Define page size (without margins)
    page_width, page_height = page_size
    usable_width = page_width - 2 * margin
    usable_height = page_height - 2 * margin
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=page_size,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    
    elements = []
    
    # Read data from txt file
    with open(data_file, 'r') as file:
        lines = file.readlines()
    
    # Clean data and remove line breaks
    lines = [line.strip() for line in lines]
    
    # Ensure data is filled in multiples of 9 (for a 3x3 table)
    while len(lines) % 9 != 0:
        lines.append('')  # Add empty cells if necessary
    
    # Create a custom style for the cell content
    from reportlab.lib.styles import ParagraphStyle
    cell_style = ParagraphStyle(
        'CellStyle',
        fontName='Anton',
        fontSize=font_size,
        leading=font_size + SPACE_BETWEEN_LINES,
        alignment=1,  # Center alignment
        textColor=CELL_FONT_COLOR
    )
    
    # Calculate cell dimensions
    cell_width = (usable_width - 2 * CELL_BORDER_SPACE) / 3
    cell_height = (usable_height - 2 * CELL_BORDER_SPACE) / 3
    
    # Divide into blocks of 9 elements (3 rows of 3 columns)
    for i in range(0, len(lines), 9):
        chunk = lines[i:i+9]
        data = []
        for j in range(0, 9, 3):
            row = [Paragraph(cell, cell_style) for cell in chunk[j:j+3]]
            data.append(row)
        
        # Create table without headers that occupies 100% of available width and height
        table = Table(data, colWidths=[cell_width] * 3, rowHeights=[cell_height] * 3)
        
        # Table style with alignment, dynamic text wrapping, and custom styling
        style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), CELL_BORDER_SPACE / 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), CELL_BORDER_SPACE / 2),
            ('TOPPADDING', (0, 0), (-1, -1), CELL_BORDER_SPACE / 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), CELL_BORDER_SPACE / 2),
        ])
        
        # Add different background colors for each cell
        for row in range(3):
            for col in range(3):
                color_index = (row * 3 + col) % len(background_colors)
                style.add('BACKGROUND', (col, row), (col, row), background_colors[color_index])
        
        table.setStyle(style)
        
        # Add table to elements
        elements.append(table)
        
        # Add a page break after each table, except for the last one
        if i + 9 < len(lines):
            elements.append(PageBreak())
    
    # Create the PDF
    doc.build(elements)

def main():
    # Get command-line arguments (excluding the script name)
    args = sys.argv[1:]

    # If no arguments provided, use letter size
    if not args:
        args = ['letter']

    # Process each argument
    for arg in args:
        arg = arg.lower()
        if arg in PAGE_SIZES:
            output_file = f"{os.path.splitext(FILE_OUTPUT)[0]}_{arg}.pdf"
            create_dynamic_table_pdf(output_file, "data.txt", arg)
            print(f"Generated {output_file} with font size {PAGE_SIZES[arg]['font_size']}")
        else:
            print(f"Unsupported page size: {arg}")

if __name__ == "__main__":
    main()