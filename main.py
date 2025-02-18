import warnings
import os
import json
from pycards_module import parallel_generate_pdfs  # Se mantiene la importación correcta

# Obtener la ruta del directorio donde se encuentra este script
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")

# Función para cargar configuraciones desde un archivo JSON
def load_config(json_path):
    with open(json_path, 'r') as config_file:
        return json.load(config_file)

def main():
    try:
        config = load_config(config_path)

        if not config['SHOW_WARNINGS']:
            warnings.filterwarnings("ignore")

        execution_params = config.get('EXECUTION_PARAMS', ['letter'])
        font_path = os.path.expanduser(config['CARD_FONT'])
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        # Optimización: Paralelización con ProcessPoolExecutor
        parallel_generate_pdfs(config, execution_params)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please check that all required files (config.json, font file, etc.) exist and the paths are correct.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()