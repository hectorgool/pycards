import os
import sys
import warnings
from fpdf import FPDF
from PIL import Image
from typing import List, Dict, Tuple

# Configuration constants
CARD_TEXT_INPUT = "financial_empowerment.txt"
CARD_FONT = os.path.expanduser("~/.fonts/Anton-Regular.ttf")
CELLPADDING = 5
CELLSPACING = 5
BORDER_COLOR = "#495057"
FONT_COLOR = "#495057"
SHOW_WARNINGS = False
COLS = 3
ROWS = 3
OUTPUT_NAME = "card_"
BACKGROUND_DIR = "png"

# Dictionary defining page sizes and corresponding font sizes
PAGE_SIZES: Dict[str, Dict[str, Tuple[int, int] | int]] = {
    'letter': {'size': (216, 279), 'font_size': 18},
    'legal': {'size': (216, 356), 'font_size': 18},
    'a4': {'size': (210, 297), 'font_size': 24},
    'a3': {'size': (297, 420), 'font_size': 34},
    'a2': {'size': (420, 594), 'font_size': 44},
    'a1': {'size': (594, 841), 'font_size': 54},
    'a0': {'size': (841, 1189), 'font_size': 64},
    'ledger': {'size': (279, 432), 'font_size': 34}
}

class ColorConverter:
    """Utility class for color conversion operations."""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Converts a hexadecimal color to RGB values."""
        return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))

class TextProcessor:
    """Handles text-related operations."""
    
    @staticmethod
    def get_text_lines(file_path: str) -> List[str]:
        """Reads lines from a text file and returns them as a list."""
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]

class BackgroundManager:
    """Manages background images for the cards."""
    
    def __init__(self, background_dir: str):
        """Initializes the BackgroundManager with a directory of background images."""
        self.backgrounds = [os.path.join(background_dir, bg) for bg in ["mandala_morado.png"]]

    def get_background(self, index: int) -> str:
        """Returns a background image path based on the given index."""
        return self.backgrounds[index % len(self.backgrounds)]

class CustomPDF(FPDF):
    """Custom PDF class extending FPDF with additional functionality."""
    
    def __init__(self, page_size: Tuple[int, int], font_size: int):
        """Initializes the CustomPDF with specified page size and font size."""
        super().__init__(orientation='P', unit='mm', format=page_size)
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(CELLSPACING, CELLSPACING, CELLSPACING)
        self.add_page()

        # Set up font and color
        self.add_font('Anton', '', CARD_FONT, uni=True)
        self.set_font('Anton', '', font_size)
        r, g, b = ColorConverter.hex_to_rgb(FONT_COLOR)
        self.set_text_color(r, g, b)

    def draw_bordered_cell(self, x: float, y: float, w: float, h: float, text: str, bg_image: str):
        """Draws a cell with a border, background image, and centered text."""
        # Set border color
        r, g, b = ColorConverter.hex_to_rgb(BORDER_COLOR)
        self.set_draw_color(r, g, b)
        
        # Add background image and draw border
        self.image(bg_image, x=x, y=y, w=w, h=h)
        self.rect(x, y, w, h)
        
        # Calculate text positioning
        text_width = w - 2 * CELLPADDING
        text_height = h - 2 * CELLPADDING
        num_lines = self.get_num_lines(text, text_width)
        line_height = self.font_size_pt * 0.3527
        total_text_height = num_lines * line_height
        vertical_offset = (text_height - total_text_height) / 2
        
        # Add centered text
        self.set_xy(x + CELLPADDING, y + vertical_offset + CELLPADDING)
        self.multi_cell(text_width, line_height, text, border=0, align="C")

    def get_num_lines(self, text: str, width: float) -> int:
        """Calculates the number of lines needed for the text within a given width."""
        lines = self.multi_cell(width, 10, text, border=0, align="C", split_only=True)
        return len(lines)

class PDFGenerator:
    """Handles the generation of PDF files with financial empowerment cards."""
    
    def __init__(self, background_manager: BackgroundManager):
        """Initializes the PDFGenerator with a BackgroundManager."""
        self.background_manager = background_manager

    def generate_pdf(self, page_type: str, page_size: Tuple[int, int], font_size: int, custom_name: str = None):
        """Generates a PDF file with financial empowerment cards for the specified page type."""
        pdf = CustomPDF(page_size, font_size)
        lines = TextProcessor.get_text_lines(CARD_TEXT_INPUT)
        
        # Calculate cell dimensions
        cell_width = (page_size[0] - 2 * CELLSPACING) / COLS
        cell_height = (page_size[1] - 2 * CELLSPACING) / ROWS
        
        # Generate cards
        for idx, line in enumerate(lines):
            if idx > 0 and idx % (COLS * ROWS) == 0:
                pdf.add_page()

            row = (idx % (COLS * ROWS)) // COLS
            col = (idx % (COLS * ROWS)) % COLS
            
            x = CELLSPACING + col * cell_width
            y = CELLSPACING + row * cell_height
            
            bg_image = self.background_manager.get_background(idx)
            
            pdf.draw_bordered_cell(x, y, cell_width, cell_height, line, bg_image)

        # Save the PDF file
        output_filename = f"{OUTPUT_NAME}{page_type}.pdf" if not custom_name else f"{custom_name}_{page_type}.pdf"
        pdf.output(output_filename)

def main():
    """Main function to handle command-line arguments and generate PDFs."""
    if not SHOW_WARNINGS:
        warnings.filterwarnings("ignore")

    # Parse command-line arguments
    page_types = sys.argv[1:] if len(sys.argv) > 1 else ['letter']
    
    # Check for custom name in arguments
    if page_types[-1] not in PAGE_SIZES:
        custom_name = page_types[-1]
        page_types = page_types[:-1]
    else:
        custom_name = None
    
    # Initialize BackgroundManager and PDFGenerator
    background_manager = BackgroundManager(BACKGROUND_DIR)
    pdf_generator = PDFGenerator(background_manager)

    # Generate PDFs for each specified page type
    for page_type in page_types:
        if page_type in PAGE_SIZES:
            page_size_info = PAGE_SIZES[page_type]
            pdf_generator.generate_pdf(page_type, page_size_info['size'], page_size_info['font_size'], custom_name)
        else:
            print(f"The page type '{page_type}' is not valid. Please choose from: {', '.join(PAGE_SIZES.keys())}.")

if __name__ == "__main__":
    main()