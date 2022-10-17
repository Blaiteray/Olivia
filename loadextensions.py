from pathlib import Path
import os
import importlib

if not Path('./extensions').exists():
        print('ERROR! EXTENSION FOLDER DOES NOT EXIST')
        exit()

def extension_loader():
    extension_path = Path('./extensions')
    extension_list = os.listdir(extension_path)
    for extension in extension_list:
        print(extension)
    selected_extension = input('Selsect an extension: ').strip()
    while selected_extension not in extension_list:
        print('Invalid extension name.')
        selected_extension = input('Selsect an extension: ').strip()
    extension_module = importlib.import_module('extensions'+'.'+selected_extension)

    extension_module.main()
    


extension_loader()
