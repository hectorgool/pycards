import os
import warnings
from fpdf import FPDF
from PIL import Image
from typing import List, Dict, Tuple
import json
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

def load_config(config_file: str) -> Dict:
    with open(config_file, 'r') as f:
        return json.load(f)

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def get_text_lines(file_path: str) -> List[str]:
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def get_background(backgrounds: List[str], index: int) -> str:
    return backgrounds[index % len(backgrounds)]

# Function for calculating the number of lines needed for text
def get_num_lines(pdf: FPDF, text: str, text_width: float) -> int:
    return len(pdf.multi_cell(text_width, pdf.font_size, text, split_only=True))

# Optimized draw_bordered_cell function with image and text properly positioned
def draw_bordered_cell_optimized(pdf: FPDF, x: float, y: float, w: float, h: float, text: str, background: str, config: Dict):
    # Load and place the background image
    image = Image.open(background).convert("RGBA")
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Position the image in the PDF
    pdf.image(img_byte_arr, x=x, y=y, w=w, h=h)
    
    # Draw the border and set colors
    border_color = hex_to_rgb(config['BORDER_COLOR'])
    font_color = hex_to_rgb(config['FONT_COLOR'])
    
    pdf.set_draw_color(*border_color)
    pdf.set_text_color(*font_color)
    pdf.rect(x, y, w, h)
    
    # Text rendering inside the cell
    text_width = w - 2 * config['CELLPADDING']
    text_height = h - 2 * config['CELLPADDING']
    line_spacing_factor = config.get('LINE_SPACING_FACTOR', 1.2)
    line_height = pdf.font_size * 0.3527 * line_spacing_factor
    num_lines = get_num_lines(pdf, text, text_width)
    total_text_height = num_lines * line_height
    vertical_offset = (text_height - total_text_height) / 2
    
    # Ensure text is centered vertically and horizontally within the cell
    pdf.set_xy(x + config['CELLPADDING'], y + config['CELLPADDING'] + vertical_offset)
    text_align = config.get('TEXT_ALIGN', 'C')
    
    pdf.multi_cell(text_width, line_height, text, align=text_align)

# Parallelizing the PDF generation using ThreadPoolExecutor for each page type
def parallel_generate_pdfs(config, page_types):
    with ThreadPoolExecutor() as executor:
        executor.map(lambda page_type: generate_pdf(config, page_type, tuple(config['PAGE_SIZES'][page_type]['size']), config['PAGE_SIZES'][page_type]['font_size']), page_types)

def generate_pdf(config: Dict, page_type: str, page_size: Tuple[int, int], font_size: int):
    pdf = FPDF(format=page_size)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_path = os.path.expanduser(config['CARD_FONT'])
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")
    
    pdf.add_font('CustomFont', '', font_path, uni=True)
    pdf.set_font('CustomFont', size=font_size)

    lines = get_text_lines(config['CARD_TEXT_INPUT'])

    cell_width = (page_size[0] - 2 * config['CELLSPACING']) / config['COLS']
    cell_height = (page_size[1] - 2 * config['CELLSPACING']) / config['ROWS']

    backgrounds = [os.path.join(config['BACKGROUND_DIR'], bg) for bg in config['BACKGROUNDS']]

    for idx, line in enumerate(lines):
        if idx > 0 and idx % (config['COLS'] * config['ROWS']) == 0:
            pdf.add_page()

        row = (idx % (config['COLS'] * config['ROWS'])) // config['COLS']
        col = (idx % (config['COLS'] * config['ROWS'])) % config['COLS']

        x = config['CELLSPACING'] + col * cell_width
        y = config['CELLSPACING'] + row * cell_height

        bg_image = get_background(backgrounds, idx)

        draw_bordered_cell_optimized(pdf, x, y, cell_width, cell_height, line, bg_image, config)

    output_filename = f"{config['OUTPUT_NAME']}{page_type}.pdf"
    pdf.output(output_filename)
