import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
import time

kivy.require('1.9.1')

class DisplayImage(App):
    layout = None
    num_keys = 0
    keys_displayed = []
    keys_displayed_copy = []
    side_buffer = 0
    key_height = 0

    def set_num_keys(self, num_keys):
        self.num_keys = num_keys
        self.keys_displayed = [False] * num_keys
        self.side_buffer = Window.width * 0.01
        self.key_height = 0.4

    def set_layout(self):
        self.layout = FloatLayout()
        backgroundColor = Button(Color=(0.7 , 0, 0))
        backgroundColor.disabled = True
        self.layout.add_widget(backgroundColor)

    def add_keys_to_board(self, num_keys):
        self.set_layout()
        self.set_num_keys(num_keys)
        key_widgets = []
        horizontal_offset = 0

        for i in range(num_keys):
            if i % 12 == 0 or i % 12 == 5:
                key_widgets.append(Image(source="KeyImages/LeftSideSkinny.png"))
            if i % 12 == 1 or i % 12 == 3 or i % 12 == 6 or i % 12 == 8 or i % 12 == 10:
                key_widgets.append(Image(source="KeyImages/BlackKey.png"))
            if i % 12 == 2 or i % 12 == 7 or i % 12 == 9:
                key_widgets.append(Image(source="KeyImages/MiddleSkinny.png"))
            if i % 12 == 4 or i % 12 == 11:
                key_widgets.append(Image(source="KeyImages/RightSideSkinny.png"))
            self.keys_displayed[i] = True
            self.insert_to_layout_leftmost(key_widgets[i], horizontal_offset=horizontal_offset)
            horizontal_offset += key_widgets[i].width
        self.key_widgets = key_widgets

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

    def toggleKeyDisplay(self, buttonNum):
        if buttonNum < self.num_keys:
            if self.keys_displayed[buttonNum] is True:
                self.keys_displayed[buttonNum] = False
                self.key_widgets[buttonNum].x -= 10000
            elif self.keys_displayed[buttonNum] is False:
                self.keys_displayed[buttonNum] = True
                self.key_widgets[buttonNum].x += 10000

display = DisplayImage()
display.fullscreen()
display.add_keys_to_board(8)
print display.key_widgets[2].right
display.toggleKeyDisplay(2)
print display.key_widgets[2].right

display.run()
display.toggleKeyDisplay(2)

print display.key_widgets[2].right