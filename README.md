# Financial Empowerment Card Generator

This script generates PDF files containing financial empowerment cards with customizable page sizes and layouts.

## Features

- Supports multiple page sizes (letter, legal, A4, A3, A2, A1, A0, ledger)
- Customizable grid layout (3x3 by default)
- Background images for each card
- Unicode support for text
- Custom font support

## Requirements

- Python 3.6+
- fpdf library
- Pillow library

## Installation

1. Clone this repository
2. Install the required libraries:

```bash
pip install fpdf Pillow
```

3. Ensure you have the Anton-Regular.ttf font file in your `~/.fonts/` directory

## Usage

Run the script from the command line, specifying the desired page size(s):

```bash
python main.py [page_size1] [page_size2] ... [custom_name]
```

Available page sizes: letter, legal, a4, a3, a2, a1, a0, ledger

If a custom name is provided as the last argument, it will be used as a prefix for the output file names.

## Configuration

You can modify the following constants in the script to customize the output:

- `CARD_TEXT_INPUT`: Input file containing text for cards
- `CARD_FONT`: Path to the font file
- `CELLPADDING`: Space inside each cell in millimeters
- `CELLSPACING`: Space between cells and borders in millimeters
- `BORDER_COLOR`: Border color in hexadecimal format
- `FONT_COLOR`: Font color in hexadecimal format
- `COLS`: Number of columns in the grid
- `ROWS`: Number of rows in the grid
- `OUTPUT_NAME`: Prefix for output PDF filename

## Examples

1. Generate a letter-sized PDF:
```bash
python main.py letter
```
Result: `card_letter.pdf`

2. Generate multiple PDFs with different sizes:
```bash
python main.py letter a4 legal
```
Result: `card_letter.pdf`, `card_a4.pdf`, `card_legal.pdf`

3. Generate PDFs with a custom name prefix:
```bash
python main.py letter a4 custom_project
```
Result: `custom_project_letter.pdf`, `custom_project_a4.pdf`

## Contributing

Feel free to submit issues or pull requests if you have any improvements or bug fixes.

## License

This project is open-source and available under the MIT License.