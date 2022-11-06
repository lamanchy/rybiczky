from os.path import dirname, abspath
import sys

FPS = 30
RESET_DISTANCE = 1000
SCALE = 0.5


if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    BASE_PATH = sys._MEIPASS
    FULLSCREEN = True
    DEBUG = False

else:
    BASE_PATH = dirname(dirname(abspath(__file__)))
    FULLSCREEN = False
    DEBUG = True
