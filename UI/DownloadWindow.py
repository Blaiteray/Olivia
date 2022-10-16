from turtle import width
import kivy
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
        self.extension_label = Label(text = 'Select a extension',size_hint_x=None, width=200)
        self.add_widget(self.extension_label)
        self.extension_option =  self.create_dropdown()
        self.add_widget(self.extension_option)
        self.extension_add_confirmation = Button(text = 'Select',size_hint_x=None, width=160)
        self.add_widget(self.extension_add_confirmation)
        self.url_input_label = Label(text='Input URL of the manga',size_hint_x=None, width=200)
        self.add_widget(self.url_input_label)
        self.url_input = TextInput(multiline=False)
        self.add_widget(self.url_input)
        self.url_input_confirmation = Button(text='OK',size_hint_x=None, width=160)
        self.add_widget(self.url_input_confirmation)

    def create_dropdown(self):
        dropdown = DropDown()
        for index in range(10):
            btn = Button(text='Value %d' % index, size_hint_y=None, height=33)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        mainbutton = Button(text='Select Extension')
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        return mainbutton
    

class LowerPannel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_wheel_distance = 100














class DownloadWindow(App):
    def build(self):
        return DownloadWindowLayout()
    

if __name__ == '__main__':
    DownloadWindow().run()


