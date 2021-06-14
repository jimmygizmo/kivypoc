import sys
import os
from os.path import join
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time

# Try later: from kivy.utils import platform THEN print(platform) etc.

# Uncomment these lines to see all the messages
from kivy.logger import Logger
import logging
Logger.setLevel(logging.TRACE)

print(f"* * * * * * * * PYTHON VERSION: {sys.version}")
print(f"* * * * * * * * CURRENT WORKING DIRECTORY: {os.getcwd()}")
# Attempted to App().get_running_app() here but that returns None. This would be because the app is not running yet. :)
# Turns out we can get it inside of CameraClick() and probably any handler.
# At the end of this main code, the 'running app' does not exist until the main event loop
# is started with TestCamera().run()


Builder.load_string("""
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: root.toggle_play()
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
""")

# ToggleButton used to have play control all in the kv like this:  on_press: camera.play = not camera.play
# I made it this way so I could do more in a proper method:
# on_press: root.toggle_play


class CameraClick(BoxLayout):
    camera_state = False

    def capture(self):
        """
        Function to capture the images and give them the names
        according to their captured time and date.
        """
        # running_app = TestCamera.get_running_app()
        running_app = TestCamera().get_running_app()  # THIS WORKS TO GET USER DATA DIR
        user_data_dir = running_app.user_data_dir
        # REFERENCE: https://kivy.org/doc/stable/api-kivy.app.html#kivy.app.App.user_data_dir
        # TODO: Current problem is this is returning None.
        print(f"* * * * * * * * USER DATA DIRECTORY: {user_data_dir}")

        camera = self.ids['camera']

        timestr = time.strftime("%Y%m%d_%H%M%S")
        image_file = f"IMG_{timestr}.png"
        writeable_path = join(user_data_dir, image_file)
        # camera.export_to_png("IMG_{}.png".format(timestr))  # Operation not permitted
        camera.export_to_png(writeable_path)  # Operation not permitted
        print(f"* * * * * * * * CAPTURED AN IMAGE. ID: {timestr}")
        # TODO: Attempt alternate way to write image data. Use user_data_dir similar to this:
        #   filename = join(user_data_dir, "save.txt")
        #   with open(filename, "w") as fd:
        #       fd.write(image_data_or_text_lines_or_whatever)

    def toggle_play(self):
        print(f"* * * * * * * * CAMERA PLAY TOGGLED. BEFORE STATE: {self.camera_state}")
        self.camera_state = not self.camera_state
        camera = self.ids['camera']
        camera.play = self.camera_state
        print(f"* * * * * * * * CAMERA PLAY TOGGLED. AFTER STATE: {self.camera_state}")


class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()

# This code never runs, meaning the preceding .run() is the start of an infinite event loop. Makes sense.
# running_app = TestCamera().get_running_app()  # WILL THIS WORK HERE? (It does work inside of CameraClick()).
# user_data_dir = running_app.user_data_dir
# print(f"* * * * * * * * (STARTUP) USER DATA DIRECTORY: {user_data_dir}")

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
