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
from math import ceil
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

class LibraryLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows=2
        self.cols=1
        self.menu_panel = BoxLayout(orientation='horizontal', size_hint_y=None, height= 33)
        self.prev_button = Button(text='<<', size_hint=(None,None), height=33,width=66)
        self.menu_panel.add_widget(self.prev_button)
        self.add_widget(self.menu_panel)
        self.folder_container = FolderContainer()
        self.add_widget(self.folder_container)


class FolderContainer(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_distance = 100

        self.extension_folder = ExtensionFolder()
        self.add_widget(self.extension_folder)
        


class ExtensionFolder(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.download_path = Path('./downloads')
        self.extension_list = os.listdir(self.download_path)
        height_scale = 150
        folder_in_row = 5
        folder_rows = ceil(len(self.extension_list)/folder_in_row)
        self.height = folder_rows*height_scale

        self.folder_container = GridLayout(rows=folder_rows, cols=folder_in_row, padding=[10,10,10,10], spacing=[10,10])
        self.add_widget(self.folder_container)
        for i in self.extension_list:
            self.folder_container.add_widget(Button(text=i, size_hint_y=None, height=height_scale, size_hint_x=1/folder_in_row, on_press=self.extension_select_cb))
        if len(self.extension_list) < folder_in_row:
            self.folder_container.add_widget(Label(text='', size_hint_y=None, height=height_scale, size_hint_x=1/folder_in_row*(folder_in_row-len(self.extension_list)%folder_in_row)))

    def extension_select_cb(self, i):
        self.extension_path = self.download_path / i.text
        print(self.extension_path)

class MangaFolder:
    pass


class ChapterFolder:
    pass








class Library(App):
    def build(self):
        return LibraryLayout()

if __name__ == '__main__':
    Library().run()