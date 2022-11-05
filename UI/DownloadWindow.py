"""
Contains widet class to downlad content. Main widget class is DownloadWindowLayout 

"""


import importlib
from re import L
from turtle import right
import kivy
import os
kivy.require('2.1.0')
from kivy.app import App
from kivy.core.window import Window
Window.minimum_width, Window.minimum_height = (800, 600)
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from pathlib  import Path
from kivy.uix.spinner import Spinner


class DownloadWindowLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.upperPannel = UpperPannel()
        self.add_widget(self.upperPannel)
        self.lowerPannel = LowerPannel()
        self.add_widget(self.lowerPannel)


        self.upperPannel.url_input_confirmation.bind(on_press=lambda i:self.url_confirmation(self.upperPannel.url_input.text))

    def url_confirmation(self, selected_url):
        self.upperPannel.extension_confirmation(self.upperPannel.extension_option.text)
        if self.upperPannel.extension_selected:
            chapter_list = self.upperPannel.extension_module[0](selected_url)
            if chapter_list:
                self.lowerPannel.create_chapter_list_panel(chapter_list)
                self.lowerPannel.create_details_panel()
                self.lowerPannel.download_link = selected_url
                self.lowerPannel.image_downloader = self.upperPannel.extension_module[1]
            else:
                print('ERROR! INPUT A VALID URL')
        else:
            print('Select extesion first')
        print(selected_url)

class UpperPannel(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        input_box = GridLayout(cols=2, rows=2)
        
        self.size_hint_y = None
        self.height = 66
        self.extension_selected = False
        self.extension_path = Path('./extensions')
        self.extension_name = os.listdir(self.extension_path)
        self.extension_label = Label(text = 'Select a extension',size_hint_x=None, width=200)
        input_box.add_widget(self.extension_label)
        self.extension_option =  self.create_dropdown()
        input_box.add_widget(self.extension_option)
        # self.extension_add_confirmation = Button(text = 'Select',size_hint_x=None, width=160)
        # self.extension_add_confirmation.bind(on_press=lambda instance:self.extension_confirmation(self.extension_option.text))
        # input_box.add_widget(self.extension_add_confirmation)
        self.url_input_label = Label(text='Input URL of the manga',size_hint_x=None, width=200)
        input_box.add_widget(self.url_input_label)
        self.url_input = TextInput(multiline=False)
        input_box.add_widget(self.url_input)

        self.url_input_confirmation = Button(text='OK',size_hint_x=None, width=160)

        self.add_widget(input_box)
        self.add_widget(self.url_input_confirmation)
    
    def extension_confirmation(self,selected_option):
        
        if selected_option in self.extension_name:
            self.extension_selected = True
            self.extension_module = importlib.import_module('extensions'+'.'+selected_option).main()
        else:
            print('Please select an option')
    
    


    def create_dropdown(self):
        spinner = Spinner(
            # default value shown
            text='Home',
            # available values
            values=self.extension_name,
            # just for positioning in our exampl
            sync_height=True)

        

        spinner.bind(text=self.dropdown_callback)
        return spinner
    
    def dropdown_callback(self, spinner, text):
            print('The spinner', spinner, 'has text', text)

    

class LowerPannel(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.cols = 2
        self.download_link = ''
        self.selected_chapters = []
        self.image_downloader = None
        # self.create_chapter_list_panel([])
        
        
    def create_chapter_list_panel(self, chapter_list):
        if 'chapter_list_panel' in self.__dict__:
            pass
        else:
            self.chapter_list = chapter_list
            chapter_list_container = ScrollView(scroll_wheel_distance = 100)
            chapter_button_container = BoxLayout(orientation='vertical',size_hint_y=None, height=len(self.chapter_list)*33+33)
            instruction_label = Label(text='Select chapters to download', size_hint_y=None, height=33)
            chapter_button_container.add_widget(instruction_label)
            self.chapter_list_buttons = []
            for chapter in self.chapter_list:
                self.chapter_list_buttons.append(Button(text=chapter, size_hint_y=None, height=33))
                self.chapter_list_buttons[-1].bind(on_release=self.chapter_selction_callback)
                chapter_button_container.add_widget(self.chapter_list_buttons[-1])
            chapter_list_container.add_widget(chapter_button_container)
            self.chapter_list_panel = chapter_list_container
            self.add_widget(self.chapter_list_panel)
    
    def create_details_panel(self):
        if 'details_panel' in self.__dict__:
            if self.selected_chapters:
                self.first_chapter.text = str(min(self.selected_chapters))
                self.last_chapter.text = str(max(self.selected_chapters))
        else:
            right_panel = GridLayout(cols=1, rows=2)
            info_panel = Button(text='Info', size_hint_y=0.8)
            details_panel = GridLayout(cols=2, rows=3, size_hint_y=0.2)
            right_panel.add_widget(info_panel)
            right_panel.add_widget(details_panel)

            self.first_chapter = Label(text='Not Selected')
            self.last_chapter = Label(text='Not Selected')

            details_panel.add_widget(Label(text='First Chapter:'))
            details_panel.add_widget(self.first_chapter)
            details_panel.add_widget(Label(text='Last Chapter:'))
            details_panel.add_widget(self.last_chapter)

            reset_chapter_selected = Button(text='Reset')
            reset_chapter_selected.bind(on_press=self.rest_chpater_list)
            details_panel.add_widget(reset_chapter_selected)

            download_confirmation_button = Button(text='Download')
            download_confirmation_button.bind(on_press=self.download_confirmation)
            details_panel.add_widget(download_confirmation_button)

            self.details_panel = details_panel
            self.add_widget(right_panel)
        
    def chapter_selction_callback(self, instance):
        self.selected_chapters.append(getattr(instance, 'text'))
        self.create_details_panel()
        print(getattr(instance, 'text'))
    
    def download_confirmation(self, i):
        mangalink = self.download_link
        manga_title = mangalink[:-1].split('/')[-1] if mangalink[-1] == '/' else mangalink.split('/')[-1]

        start_chapter_name = min(self.selected_chapters)
        end_chapter_name = max(self.selected_chapters)
        
        chapters_to_download = []
        temp = False
        for i in self.chapter_list:
            if i == end_chapter_name:
                temp = True
            if temp:
                chapters_to_download.append(i)
            if i == start_chapter_name:
                break
        chapters_to_download.reverse()

        for chapter in chapters_to_download:
            self.image_downloader(manga_title,chapter, self.chapter_list[chapter])
        else:
            print('DONE')
    
    def rest_chpater_list(self, i):
        self.selected_chapters = []
        self.first_chapter.text = 'Not Selected'
        self.last_chapter.text = 'Not Selected'


#Delete this class after done desiging
class DownloadWindow(App):
    def build(self):
        return DownloadWindowLayout()
    

# if __name__ == '__main__':
#     DownloadWindow().run()
