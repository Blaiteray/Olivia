"""
A manga downloading and reading tool
"""

import kivy
kivy.require('2.1.0')

from kivy.app import App 
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class MainLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.upperGrid = GridLayout(rows=1, cols=4, size_hint=(1, 0.04))
        self.upperGrid.add_widget(Button(text="Library"))
        self.upperGrid.add_widget(Button(text="History"))
        self.upperGrid.add_widget(Button(text="Extensions"))
        app_settings = Button(text="Settings")
        app_settings.bind(on_press=self.test_cb)
        self.upperGrid.add_widget(app_settings)

        self.add_widget(self.upperGrid)
        self.add_widget(Button(text='Lower Grid'))
    
    def test_cb(self, i):
        content = Button(text='Close me!')
        popup = Popup(content=content, auto_dismiss=False, size_hint=(.5, .5))

        # bind the on_press event of the button to the dismiss function
        content.bind(on_press=popup.dismiss)

        # open the popup
        popup.open()

class OlivApp(App):
    def build(self):
        return MainLayout()

OlivApp().run()