import os
import warnings
from fpdf import FPDF
from PIL import Image
from typing import List, Dict, Tuple
import json

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

def apply_alpha(image_path: str, alpha: int) -> Image.Image:
    image = Image.open(image_path).convert("RGBA")
    alpha_channel = image.getchannel('A')
    alpha_channel = alpha_channel.point(lambda p: p * (alpha / 100))
    image.putalpha(alpha_channel)
    return image

def draw_bordered_cell(pdf: FPDF, x: float, y: float, w: float, h: float, text: str, background: str, config: Dict):
    image_with_alpha = apply_alpha(background, config['BACKGROUND_ALPHA'])
    temp_path = 'temp_with_alpha.png'
    image_with_alpha.save(temp_path, format='PNG')
    
    pdf.image(temp_path, x=x, y=y, w=w, h=h)
    os.remove(temp_path)
    
    border_color = hex_to_rgb(config['BORDER_COLOR'])
    font_color = hex_to_rgb(config['FONT_COLOR'])
    
    pdf.set_draw_color(*border_color)
    pdf.set_text_color(*font_color)
    pdf.rect(x, y, w, h)
    
    font_size = config.get('FONT_SIZE', 12)  # Tamaño de fuente predeterminado: 12 pt
    pdf.set_font_size(font_size)

    text_width = w - 2 * config['CELLPADDING']
    text_height = h - 2 * config['CELLPADDING']
    num_lines = get_num_lines(pdf, text, text_width)
    line_height = font_size * 0.3527
    total_text_height = num_lines * line_height
    vertical_offset = (text_height - total_text_height) / 2
    
    text_align = config.get('TEXT_ALIGN', 'C')  # "L", "C", or "R" for left, center, or right
    
    pdf.set_xy(x + config['CELLPADDING'], y + vertical_offset + config['CELLPADDING'])
    pdf.multi_cell(text_width, line_height, text, border=0, align=text_align)

def get_num_lines(pdf: FPDF, text: str, width: float) -> int:
    lines = pdf.multi_cell(width, 10, text, border=0, align="C", split_only=True)
    return len(lines)

def generate_pdf(config: Dict, page_type: str, page_size: Tuple[int, int], font_size: int, custom_name: str = None):
    pdf = FPDF(format=page_size)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Load the custom font from config
    font_path = os.path.expanduser(config['CARD_FONT'])
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")
    
    # Add the font to FPDF
    pdf.add_font('CustomFont', '', font_path, uni=True)
    pdf.set_font('CustomFont', size=font_size)  # Use the Unicode font

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

        draw_bordered_cell(pdf, x, y, cell_width, cell_height, line, bg_image, config)

    output_filename = f"{config['OUTPUT_NAME']}{page_type}.pdf" if not custom_name else f"{custom_name}_{page_type}.pdf"
    pdf.output(output_filename)
