import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image

kivy.require('1.9.1')

class DisplayImage(App):
    layout = None
    num_keys = 0
    keys_displayed = []
    side_buffer = 0
    key_height = 0

    def set_num_keys(self, num_keys):
        self.num_keys = num_keys
        self.keys_displayed = [False] * num_keys
        self.side_buffer = Window.width * 0.01
        self.key_height = 0.4

    def set_layout(self):
        self.layout = FloatLayout()

    def add_keys_to_board(self, num_keys):
        self.set_layout()
        self.set_num_keys(num_keys)
        key_images = []
        horizontal_offset = 0

        for i in range(num_keys):
            if i % 12 == 0 or i % 12 == 5:
                key_images.append(Image(source="KeyImages/LeftSideSkinny.png"))
            if i % 12 == 1 or i % 12 == 3 or i % 12 == 6 or i % 12 == 8 or i % 12 == 10:
                key_images.append(Image(source="KeyImages/BlackKey.png"))
            if i % 12 == 2 or i % 12 == 7 or i % 12 == 9:
                key_images.append(Image(source="KeyImages/MiddleSkinny.png"))
            if i % 12 == 4 or i % 12 == 11:
                key_images.append(Image(source="KeyImages/RightSideSkinny.png"))
            self.insert_to_layout_leftmost(key_images[i], horizontal_offset=horizontal_offset)
            horizontal_offset += 50


    def insert_to_layout_leftmost(self, widget, horizontal_offset=0):
        widget.height = self.key_height
        widget.size_hint_y = self.key_height
        widget.size_hint_x = float(1)/self.num_keys
        widget.right += horizontal_offset
        self.layout.add_widget(widget)

    def build(self):
        return self.layout

    def fullscreen(self):
        Window.fullscreen = True

display = DisplayImage()
display.fullscreen()
display.add_keys_to_board(13)
'''
key1 = Image(source="KeyImages/LeftSideSkinny.png")
#key1.size_hint_x = 0.5
#key1.size_hint_y = 0.5

display.insert_to_layout_leftmost(key1)

key2 = Image(source="KeyImages/RightSideSkinny.png")
key2.pos = (100,0)
display.insert_to_layout_leftmost(key2)
'''



display.run()