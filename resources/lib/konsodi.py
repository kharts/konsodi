# konsodi.py - main module of the addon
#
# Copyright 2016 kharts (https://github.com/kharts)
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.


import sys
from cStringIO import StringIO
import pyxbmct
from common import *


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_ROWS = 12
WINDOW_COLUMNS = 16
COMMAND_HEIGHT = 1
PROMPT_WIDTH = 2
BUTTON_WIDTH = 2


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
        self.prompt = pyxbmct.Label(">>>")
        self.placeControl(
            self.prompt,
            row=WINDOW_ROWS-COMMAND_HEIGHT,
            column=0,
            rowspan=COMMAND_HEIGHT,
            columnspan=PROMPT_WIDTH
        )
        self.command = pyxbmct.Edit("")
        self.placeControl(
            self.command,
            row=WINDOW_ROWS-COMMAND_HEIGHT,
            column=PROMPT_WIDTH,
            rowspan=COMMAND_HEIGHT,
            columnspan=WINDOW_COLUMNS-PROMPT_WIDTH-BUTTON_WIDTH
        )
        self.run_button = pyxbmct.Button("Run")
        self.placeControl(
            self.run_button,
            row=WINDOW_ROWS-COMMAND_HEIGHT,
            column=WINDOW_COLUMNS-BUTTON_WIDTH,
            rowspan=COMMAND_HEIGHT,
            columnspan=BUTTON_WIDTH
        )
        self.connect(self.run_button, self.run_command)
        self.setFocus(self.command)

    def run_command(self):
        """
        Run command
        :return: None
        """

        command = self.command.getText()
        debug("command: " + command)
        self.add_to_history(">>> " + command)

        self.set_streams()

        try:
            result = eval(command)
        except Exception, e:
            result = e

        output = self.output.read()
        self.add_to_history(output)
        debug("output: " + output)

        result_text = str(result)
        self.add_to_history(result_text)
        debug("result: " + result_text)

        self.reset_streams()

        self.command.setText("")

    def add_to_history(self, message):
        """
        Add message to history
        :param message: text of the message
        :type message: text
        :return: None
        """

        if not message:
            return

        if self.history:
            self.history += "\n"

        self.history += message

        self.history_box.setText(self.history)
        self.history_box.scroll(len(self.history))

    def set_streams(self):
        """
        Change standard output and error streams
        :return: None
        """

        self.old_stdout = sys.stdout
        self.old_sterr = sys.stderr
        self.output = StringIO()
        sys.stdout = self.output
        sys.stderr = self.output

    def reset_streams(self):
        """
        Revert back standard output and error streams
        :return: None
        """

        sys.stdout = self.old_stdout
        sys.stderr = self.old_sterr