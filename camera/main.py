import sys
import os
from os.path import join
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time

# Uncomment these lines to see all the messages
from kivy.logger import Logger
import logging
Logger.setLevel(logging.TRACE)

print(f"* * * * * * * * PYTHON VERSION: {sys.version}")
print(f"* * * * * * * * CURRENT WORKING DIRECTORY: {os.getcwd()}")
# Attempted to App().get_running_app() here but that returns None.


Builder.load_string("""
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
""")


class CameraClick(BoxLayout):
    def capture(self):
        """
        Function to capture the images and give them the names
        according to their captured time and date.
        """

        # running_app = TestCamera.get_running_app()
        running_app = TestCamera().get_running_app()
        user_data_dir = running_app.user_data_dir
        # REFERENCE: https://kivy.org/doc/stable/api-kivy.app.html#kivy.app.App.user_data_dir
        # TODO: Current problem is this is returning None.
        print(f"* * * * * * * * USER DATA DIRECTORY: {user_data_dir}")

        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print(f"* * * * * * * * CAPTURED AN IMAGE. ID: {timestr}")
        # TODO: Attempt alternate way to write image data. Use user_data_dir similar to this:
        #   filename = join(user_data_dir, "save.txt")
        #   with open(filename, "w") as fd:
        #       fd.write(image_data_or_text_lines_or_whatever)


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()


"""
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a button labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.
"""

##
#
