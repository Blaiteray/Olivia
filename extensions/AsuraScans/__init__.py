"""
WARNING!!!!! DO NOT RUN THIS FILE FROM THIS DIRECTORY DIRECTLY. USE LoadExtensions.py
"""

from pathlib import Path
from extensions.AsuraScans.loadchapter import  load_chapter_list
from extensions.AsuraScans.loadchapterimage import  download_images
import os

extension_name = 'AsuraScans'

"https://asura.gg/manga/reincarnation-of-the-strongest-sword-god/"

downloadPath = Path("./downloads") / extension_name
if not downloadPath.exists():
    os.makedirs(downloadPath)

print(f'SETUP EXTENSION ({extension_name}): OK')

def main():
    return (load_chapter_list, download_images)