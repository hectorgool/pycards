import os
import warnings
from fpdf import FPDF
from PIL import Image
from typing import List, Dict, Tuple
import json
from io import BytesIO
from concurrent.futures import ProcessPoolExecutor

def load_config(config_file: str) -> Dict:
    print("Loading configuration...")
    with open(config_file, 'r') as f:
        return json.load(f)

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def get_text_lines(file_path: str) -> List[str]:
    print(f"Reading text lines from {file_path}...")
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def preload_backgrounds(backgrounds: List[str]) -> Dict[str, BytesIO]:
    print("Preloading background images...")
    loaded_images = {}
    for bg in backgrounds:
        print(f"Loading background: {bg}")
        img = Image.open(bg).convert("RGBA")
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        loaded_images[bg] = img_byte_arr
    return loaded_images

def draw_bordered_cell_optimized(pdf: FPDF, x: float, y: float, w: float, h: float, text: str, background: BytesIO, config: Dict):
    print(f"Drawing cell at ({x}, {y}) with text: {text}")
    pdf.image(background, x=x, y=y, w=w, h=h)
    
    border_color = hex_to_rgb(config['BORDER_COLOR'])
    font_color = hex_to_rgb(config['FONT_COLOR'])
    
    pdf.set_draw_color(*border_color)
    pdf.set_text_color(*font_color)
    pdf.rect(x, y, w, h)
    
    text_width = w - 2 * config['CELLPADDING']
    text_height = h - 2 * config['CELLPADDING']
    line_spacing_factor = config.get('LINE_SPACING_FACTOR', 1.2)
    line_height = pdf.font_size * 0.3527 * line_spacing_factor
    
    pdf.set_xy(x + config['CELLPADDING'], y + config['CELLPADDING'])
    pdf.multi_cell(text_width, line_height, text, align=config.get('TEXT_ALIGN', 'C'))

def generate_pdf(args):
    config, page_type = args
    print(f"Generating PDF for {page_type}...")
    page_size = tuple(config['PAGE_SIZES'][page_type]['size'])
    font_size = config['PAGE_SIZES'][page_type]['font_size']
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
    preloaded_backgrounds = preload_backgrounds(backgrounds)
    
    for idx, line in enumerate(lines):
        if idx > 0 and idx % (config['COLS'] * config['ROWS']) == 0:
            print("Adding new page to PDF...")
            pdf.add_page()
        
        row = (idx % (config['COLS'] * config['ROWS'])) // config['COLS']
        col = (idx % (config['COLS'] * config['ROWS']) % config['COLS'])
        x = config['CELLSPACING'] + col * cell_width
        y = config['CELLSPACING'] + row * cell_height
        bg_image = preloaded_backgrounds[backgrounds[idx % len(backgrounds)]]
        
        draw_bordered_cell_optimized(pdf, x, y, cell_width, cell_height, line, bg_image, config)
    
    output_filename = f"{config['OUTPUT_NAME']}{page_type}.pdf"
    print(f"Saving PDF: {output_filename}")
    pdf.output(output_filename)

def parallel_generate_pdfs(config, page_types):
    print("Starting parallel PDF generation...")
    with ProcessPoolExecutor() as executor:
        executor.map(generate_pdf, [(config, page_type) for page_type in page_types])
    print("PDF generation completed!")
