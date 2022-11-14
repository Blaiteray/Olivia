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
from functools import reduce
from customlib import sort_ord

class ReaderLayout(GridLayout):
    def __init__(self, chapter_folder, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.cols = 1
        self.toolbar_height = 45
        self.image_container = ImageContainer(chapter_folder, self.create_toolbar)
        self.add_widget(self.image_container)
    
    def create_toolbar(self):
        tool_bar_buttons = GridLayout(rows=1, cols=5,size_hint_y=None, height=self.toolbar_height)
        prev_button = Button(text='<<', size_hint=(0.3, None), height=self.toolbar_height)
        next_button = Button(text='>>', size_hint=(0.3, None), height=self.toolbar_height)
        close_button = Button(text='Close', size_hint=(0.08, None), height=self.toolbar_height)
        zoom_in_button = Button(text='+', size_hint=(0.16, None), height=self.toolbar_height, on_press=self.zoom_cb)
        zoom_out_button = Button(text='-', size_hint=(0.16, None), height=self.toolbar_height, on_press=self.zoom_cb)
        
        self.close_pos = 4 # Position of close button starting from right, where rightmost button has position 0.
        tool_bar_buttons.add_widget(close_button)
        tool_bar_buttons.add_widget(prev_button)
        tool_bar_buttons.add_widget(zoom_in_button)
        tool_bar_buttons.add_widget(zoom_out_button)
        tool_bar_buttons.add_widget(next_button)
        return tool_bar_buttons

    def zoom_cb(self, i):
        if i.text == '+':
            for item in self.image_container.display_items:
                item.width += 50
                item.height += 50/item.image_ratio
                self.image_container.inside_box.height += 50/item.image_ratio
        else:
            for item in self.image_container.display_items:
                item.width -= 50
                item.height -= 50/item.image_ratio
                self.image_container.inside_box.height -= 50/item.image_ratio

class ImageContainer(ScrollView):
    def __init__(self, chapter_folder, create_toolbar, **kwargs):
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
            item.width = 800
            item.height = item.width/item.image_ratio
            inside_box_height += item.height
        
        self.toolbar_up = create_toolbar()
        self.toolbar_down = create_toolbar()
        self.inside_box = BoxLayout(orientation='vertical',size_hint=(1,None), height=inside_box_height+self.toolbar_up.height+self.toolbar_down.height)
        self.add_widget(self.inside_box)

        self.inside_box.add_widget(self.toolbar_up)
        for item in self.display_items:
            self.inside_box.add_widget(item)
        self.inside_box.add_widget(self.toolbar_down)



class Temp(App):
    def build(self):
        return ReaderLayout(Path('downloads/AsuraScans/murim-login/Chapter 03'))
