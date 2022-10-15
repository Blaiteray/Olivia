"""
A manga downloading and reading tool
"""


from tkinter import Grid
from turtle import width
import kivy
kivy.require('2.1.0')

from kivy.app import App 
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image


class ImagePanel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.readerWindow = ReaderWindow()
        self.add_widget(self.readerWindow)

    def on_scroll_stop(self, touch, check_children=True):
        if self.scroll_y <0 and hasattr(self,'readerWindow') and hasattr(self.readerWindow, 'change_img'):
            self.readerWindow.change_img()
            self.readerWindow.height += self.readerWindow.current_img[-1].height
            # self.scroll_y += self.readerWindow.current_img[-1].height
        return super().on_scroll_stop(touch, check_children)

class ReaderWindow(BoxLayout):
    def change_img(self):
        self.add_image("10.jpg")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.current_img = []
        self.size_hint = (1, None)
        self.add_image("2.jpg")
    
    def add_image(self, loc):
        img1 = Image(source=loc)
        img1.allow_stretch = True
        img1.height = Window.width/img1.image_ratio
        img1.reload()
        self.add_widget(img1)
        self.height = img1.height
        self.current_img.append(img1)
class OlivApp(App):
    pass

OlivApp().run()