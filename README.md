
# Card Generator PDF Project

This project is a customizable PDF generator that creates cards with text input and background images, laid out in a grid format. The project allows users to configure various settings such as font, page size, grid layout, and more through a `config.json` file.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/card-generator.git
   cd card-generator
   ```

2. **Install required dependencies:**
   This project requires Python 3.x and some external libraries. Install the dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install additional fonts (if needed):**
   The project relies on custom fonts specified in the `config.json`. Make sure you have the required `.ttf` or `.otf` fonts installed, or provide a path to the font file in the configuration.

## Configuration

The project uses a `config.json` file for configuring the card generation. Below is an example of the configuration options:

```json
{
    "CARD_TEXT_INPUT": "wealth.txt",
    "CARD_FONT": "~/.fonts/Kalam-Regular.ttf",
    "CELLPADDING": 5,
    "CELLSPACING": 5,
    "BORDER_COLOR": "#495057",
    "FONT_COLOR": "#495057",
    "SHOW_WARNINGS": false,
    "COLS": 3,
    "ROWS": 3,
    "OUTPUT_NAME": "card_",
    "BACKGROUND_DIR": "png",
    "BACKGROUND_ALPHA": 40,
    "BACKGROUNDS": ["angel.png"],
    "PAGE_SIZES": {
        "letter": {"size": [216, 279], "font_size": 18},
        "a4": {"size": [210, 297], "font_size": 24}
    },
    "EXECUTION_PARAMS": ["letter", "a4"]
}
```

### Key Configuration Options:
- `CARD_TEXT_INPUT`: Path to the text file containing the text for the cards.
- `CARD_FONT`: Path to the custom font to be used. Must be a Unicode-compatible font (`.ttf` or `.otf`).
- `CELLPADDING` and `CELLSPACING`: Padding and spacing for the grid layout.
- `BORDER_COLOR` and `FONT_COLOR`: Colors for the card border and text.
- `OUTPUT_NAME`: The prefix for the output PDF file.
- `BACKGROUND_DIR`: Directory containing the background images.
- `BACKGROUNDS`: List of background image filenames.
- `PAGE_SIZES`: Predefined page sizes and associated font sizes.

## Usage

1. **Prepare your text and images:**
   - The text file (`wealth.txt` in the config) should contain the lines to be printed on the cards.
   - Place your background images in the directory specified in the configuration.

2. **Run the generator:**
   To generate the PDFs, simply run the main script:
   ```bash
   python3 main.py
   ```

3. **Output:**
   The generated PDFs will be saved in the same directory as the script, with filenames prefixed by the value of `OUTPUT_NAME` followed by the page size (e.g., `card_letter.pdf`).

## File Structure

- `main.py`: The main entry point of the project.
- `pycards_module.py`: Contains helper functions for loading configuration, generating the PDF, and rendering the text.
- `config.json`: Configuration file where you define the settings for the PDF generation.
- `wealth.txt`: Example input text file.
- `png/`: Directory containing background images for the cards.

## Contributing

Contributions are welcome! Please follow the standard Git workflow:
1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

