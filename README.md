El script en Python genera PDFs personalizados utilizando la biblioteca `FPDF`, y maneja imágenes y fuentes mediante `PIL` y una fuente específica, `Anton-Regular.ttf`. Aquí tienes un resumen del propósito del script y cómo usarlo en un archivo README.md.

### Archivo README.md

```markdown
# PDF Generator Script

Este script permite generar archivos PDF personalizados con texto e imágenes, utilizando la biblioteca FPDF para manejar las configuraciones de página y fuentes. El script está diseñado para incluir diferentes tamaños de página, colores de fuente y bordes, así como imágenes de fondo.

## Requisitos

- Python 3.x
- Paquetes requeridos:
  - fpdf
  - pillow

Para instalar las dependencias, puedes utilizar pip:
```bash
pip install fpdf pillow
```

## Uso

Este script toma texto de un archivo `texto.txt`, utiliza la fuente `Anton-Regular.ttf`, y puede generar PDFs con diferentes tamaños de página. El PDF generado tendrá un diseño personalizado con una imagen de fondo y opciones de espaciado y márgenes.

### Ejecución

Para ejecutar el script, simplemente usa:
```bash
python main.py
```

El archivo `texto.txt` debe estar en el mismo directorio que el script, y la fuente personalizada `Anton-Regular.ttf` debe estar en `~/.fonts/` o en una ruta especificada en el código.

### Argumentos

El script no recibe directamente argumentos desde la línea de comandos, pero se pueden modificar las variables globales dentro del código para personalizar el comportamiento:

- **CARD_TEXT_INPUT**: Ruta al archivo de texto a utilizar (por defecto: `texto.txt`).
- **CARD_FONT**: Ruta a la fuente TrueType Font (TTF) a utilizar (por defecto: `~/.fonts/Anton-Regular.ttf`).
- **CELLPADDING**: Espaciado dentro de la celda en milímetros (por defecto: `5`).
- **CELLSPACING**: Espaciado entre celdas y bordes en milímetros (por defecto: `5`).
- **BORDER_COLOR**: Color del borde en formato hexadecimal (por defecto: `#495057`).
- **FONT_COLOR**: Color de la tipografía en formato hexadecimal (por defecto: `#495057`).
- **PAGE_SIZES**: Tamaños de página disponibles. Los tamaños predefinidos son:
  - letter (216 x 279 mm)
  - legal (216 x 356 mm)
  - a4 (210 x 297 mm)
  - a3 (297 x 420 mm)
  - a2 (420 x 594 mm)
  - a1 (594 x 841 mm)
  - a0 (841 x 1189 mm)
  - ledger (279 x 432 mm)

### Ejemplo de Personalización

Si deseas cambiar el tamaño de la página o los colores, edita las siguientes variables en el código:
```python
PAGE_SIZES = {
    'letter': {'size': LETTER, 'font_size': 18},
    'legal': {'size': LEGAL, 'font_size': 18},
    'a4': {'size': A4, 'font_size': 24},
    ...
}
```

Para cambiar el color de la tipografía, edita:
```python
FONT_COLOR = "#000000"  # Por ejemplo, negro
```

### Funcionalidades Adicionales

- El script permite agregar imágenes como fondo del PDF (`cat_yoga.png` es un ejemplo incluido).
- Tiene soporte para diferentes tamaños de página y fuentes Unicode.

## Contacto

Para cualquier duda o mejora, puedes contactar al autor del script.

Ejemplo:
```
python3 main.py letter legal leger A0 A1 A2 A3 A4
```
