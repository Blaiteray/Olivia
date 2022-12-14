import kivy
import os
kivy.require('2.1.0')
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from pathlib import Path
from math import ceil
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

from customlib import create_popup, sort_ord
from UI import Reader

class LibraryLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows=2
        self.cols=1
        self.menu_panel = BoxLayout(orientation='horizontal', size_hint_y=None, height= 33)
        self.folder_container = FolderContainer()
        self.add_widget(self.folder_container)
        self.add_widget(self.menu_panel)
        self.prev_button = Button(text='<<', size_hint=(0.5,None), height=33, on_press=self.folder_container.go_back)
        self.next_button = Button(text='>>', size_hint=(0.5,None), height=33, on_press=self.folder_container.go_next)
        self.menu_panel.add_widget(self.prev_button)
        self.menu_panel.add_widget(self.next_button)
    


class FolderContainer(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_path = Path('./downloads')
        self.extension_screen = Screen(name='extension_select', size_hint=(1,1))
        self.extension_folder = FolderView(self.download_path, False, self.extension_select_cb)
        self.extension_screen.add_widget(self.extension_folder)
        self.add_widget(self.extension_screen)

        self.manga_list_screen = Screen(name='manga_list')
        self.add_widget(self.manga_list_screen)

        self.chapter_list_screen = Screen(name='chapter_list')
        self.add_widget(self.chapter_list_screen)
        self.history_stack = [self.current]
        self.last_back = None


    def extension_select_cb(self, i):
        self.extension_path = self.download_path / i.text
        self.transition.direction = 'left'
        self.current = 'manga_list'
        self.current_enxtension = FolderView(self.extension_path, True, self.manga_select_cb, 1, 40, 10, 20)
        self.manga_list_screen.clear_widgets()
        self.manga_list_screen.add_widget(self.current_enxtension)
        self.history_stack.append(self.current)
        self.last_back = None
        print(self.extension_path)
    
    def manga_select_cb(self, i):
        self.manga_path = self.extension_path/ '-'.join(i.text.split(' ')).lower()
        self.transition.direction = 'left'
        self.current = 'chapter_list'
        self.currnet_manga_name = i.text
        self.current_manga = FolderView(self.manga_path, False, self.chapter_select_cb, 4, 40, 5, 20)
        self.chapter_list_screen.clear_widgets()
        self.chapter_list_screen.add_widget(self.current_manga)
        self.history_stack.append(self.current)
        self.last_back = None
        print(self.manga_path)
    
    def chapter_select_cb(self, i):
        self.current_chapter = i.text
        self.chapter_path = self.manga_path / i.text
        self.reader_content = Reader.ReaderLayout(self.chapter_path, 800)
        self.reader_popup = Popup(content=self.reader_content, auto_dismiss=False,title=f'{self.currnet_manga_name} [{i.text}]')
        self.reader_content.close_button.bind(on_press=self.reader_popup.dismiss)
        self.reader_content.next_button.bind(on_press=self.next_chapter_button_cb)
        self.reader_content.prev_button.bind(on_press=self.prev_chapter_button_cb)
        self.reader_popup.open()
    
    def next_chapter_button_cb(self, i):
        if self.current_chapter == self.current_manga.item_list[-1]:
            create_popup('No next chapter', 'MESSAGE')
        else:
            image_width = self.reader_content.image_width
            self.current_chapter = self.current_manga.item_list[self.current_manga.item_list.index(self.current_chapter)+1]
            self.chapter_path = self.manga_path / self.current_chapter
            self.reader_content = Reader.ReaderLayout(self.chapter_path, image_width)
            self.reader_popup.content = self.reader_content
            self.reader_popup.title=f'{self.currnet_manga_name} [{self.current_chapter}]'
            self.reader_content.close_button.bind(on_press=self.reader_popup.dismiss)
            self.reader_content.next_button.bind(on_press=self.next_chapter_button_cb)
            self.reader_content.prev_button.bind(on_press=self.prev_chapter_button_cb)
    
    def prev_chapter_button_cb(self, i):
        if self.current_chapter == self.current_manga.item_list[0]:
            create_popup('No previous chapter', 'MESSAGE')
        else:
            image_width = self.reader_content.image_width
            self.current_chapter = self.current_manga.item_list[self.current_manga.item_list.index(self.current_chapter)-1]
            self.chapter_path = self.manga_path / self.current_chapter
            self.reader_content = Reader.ReaderLayout(self.chapter_path, image_width)
            self.reader_popup.content = self.reader_content
            self.reader_popup.title=f'{self.currnet_manga_name} [{self.current_chapter}]'
            self.reader_content.close_button.bind(on_press=self.reader_popup.dismiss)
            self.reader_content.next_button.bind(on_press=self.next_chapter_button_cb)
            self.reader_content.prev_button.bind(on_press=self.prev_chapter_button_cb)
    
    def go_back(self, i):
        if len(self.history_stack) > 1:
            self.last_back = self.history_stack.pop()
            self.transition.direction = 'right'
            self.current = self.history_stack[-1]
    
    def go_next(self, i):
        if self.last_back:
            self.transition.direction = 'left'
            self.current = self.last_back
            self.history_stack.append(self.last_back)
            self.last_back = None
        


class FolderView(ScrollView):
    def __init__(self, path, simplify, extension_select_cb, folder_in_row=3, height_scale=150, spacing=10, padding=20):
        super().__init__()
        self.scroll_wheel_distance = 100
        self.item_list = []
        if path.exists():
            self.item_list = sorted(os.listdir(path), key=sort_ord)
            if simplify:
                self.item_list = list(map(lambda x: ' '.join(x.split('-')).title() ,self.item_list))
        else:
            create_popup('Please wait while downloading.', 'MESSAGE')

        folder_rows = ceil(len(self.item_list)/folder_in_row)
        self.boxlayout_inside = BoxLayout(orientation = 'vertical', size_hint_y = None, height = folder_rows*(height_scale+spacing)+2*padding)
        self.add_widget(self.boxlayout_inside)

        self.folder_container = GridLayout(rows=folder_rows, cols=folder_in_row, spacing=(spacing,spacing), padding=[padding]*4)
        self.boxlayout_inside.add_widget(self.folder_container)
        for i in self.item_list:
            self.folder_container.add_widget(Button(text=i, size_hint_y=None, height=height_scale, size_hint_x=1/folder_in_row, on_press=extension_select_cb))
        if len(self.item_list) < folder_in_row:
            self.folder_container.add_widget(Label(text='', size_hint_y=None, height=height_scale, size_hint_x=1/folder_in_row*(folder_in_row-len(self.item_list)%folder_in_row)))



class ChapterFolder:
    pass

