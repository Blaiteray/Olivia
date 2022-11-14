import kivy
import os
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from pathlib import Path
from customlib import sort_ord

class ReaderLayout(GridLayout):
    def __init__(self, chapter_folder, image_width, **kwargs):
        super().__init__(**kwargs)
        self.rows = 2
        self.cols = 1
        self.toolbar_height = 20
        self.image_width = image_width
    
        self.tool_bar_buttons = GridLayout(rows=1, cols=5,size_hint_y=None, height=self.toolbar_height)
        self.prev_button = Button(text='<<', size_hint=(0.3, None), height=self.toolbar_height)
        self.next_button = Button(text='>>', size_hint=(0.3, None), height=self.toolbar_height)
        self.close_button = Button(text='Close', size_hint=(0.08, None), height=self.toolbar_height)
        self.zoom_in_button = Button(text='+', size_hint=(0.16, None), height=self.toolbar_height, on_press=self.zoom_cb)
        self.zoom_out_button = Button(text='-', size_hint=(0.16, None), height=self.toolbar_height, on_press=self.zoom_cb)
        
        self.tool_bar_buttons.add_widget(self.close_button)
        self.tool_bar_buttons.add_widget(self.prev_button)
        self.tool_bar_buttons.add_widget(self.zoom_in_button)
        self.tool_bar_buttons.add_widget(self.zoom_out_button)
        self.tool_bar_buttons.add_widget(self.next_button)

        self.add_widget(self.tool_bar_buttons)

        self.image_container = ImageContainer(chapter_folder, self.image_width)
        self.add_widget(self.image_container)

    def zoom_cb(self, i):
        if i.text == '+':
            self.image_width += 50
            for item in self.image_container.display_items:
                item.width += 50
                item.height += 50/item.image_ratio
                self.image_container.inside_box.height += 50/item.image_ratio
        else:
            self.image_width -= 50
            for item in self.image_container.display_items:
                item.width -= 50
                item.height -= 50/item.image_ratio
                self.image_container.inside_box.height -= 50/item.image_ratio

class ImageContainer(ScrollView):
    def __init__(self, chapter_folder, image_width, **kwargs):
        super().__init__(**kwargs)
        self.scroll_wheel_distance = 100
        self.scroll_type = ['bars', 'content']
        self.bar_width = 15
        image_list = sorted(os.listdir(chapter_folder), key=sort_ord)
        self.display_items = list(map(lambda x: Image(source=str(chapter_folder/x)) ,image_list))
        inside_box_height = 0
        for item in self.display_items:
            item.allow_stretch = True
            item.size_hint = (1,None)
            item.width = image_width
            item.height = item.width/item.image_ratio
            inside_box_height += item.height
        
        self.inside_box = BoxLayout(orientation='vertical',size_hint=(1,None), height=inside_box_height)
        self.add_widget(self.inside_box)

        for item in self.display_items:
            self.inside_box.add_widget(item)



class Temp(App):
    def build(self):
        return ReaderLayout(Path('downloads/AsuraScans/murim-login/Chapter 03'), 800)
