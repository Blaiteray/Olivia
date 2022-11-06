"""
A manga downloading and reading tool
"""

import kivy
kivy.require('2.1.0')

from kivy.app import App 
from kivy.core.window import Window
Window.minimum_width, Window.minimum_height = (800, 600)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from UI import DownloadWindow


class MainLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.upperGrid = GridLayout(rows=1, cols=4, size_hint=(1, 0.04))
        self.upperGrid.add_widget(Button(text="Library", size_hint_x=0.7))
        download_open = Button(text="Download", size_hint_x=0.15)
        download_open.bind(on_press=self.download_open_cb)
        self.upperGrid.add_widget(download_open)
        app_settings = Button(text="Settings",size_hint_x=0.15)
        app_settings.bind(on_press=self.test_cb)
        self.upperGrid.add_widget(app_settings)

        self.add_widget(self.upperGrid)
        self.add_widget(Button(text='Lower Grid'))
    
    def download_open_cb(self, i):
        content = DownloadWindow.DownloadWindowLayout()
        popup = Popup(content=content, auto_dismiss=True, size_hint=(0.96, 0.96), title='Download Window[Click outside to close]')
        popup.open()
        print('OK')

    def test_cb(self, i):
        content = Button(text='Close me!')
        popup = Popup(content=content, auto_dismiss=False, size_hint=(.5, .5))
        content.bind(on_press=popup.dismiss)
        popup.open()


class OlivApp(App):
    def build(self):
        return MainLayout()

OlivApp().run()