"""
load_image function takes the chapter url, returns all the image url in a list.
"""


from email.mime import image
import requests
import shutil
from bs4 import BeautifulSoup
from pathlib import Path
import os
import re

def load_image_url(chapterlink):
    req = requests.get(chapterlink)
    if req.status_code != requests.codes.ok:
        print('ERROR '+req.status_code)
        return
    
    soup = BeautifulSoup(req.content, "html.parser")
    found_obj = soup.find_all("img", { "class": "alignnone"})
    
    image_links = []
    for i in range(len(found_obj)):
        image_links.append(found_obj[i].get("src"))
    
    return image_links

def download_images(manga_name,chapter_name,image_links):
    chDownloadPath = Path("./downloads/AsuraScans/") / manga_name / chapter_name
    if not chDownloadPath.exists():
        os.makedirs(chDownloadPath)
    current_dir = Path.cwd()
    os.chdir(chDownloadPath)
    for page_no in range(len(image_links)):
        url = image_links[page_no]

        file_name = str(page_no) + re.compile(r".\w+?$").search(url).group()

        res = requests.get(url, stream = True)

        if res.status_code == requests.codes.ok:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
        else:
            print("ERROR "+res.status_code)
            os.chdir(current_dir)
            break
    else:
        os.chdir(current_dir)
        print(chapter_name+' DOWNLOAD STATUS: OK')


# download_images('the-dark-magician-transmigrates-after-66666-years','Chapter 56', 
#     load_image_url('https://asura.gg/the-dark-magician-transmigrates-after-66666-years-chapter-56/'))
