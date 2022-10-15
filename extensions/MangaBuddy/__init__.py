from distutils import extension
from pathlib import Path
import os

extension_name = 'MangaBuddy'

downloadPath = Path("./downloads") / extension_name
if not downloadPath.exists():
    os.makedirs(downloadPath)

print(f'SETUP EXTENSION ({extension_name})): OK')

def main():
    pass