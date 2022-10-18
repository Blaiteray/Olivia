# from pathlib import Path
# import os
# import importlib

# if not Path('./extensions').exists():
#         print('ERROR! EXTENSION FOLDER DOES NOT EXIST')
#         exit()

# def extension_loader(selected_extension):
#     extension_path = Path('./extensions')
#     extension_list = os.listdir(extension_path)
#     for extension in extension_list:
#         print(extension)
#     extension_module = importlib.import_module('extensions'+'.'+selected_extension)

#     return extension_module
    

from UI import DownloadWindow
DownloadWindow.DownloadWindow().run()