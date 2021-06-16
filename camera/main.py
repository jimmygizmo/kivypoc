import sys
import os
# import os.path
from kivy.app import App
# from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time

from kivy.utils import platform  # ios, android, macosx, linux, win or unknown


from kivy.logger import Logger
import logging


Logger.setLevel(logging.TRACE)  # Set log level to maximum detail level.
# Currently the logging output seen with TRACE is very reasonable/minimal. Of course some of the logging is coming
# from the IOS/XCode side and can be addressed separately, but so far logging is both minimal and very informative
# overall. (As seen in the XCode run output when running the app on an iPhone.)

print(f"* * * * * * * * KIVY CAMERA DEMO APP STARTING. App class name: TestCamera")
print(f"* * * * * * * * STDOUT/prints from application Python code will usually begin with 4 or 8 asterisks * * * *")
# TODO: See about switching to using nothing but the logging module. Configure it properly for STDOUT default.
#  See restproto project for good example of basic logging config for STDOUT logging.
print(f"* * * * * * * * PLATFORM: {platform}")

print(f"* * * * * * * * PYTHON VERSION (sys.version): {sys.version}")
print(f"* * * * * * * * CURRENT WORKING DIRECTORY (os.getcwd): {os.getcwd()}")


# ################################################ CLASS DEFINITIONS ###################################################


class CameraClick(BoxLayout):
    camera_state = False

    def capture(self):
        """
        Function to capture the images and give them the names
        according to their captured time and date.
        """
        running_app = TestCamera().get_running_app()
        user_data_dir = running_app.user_data_dir
        # REFERENCE: https://kivy.org/doc/stable/api-kivy.app.html#kivy.app.App.user_data_dir
        print(f"* * * * * * * * USER DATA DIRECTORY: {user_data_dir}")

        camera = self.ids['camera']  # TODO: Investigate what .ids['...'] can do.

        timestr = time.strftime("%Y%m%d_%H%M%S")
        print(f"* * * * * * * * CAPTURED AN IMAGE. ID: {timestr}")
        image_file = f"IMG_{timestr}.png"
        image_path = os.path.join(user_data_dir, image_file)
        print(f"* * * * * * * * CAPTURED IMAGE FILE PATH TO WRITE: {image_path}")
        camera.export_to_png(image_path)

        # TODO: Attempt alternate way to write image data. Use user_data_dir similar to this:
        #   filename = join(user_data_dir, "save.txt")
        #   with open(filename, "w") as fd:
        #       fd.write(image_data_or_text_lines_or_whatever)

        # TODO: Image capture appears to be working. No errors. However the image files must be verified on the device.
        #   Even better: setup a service to HTTP-post them to etc.

        self.dirlist(user_data_dir)

    @staticmethod
    def dirlist(dirpath):
        print(f"* * * * * * * * DIR LISTING OF USER DATA DIR:")
        items = os.listdir(dirpath)
        for item in items:
            print(f"* * * *: {item}")
        for item in items:
            item_absolute = os.path.join(dirpath, item)
            print(f"* * * *: {item}")

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

# Any code below here never runs, at least until (possibly/unconfirmed) the App is finalizing and exiting.
# The preceding .run() is the start of an infinite event loop. Makes sense.

print(f"* * * * * * * * App.run() has completed. APP EXITING.")

# ################################################## MAIN EXECUTION ####################################################


"""
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a button labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.
"""


# ##########################################################
############################################################

##
#
