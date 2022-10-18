"""
Contains widet class to downlad content. Main widget class is DownloadWindowLayout 

"""


import importlib
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


class UpperPannel(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 2
        self.size_hint_y = None
        self.height = 66
        self.extension_selected = False
        self.extension_path = Path('./extensions')
        self.extension_name = os.listdir(self.extension_path)
        self.extension_label = Label(text = 'Select a extension',size_hint_x=None, width=200)
        self.add_widget(self.extension_label)
        self.extension_option =  self.create_dropdown()
        self.add_widget(self.extension_option)
        self.extension_add_confirmation = Button(text = 'Select',size_hint_x=None, width=160)
        self.extension_add_confirmation.bind(on_press=lambda instance:self.extension_confirmation(self.extension_option.text))
        self.add_widget(self.extension_add_confirmation)
        self.url_input_label = Label(text='Input URL of the manga',size_hint_x=None, width=200)
        self.add_widget(self.url_input_label)
        self.url_input = TextInput(multiline=False)
        self.add_widget(self.url_input)
        self.url_input_confirmation = Button(text='OK',size_hint_x=None, width=160)
        self.url_input_confirmation.bind(on_press=lambda instance:self.url_confirmation(self.url_input.text))
        self.add_widget(self.url_input_confirmation)
    
    def extension_confirmation(self,selected_option):
        self.extension_selected = True
        print(selected_option)
        self.extension_module = importlib.import_module('extensions'+'.'+selected_option).main()
    
    def url_confirmation(self, selected_url):
        if self.extension_selected:
            pass
        else:
            print('Select extesion first')
        print(selected_url)


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
        self.chapter_list_panel = self.create_chapter_list_panel()
        self.add_widget(self.chapter_list_panel)
        self.details_panel = self.create_details_panel()
        self.add_widget(self.details_panel)
        
    def create_chapter_list_panel(self):
        self.chapter_list = ['Chapter '+str(i) for i in range(30)]
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
        return chapter_list_container
    
    def create_details_panel(self):
        details_panel = GridLayout(cols=1, rows=2)
        # manga_cover_image_location = str(Path('.'))
        # manga_cover = Image(src=manga_cover_image_location)
        # manga_cover.size_hint_y = 1.5
        # details_panel.add_widget(manga_cover)
        # manga_name_str = ''
        # manga_name = Label(text=manga_name_str)
        # details_panel.add_widget(manga_name)
        return details_panel
    
    def chapter_selction_callback(self, instance):
        print(getattr(instance, 'text'))


#Delete this class after done desiging
class DownloadWindow(App):
    def build(self):
        return DownloadWindowLayout()
    

# if __name__ == '__main__':
#     DownloadWindow().run()
