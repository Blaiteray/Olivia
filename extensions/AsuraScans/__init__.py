"""
WARNING!!!!! DO NOT RUN THIS FILE FROM THIS DIRECTORY DIRECTLY. USE LoadExtensions.py
"""

from pathlib import Path
from extensions.AsuraScans.loadchapterlist import  load_chapter
from extensions.AsuraScans.loadchapterimage import  load_image_url, download_images
import os

extension_name = 'AsuraScans'

"https://asura.gg/manga/reincarnation-of-the-strongest-sword-god/"

downloadPath = Path("./downloads") / extension_name
if not downloadPath.exists():
    os.makedirs(downloadPath)

print(f'SETUP EXTENSION ({extension_name}): OK')

def main():
    mangalink = input('Enter chapter link: ').strip()
    manga_title = mangalink[:-1].split('/')[-1] if mangalink[-1] == '/' else mangalink.split('/')[-1]

    chapter_list = load_chapter(mangalink)
    for i in chapter_list:
        print(i)

    start_chapter_name = input('Select starting chapter to download: ')
    while start_chapter_name not in chapter_list:
        print('Incalid chapter name')
        start_chapter_name = input('Select starting chapter to download: ')
    end_chapter_name = input('Select ending chapter to download: ')
    while end_chapter_name not in chapter_list:
        print('Incalid chapter name')
        end_chapter_name = input('Select ending chapter to download: ')

    chapters_to_download = []
    downloading_this = False
    for i in chapter_list:
        if i == end_chapter_name:
            downloading_this = True
        if downloading_this:
            chapters_to_download.append(i)
        if i == start_chapter_name:
            break
    chapters_to_download.reverse()

    for chapter in chapters_to_download:
        download_images(manga_title,chapter, load_image_url(chapter_list[chapter]))
    else:
        print('DONE')