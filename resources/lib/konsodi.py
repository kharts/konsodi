# konsodi.py - main module of the addon
#
# Copyright 2016 kharts (https://github.com/kharts)
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.


import pyxbmct


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_ROWS = 1
WINDOW_COLUMNS = 1


def start():
    """
    Start the plugin
    :return: None
    """

    main_window = MainWindow("Konsodi")
    main_window.doModal()


class MainWindow(pyxbmct.AddonDialogWindow):
    """
    Main windows of the plugin
    """

    def __init__(self, title):
        super(MainWindow, self).__init__(title)
        self.setGeometry(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            WINDOW_ROWS,
            WINDOW_COLUMNS
        )