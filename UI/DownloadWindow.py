"""
Contains widet class to downlad content. Main widget class is DownloadWindowLayout 

"""


from threading import Thread
import importlib
import kivy
import os
kivy.require('2.1.0')
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from pathlib  import Path
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

from customlib import create_popup, sort_ord




class DownloadWindowLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.padding = [10]*4
        self.spacing = (10,10)
        self.upperPannel = UpperPannel()
        self.add_widget(self.upperPannel)
        self.lowerPannel = LowerPannel()
        self.add_widget(self.lowerPannel)


        self.upperPannel.url_input_confirmation.bind(on_press=lambda i:self.url_confirmation(self.upperPannel.url_input.text))

    def url_confirmation(self, selected_url):
        self.upperPannel.extension_confirmation(self.upperPannel.extension_option.text)
        if not selected_url and self.upperPannel.extension_selected:
                create_popup('Enter an URL')
        elif self.upperPannel.extension_selected:
            chapter_list = self.upperPannel.extension_module[0](selected_url)
            if isinstance(chapter_list, dict):
                self.lowerPannel.create_chapter_list_panel(chapter_list)
                self.lowerPannel.download_link = selected_url
                self.lowerPannel.image_downloader = self.upperPannel.extension_module[1]
            else:
                create_popup('Connection Error!')
                print('ERROR! INPUT A VALID URL')
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
            create_popup('Select an Extension first.')
            print('Please select an option')
    
    


    def create_dropdown(self):
        spinner = Spinner(
            text='Select an Extension',
            values=self.extension_name,
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
        self.spacing = (5,10)
        self.download_link = ''
        self.selected_chapters = []
        self.image_downloader = None
        # self.create_chapter_list_panel([])
        
        
    def create_chapter_list_panel(self, chapter_list):
        if 'chapter_list_panel' in self.__dict__:
            self.remove_widget(self.chapter_list_panel)
            self.remove_widget(self.details_panel)
            self.selected_chapters = []
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
        self.create_details_panel()
        self.chapter_selction_callback(None)
    
    def create_details_panel(self):
        if 'details_panel' in self.__dict__:
            self.remove_widget(self.details_panel)
        right_panel = GridLayout(cols=1, rows=2)
        info_panel = Button(text='Info', size_hint_y=0.7)
        details_panel = GridLayout(cols=2, rows=5, size_hint_y=0.3)
        right_panel.add_widget(info_panel)
        right_panel.add_widget(details_panel)

        self.first_chapter = Label(text='Not Selected')
        self.last_chapter = Label(text='Not Selected')
        self.status = Label(text='Selecting...')
        self.downloading = Label(text='Not Started Yet')

        details_panel.add_widget(Label(text='First Chapter:'))
        details_panel.add_widget(self.first_chapter)
        details_panel.add_widget(Label(text='Last Chapter:'))
        details_panel.add_widget(self.last_chapter)
        details_panel.add_widget(Label(text='Status: '))
        details_panel.add_widget(self.status)
        details_panel.add_widget(Label(text='Downloading Now: '))
        details_panel.add_widget(self.downloading)

        reset_chapter_selected = Button(text='Reset')
        reset_chapter_selected.bind(on_press=self.reset_chapter_list)
        details_panel.add_widget(reset_chapter_selected)

        download_confirmation_button = Button(text='Download')
        download_confirmation_button.bind(on_press=self.download_confirmation)
        details_panel.add_widget(download_confirmation_button)

        self.details_panel = right_panel
        self.add_widget(self.details_panel)
        
    def chapter_selction_callback(self, instance):
        if instance:
            self.selected_chapters.append(getattr(instance, 'text'))
        if self.selected_chapters:
            self.first_chapter.text = str(min(self.selected_chapters, key=sort_ord))
            self.last_chapter.text = str(max(self.selected_chapters, key=sort_ord))
    
    def download_confirmation(self, ix):
        if self.selected_chapters:
            mangalink = self.download_link
            manga_title = mangalink[:-1].split('/')[-1] if mangalink[-1] == '/' else mangalink.split('/')[-1]

            start_chapter_name = min(self.selected_chapters, key=sort_ord)
            end_chapter_name = max(self.selected_chapters, key=sort_ord)
            
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

            self.download_concluded = False
            self.current_chapter = ''
            
            create_popup('Download Started', 'MESSAGE')

            dw_thread = Thread(target=self.downloading_thread, args=(chapters_to_download, manga_title))
            dw_thread.daemon = True
            dw_thread.start()

            
            
        else:
            create_popup('Select a chapter to download')
            print('Select a chapter to download')
    
    def downloading_thread(self, chapters_to_download, manga_title):
        self.status.text = 'Downloading...'
        for chapter in chapters_to_download:
            self.downloading.text = str(chapter)
            msg = self.image_downloader(manga_title,chapter, self.chapter_list[chapter])
            if msg != 'OK':
                self.status.text = 'Download Error'
                self.downloading.text += '[ERROR]'
                break
        else:
            self.status.text = 'Completed'
            print('DONE')
    
    def reset_chapter_list(self, i):
        self.selected_chapters = []
        self.first_chapter.text = 'Not Selected'
        self.last_chapter.text = 'Not Selected'

