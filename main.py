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
from kivy.uix.screenmanager import Screen, ScreenManager

from UI import DownloadWindow
from UI import Library


class MainLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.upperGrid = GridLayout(rows=1, cols=4, size_hint=(1, None), height=33)
        self.add_widget(self.upperGrid)

        library_open = Button(text="Library", size_hint_x=0.7)
        library_open.bind(on_press=self.library_open_cb)
        self.upperGrid.add_widget(library_open)

        download_open = Button(text="Download", size_hint_x=0.15)
        download_open.bind(on_press=self.download_open_cb)
        self.upperGrid.add_widget(download_open)

        app_settings = Button(text="Settings",size_hint_x=0.15)
        app_settings.bind(on_press=self.test_cb)
        self.upperGrid.add_widget(app_settings)

        self.lower_grid = ScreenManager()
        self.add_widget(self.lower_grid)

        self.library_panel = Library.LibraryLayout()
        self.library_screen = Screen(name='library')
        self.library_screen.add_widget(self.library_panel)
        self.lower_grid.add_widget(self.library_screen)

        self.download_panel = DownloadWindow.DownloadWindowLayout()
        self.download_screen = Screen(name='download')
        self.download_screen.add_widget(self.download_panel)
        self.lower_grid.add_widget(self.download_screen)
        
    def library_open_cb(self, i):
        self.lower_grid.transition.direction = 'right'
        self.lower_grid.current = 'library'

    def download_open_cb(self, i):
        self.lower_grid.transition.direction = 'left'
        self.lower_grid.current = 'download'

    def test_cb(self, i):
        content = Button(text='Close me!')
        popup = Popup(content=content, auto_dismiss=False, size_hint=(.5, .5))
        content.bind(on_press=popup.dismiss)
        popup.open()


class OlivApp(App):
    def build(self):
        return MainLayout()

OlivApp().run()