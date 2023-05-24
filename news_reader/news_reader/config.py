import toml
import os

config_data = None

def load_toml_data():
    global config_data
    current_dir = os.getcwd()
    toml_file_path = os.path.join(current_dir, 'news_reader', 'config.toml') 
    if config_data is None:
        with open(toml_file_path, 'r') as file:
            config_data = toml.load(file)

load_toml_data()