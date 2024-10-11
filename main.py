import warnings
import os
from pycards_module import load_config, generate_pdf

def main():
    try:
        config = load_config('config.json')

        if not config['SHOW_WARNINGS']:
            warnings.filterwarnings("ignore")

        execution_params = config.get('EXECUTION_PARAMS', ['letter'])
        project_name = config.get('PROJECT_NAME', None)
        
        font_path = os.path.expanduser(config['CARD_FONT'])
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        for page_type in execution_params:
            if page_type in config['PAGE_SIZES']:
                page_size_info = config['PAGE_SIZES'][page_type]
                generate_pdf(config, page_type, tuple(page_size_info['size']), page_size_info['font_size'], project_name)
            else:
                print(f"The page type '{page_type}' is not valid. Please choose from: {', '.join(config['PAGE_SIZES'].keys())}.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please check that all required files (config.json, font file, etc.) exist and the paths are correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()