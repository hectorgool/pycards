import os
from fpdf import FPDF
from PIL import Image
import warnings

# Variables globales
CARD_TEXT_OUTPUT = "output.pdf"
CARD_TEXT_INPUT = "texto.txt"
CARD_FONT = os.path.expanduser("~/.fonts/Anton-Regular.ttf")
DOCUMENT_HEIGHT = 297  # Altura en milímetros (A4)
DOCUMENT_WIDTH = 210   # Ancho en milímetros (A4)
CELLPADDING = 5        # Espacio dentro de la celda en milímetros
CELLSPACING = 5        # Espacio entre celdas y bordes en milímetros
BORDER_COLOR = "#000000"  # Color negro en formato hexadecimal
SHOW_WARNINGS = False

# Deshabilitar warnings si SHOW_WARNINGS es False
if not SHOW_WARNINGS:
    warnings.filterwarnings("ignore")

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(CELLSPACING, CELLSPACING, CELLSPACING)
        self.add_page()
        
        # Registrar y configurar la fuente TTF para soporte Unicode
        self.add_font('Anton', '', CARD_FONT, uni=True)
        self.set_font('Anton', '', 12)

    def header(self):
        pass  # No necesitamos encabezado

    def footer(self):
        pass  # No necesitamos pie de página

    def draw_bordered_cell(self, x, y, w, h, text, bg_image):
        # Convertir el color hexadecimal a RGB
        r, g, b = tuple(int(BORDER_COLOR[i:i + 2], 16) for i in (1, 3, 5))
        
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

def get_text_lines(file_path):
    """Leer las líneas del archivo de texto."""
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def generate_pdf():
    # Crear el PDF
    pdf = PDF()
    
    # Cargar imágenes de fondo
    backgrounds = ["fondo1.png", "fondo2.png", "fondo3.png"]
    
    # Leer el archivo de texto
    lines = get_text_lines(CARD_TEXT_INPUT)
    
    # Definir tamaños de celdas
    cell_width = (DOCUMENT_WIDTH - 2 * CELLSPACING) / 3
    cell_height = (DOCUMENT_HEIGHT - 2 * CELLSPACING) / 3
    
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

    # Guardar el PDF
    pdf.output(CARD_TEXT_OUTPUT)

if __name__ == "__main__":
    generate_pdf()
