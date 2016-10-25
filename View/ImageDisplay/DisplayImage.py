import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

kivy.require('1.9.1')

class DisplayImage(App):
    def build(self):
        return Label(text='Test')
    def fullscreen(self):
        Window.fullscreen = True

display = DisplayImage()
display.fullscreen()
display.run()