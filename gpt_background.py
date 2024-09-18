import os
import sys
import warnings
from fpdf import FPDF
from PIL import Image

# Variables globales
FILE_OUTPUT = "affirmations"
CARD_TEXT_INPUT = "texto.txt"
CARD_FONT = os.path.expanduser("~/.fonts/Anton-Regular.ttf")
CELLPADDING = 5        # Espacio dentro de la celda en milímetros
CELLSPACING = 5        # Espacio entre celdas y bordes en milímetros
BORDER_COLOR = "#495057"  # Color negro en formato hexadecimal
FONT_COLOR = "#495057"  # Color de la tipografía en formato hexadecimal
SHOW_WARNINGS = False

# Deshabilitar warnings si SHOW_WARNINGS es False
if not SHOW_WARNINGS:
    warnings.filterwarnings("ignore")

# Definición de tamaños de página en milímetros
LETTER = (216, 279)    # Letter (Ancho x Alto)
LEGAL = (216, 356)     # Legal (Ancho x Alto)
A4 = (210, 297)        # A4 (Ancho x Alto)
A3 = (297, 420)        # A3 (Ancho x Alto)
A2 = (420, 594)        # A2 (Ancho x Alto)
A1 = (594, 841)        # A1 (Ancho x Alto)
A0 = (841, 1189)       # A0 (Ancho x Alto)
LEDGER = (279, 432)    # Ledger (Ancho x Alto)

# Lista de tamaños de página y tamaños de fuente
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

        # Registrar y configurar la fuente TTF para soporte Unicode
        self.add_font('Anton', '', CARD_FONT, uni=True)
        self.set_font('Anton', '', font_size)

        # Configurar el color de la fuente (tomado de la variable FONT_COLOR)
        r, g, b = self.hex_to_rgb(FONT_COLOR)
        self.set_text_color(r, g, b)

    def header(self):
        pass  # No necesitamos encabezado

    def footer(self):
        pass  # No necesitamos pie de página

    def draw_bordered_cell(self, x, y, w, h, text, bg_image):
        # Convertir el color hexadecimal a RGB
        r, g, b = self.hex_to_rgb(BORDER_COLOR)
        
        # Establecer el color del borde
        self.set_draw_color(r, g, b)
        
        # Dibujar el fondo de la celda
        self.image(bg_image, x=x, y=y, w=w, h=h)
        
        # Dibujar el borde de la celda
        self.rect(x, y, w, h)
        
        # Ajustar el texto dentro de la celda, centrado verticalmente
        self.set_xy(x + CELLPADDING, y + CELLPADDING)
        
        # Obtener la altura del texto
        text_width = w - 2 * CELLPADDING
        text_height = h - 2 * CELLPADDING
        
        # Calcular la altura del texto ajustado
        num_lines = self.get_num_lines(text, text_width)
        line_height = self.font_size_pt * 0.3527  # Convertir pt a mm
        total_text_height = num_lines * line_height
        
        # Calcular el desplazamiento para centrar el texto verticalmente
        vertical_offset = (text_height - total_text_height) / 2
        
        # Colocar el texto en la celda, centrado verticalmente
        self.set_xy(x + CELLPADDING, y + vertical_offset + CELLPADDING)
        self.multi_cell(text_width, line_height, text, border=0, align="C")
    
    def get_num_lines(self, text, width):
        """Retorna el número de líneas necesarias para el texto dentro de un ancho dado."""
        lines = self.multi_cell(width, 10, text, border=0, align="C", split_only=True)
        return len(lines)

    def hex_to_rgb(self, hex_color):
        """Convierte un color hexadecimal a valores RGB."""
        return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))

def get_text_lines(file_path):
    """Leer las líneas del archivo de texto."""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def generate_pdf(page_type, page_size, font_size):
    """Generar el PDF para un tamaño de página específico."""
    # Crear el PDF
    pdf = PDF(page_size, font_size)
    
    # Cargar imágenes de fondo
    backgrounds = ["fondo1.png", "fondo2.png", "fondo3.png"]
    
    # Leer el archivo de texto
    lines = get_text_lines(CARD_TEXT_INPUT)
    
    # Definir tamaños de celdas
    cell_width = (page_size[0] - 2 * CELLSPACING) / 3
    cell_height = (page_size[1] - 2 * CELLSPACING) / 3
    
    # Generar tabla dinámica
    for idx, line in enumerate(lines):
        # Añadir una nueva página si ya hemos llenado una
        if idx > 0 and idx % 9 == 0:
            pdf.add_page()

        # Posición en la grilla
        row = (idx % 9) // 3
        col = (idx % 9) % 3
        
        # Coordenadas X y Y para la celda
        x = CELLSPACING + col * cell_width
        y = CELLSPACING + row * cell_height
        
        # Alternar imágenes de fondo
        bg_image = backgrounds[idx % len(backgrounds)]
        
        # Agregar texto y borde en la celda
        pdf.draw_bordered_cell(x, y, cell_width, cell_height, line, bg_image)

    # Guardar el PDF con el sufijo adecuado
    output_filename = f"{FILE_OUTPUT}_{page_type}.pdf"
    pdf.output(output_filename)

if __name__ == "__main__":
    # Obtener los argumentos del script (por ejemplo, letter, legal, a4, etc.)
    page_types = sys.argv[1:] if len(sys.argv) > 1 else ['letter']
    
    # Generar un PDF para cada tipo de página especificado
    for page_type in page_types:
        if page_type in PAGE_SIZES:
            page_size_info = PAGE_SIZES[page_type]
            generate_pdf(page_type, page_size_info['size'], page_size_info['font_size'])
        else:
            print(f"El tipo de página '{page_type}' no es válido. Por favor elige entre: {', '.join(PAGE_SIZES.keys())}.")
