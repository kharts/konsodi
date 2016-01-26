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
COMMAND_HEIGHT = 1
PROMPT_WIDTH = 2


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
        self.history = ""
        self.history_box = pyxbmct.TextBox()
        self.placeControl(
            self.history_box,
            row=0,
            column=0,
            rowspan=WINDOW_ROWS-COMMAND_HEIGHT,
            columnspan=WINDOW_COLUMNS
        )
        self.history_box.setText("Test text")
        self.prompt = pyxbmct.Label(">>>")
        self.placeControl(
            self.prompt,
            row=WINDOW_ROWS-COMMAND_HEIGHT,
            column=0,
            rowspan=COMMAND_HEIGHT,
            columnspan=PROMPT_WIDTH
        )
        self.command = pyxbmct.Edit()
        self.placeControl(
            self.command,
            row=WINDOW_ROWS-COMMAND_HEIGHT,
            column=PROMPT_WIDTH,
            rowspan=COMMAND_HEIGHT,
            columnspan=WINDOW_COLUMNS-PROMPT_WIDTH
        )