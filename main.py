import warnings
import os
from pycards_module import load_config, parallel_generate_pdfs  # Importación corregida

def main():
    try:
        config = load_config('config.json')

        if not config['SHOW_WARNINGS']:
            warnings.filterwarnings("ignore")

        execution_params = config.get('EXECUTION_PARAMS', ['letter'])
        font_path = os.path.expanduser(config['CARD_FONT'])
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        # Parallelize page type processing
        parallel_generate_pdfs(config, execution_params)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please check that all required files (config.json, font file, etc.) exist and the paths are correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
