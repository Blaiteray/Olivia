import kivy
import os
kivy.require('2.1.0')
from kivy.app import App
from kivy.core.window import Window
Window.minimum_width, Window.minimum_height = (800, 600)
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from pathlib  import Path
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

class LibraryLayout(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_distance = 100
        self.scrollable_panel = BoxLayout(orientation='vertical',size_hint_y=None, height=33*30)
        for i in range(30):
            self.scrollable_panel.add_widget(Button(text='Try Me '+str(i), size_hint_y=None, height=33))
        self.add_widget(self.scrollable_panel)








class Library(App):
    def build(self):
        return LibraryLayout()

if __name__ == '__main__':
    Library().run()