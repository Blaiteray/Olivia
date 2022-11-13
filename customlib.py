import kivy
kivy.require('2.1.0')
from kivy.uix.button import Button
from kivy.uix.popup import Popup


def create_popup(msg, t='ERROR!'):
    content = Button(text=msg)
    popup = Popup(content=content, auto_dismiss=False, size_hint=(.4, .4),title=t)
    content.bind(on_press=popup.dismiss)
    popup.open()

def sort_ord(x):
            d1 = '0'
            digit_found = False
            for i in x:
                if '0' <= i <= '9' or i == '.':
                    digit_found = True
                    d1 += i
                elif digit_found:
                    break
            return float(d1)*10