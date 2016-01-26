# konsodi.py - main module of the addon
#
# Copyright 2016 kharts (https://github.com/kharts)
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.


import pyxbmct


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_ROWS = 12
WINDOW_COLUMNS = 16


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
        self.history = pyxbmct.TextBox()
        self.placeControl(
            self.history,
            row=0,
            column=0,
            rowspan=WINDOW_ROWS-1,
            columnspan=WINDOW_COLUMNS
        )
        self.history.setText("Test text")