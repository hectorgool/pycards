import os
import sys
import warnings
from fpdf import FPDF
from PIL import Image

# Global variables
CARD_TEXT_INPUT = "financial_empowerment.txt"  # Input file containing text for cards
CARD_FONT = os.path.expanduser("~/.fonts/Anton-Regular.ttf")  # Path to the font file
CELLPADDING = 5        # Space inside each cell in millimeters
CELLSPACING = 5        # Space between cells and borders in millimeters
BORDER_COLOR = "#495057"  # Border color in hexadecimal format
FONT_COLOR = "#495057"  # Font color in hexadecimal format
SHOW_WARNINGS = False  # Flag to control warning display
COLS = 3  # Number of columns in the grid
ROWS = 3  # Number of rows in the grid
OUTPUT_NAME = "card_" # Prefix for output PDF filename (e.g., "card_letter.pdf")

# Load background images
BACKGROUND_DIR = "png"  # Directory containing background images
backgrounds = ["mandala_morado.png"]  # List of background image filenames

# Ensure the full path to background images
backgrounds = [os.path.join(BACKGROUND_DIR, bg) for bg in backgrounds]

# Disable warnings if SHOW_WARNINGS is False
if not SHOW_WARNINGS:
    warnings.filterwarnings("ignore")

# Definition of page sizes in millimeters
LETTER = (216, 279)    # Letter (Width x Height)
LEGAL = (216, 356)     # Legal (Width x Height)
A4 = (210, 297)        # A4 (Width x Height)
A3 = (297, 420)        # A3 (Width x Height)
A2 = (420, 594)        # A2 (Width x Height)
A1 = (594, 841)        # A1 (Width x Height)
A0 = (841, 1189)       # A0 (Width x Height)
LEDGER = (279, 432)    # Ledger (Width x Height)

# Dictionary of page sizes and font sizes
PAGE_SIZES = {
    'letter': {'size': LETTER, 'font_size': 18},
    'legal': {'size': LEGAL, 'font_size': 18},
    'a4': {'size': A4, 'font_size': 24},
    'a3': {'size': A3, 'font_size': 34},
    'a2': {'size': A2, 'font_size': 44},
    'a1': {'size': A1, 'font_size': 54},
    'a0': {'size': A0, 'font_size': 64},
    'leger': {'size': LEDGER, 'font_size': 34}
}

class PDF(FPDF):
    def __init__(self, page_size, font_size):
        super().__init__(orientation='P', unit='mm', format=page_size)
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(CELLSPACING, CELLSPACING, CELLSPACING)
        self.add_page()

        # Register and configure the TTF font for Unicode support
        self.add_font('Anton', '', CARD_FONT, uni=True)
        self.set_font('Anton', '', font_size)

        # Set the font color
        r, g, b = self.hex_to_rgb(FONT_COLOR)
        self.set_text_color(r, g, b)

    def header(self):
        pass  # No header needed

    def footer(self):
        pass  # No footer needed

    def draw_bordered_cell(self, x, y, w, h, text, bg_image):
        # Convert hexadecimal color to RGB
        r, g, b = self.hex_to_rgb(BORDER_COLOR)
        
        # Set border color
        self.set_draw_color(r, g, b)
        
        # Draw cell background
        self.image(bg_image, x=x, y=y, w=w, h=h)
        
        # Draw cell border
        self.rect(x, y, w, h)
        
        # Adjust text position within the cell, vertically centered
        self.set_xy(x + CELLPADDING, y + CELLPADDING)
        
        # Get text dimensions
        text_width = w - 2 * CELLPADDING
        text_height = h - 2 * CELLPADDING
        
        # Calculate adjusted text height
        num_lines = self.get_num_lines(text, text_width)
        line_height = self.font_size_pt * 0.3527  # Convert pt to mm
        total_text_height = num_lines * line_height
        
        # Calculate offset to vertically center the text
        vertical_offset = (text_height - total_text_height) / 2
        
        # Place text in the cell, vertically centered
        self.set_xy(x + CELLPADDING, y + vertical_offset + CELLPADDING)
        self.multi_cell(text_width, line_height, text, border=0, align="C")
    
    def get_num_lines(self, text, width):
        """Returns the number of lines needed for the text within a given width."""
        lines = self.multi_cell(width, 10, text, border=0, align="C", split_only=True)
        return len(lines)

    def hex_to_rgb(self, hex_color):
        """Converts a hexadecimal color to RGB values."""
        return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))

def get_text_lines(file_path):
    """Read lines from the text file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def generate_pdf(page_type, page_size, font_size, custom_name=None):
    """Generate the PDF for a specific page size."""
    # Create PDF
    pdf = PDF(page_size, font_size)
    
    # Read text file
    lines = get_text_lines(CARD_TEXT_INPUT)
    
    # Define cell sizes
    cell_width = (page_size[0] - 2 * CELLSPACING) / COLS
    cell_height = (page_size[1] - 2 * CELLSPACING) / ROWS
    
    # Generate dynamic grid
    for idx, line in enumerate(lines):
        # Add a new page if we've filled one
        if idx > 0 and idx % (COLS * ROWS) == 0:
            pdf.add_page()

        # Position in the grid
        row = (idx % (COLS * ROWS)) // COLS
        col = (idx % (COLS * ROWS)) % COLS
        
        # X and Y coordinates for the cell
        x = CELLSPACING + col * cell_width
        y = CELLSPACING + row * cell_height
        
        # Alternate background images
        bg_image = backgrounds[idx % len(backgrounds)]
        
        # Add text and border to the cell
        pdf.draw_bordered_cell(x, y, cell_width, cell_height, line, bg_image)

    # Generate output filename
    output_filename = f"{OUTPUT_NAME}{page_type}.pdf" if not custom_name else f"{custom_name}_{page_type}.pdf"
    pdf.output(output_filename)

if __name__ == "__main__":
    # Get script arguments (e.g., letter, legal, a4, etc.)
    page_types = sys.argv[1:] if len(sys.argv) > 1 else ['letter']
    
    # Check if the last argument is not in PAGE_SIZES
    if page_types[-1] not in PAGE_SIZES:
        custom_name = page_types[-1]  # Use this argument as a custom prefix
        page_types = page_types[:-1]  # Remove the last argument so it's not treated as a page size
    else:
        custom_name = None
    
    # Generate a PDF for each specified page type
    for page_type in page_types:
        if page_type in PAGE_SIZES:
            page_size_info = PAGE_SIZES[page_type]
            generate_pdf(page_type, page_size_info['size'], page_size_info['font_size'], custom_name)
        else:
            print(f"The page type '{page_type}' is not valid. Please choose from: {', '.join(PAGE_SIZES.keys())}.")