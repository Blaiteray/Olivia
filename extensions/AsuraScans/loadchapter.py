"""
laod_chapter function takes a manhua link from asurascans, and returns a dictionary containing
chapter number: chapter url. latest chapter comes first.
"""


import requests
from bs4 import BeautifulSoup

def load_chapter_list(manhualink):
    try:
        req = requests.get(manhualink)
        if req.status_code != requests.codes.ok:
            print('ERROR '+str(req.status_code))
            return

        soup = BeautifulSoup(req.content, "html.parser")
        found_obj = soup.find_all("div", { "class": "eph-num"})
        chapter_details = dict()
        for i in range(len(found_obj)):
            chapter_details[found_obj[i].a.span.text] = found_obj[i].a.get("href")
        
        # print(chapter_details)

        return chapter_details
    except:
        print('ERROR! INVALID URL')


def load_chapter_details():
    pass
