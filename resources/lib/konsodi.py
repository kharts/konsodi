# konsodi.py - main module of the addon
#
# Copyright 2016 kharts (https://github.com/kharts)
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.


import sys
from cStringIO import StringIO
import ast
from _ast import Expr
import pyxbmct
from common import *


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_ROWS = 12
WINDOW_COLUMNS = 16
COMMAND_HEIGHT = 1
PROMPT_WIDTH = 2
BUTTON_WIDTH = 2
HISTORY_ROWS = 16
ARROW_WIDTH = 1


def start():
    """
    Start the plugin
    :return: None
    """

    main_window = MainWindow("Konsodi")
    main_window.doModal()
    del main_window


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
            columnspan=WINDOW_COLUMNS-ARROW_WIDTH
        )
        self.history_shift = 0
        self.scroll_up_button = pyxbmct.Button(
            label="",
            focusTexture=image("up_blue.png"),
            noFocusTexture=image("up_white.png")
        )
        self.placeControl(
            self.scroll_up_button,
            row=0,
            column=WINDOW_COLUMNS-ARROW_WIDTH,
            rowspan=1,
            columnspan=ARROW_WIDTH
        )
        self.scroll_down_button = pyxbmct.Button(
            label="",
            focusTexture=image("down_blue.png"),
            noFocusTexture=image("down_white.png")
        )
        self.placeControl(
            self.scroll_down_button,
            row = WINDOW_ROWS-COMMAND_HEIGHT-1,
            column=WINDOW_COLUMNS-ARROW_WIDTH,
            rowspan=1,
            columnspan=ARROW_WIDTH
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
        self.globals = {}

    def run_command(self):
        """
        Run command
        :return: None
        """

        command = self.command.getText()
        debug("command: " + command)
        self.add_to_history(">>> " + command)

        self.set_streams()

        result = self.get_result(command)

        output = self.output.read()
        self.add_to_history(output)
        debug("output: " + output)

        self.add_to_history(result)
        debug("result: " + result)

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

        #self.history_box.setText(self.history)
        #self.history_box.scroll(len(self.history))
        self.show_history()

    def show_history(self):
        """
        Display command execution history on the history_box
        :return: None
        """

        lines = n_lines(self.history)
        if lines > HISTORY_ROWS:
            self.history_shift = lines - HISTORY_ROWS
        else:
            self.history_shift = 0
        all_rows = self.history.split("\n")
        last_rows = all_rows[self.history_shift:]
        text = "\n".join(last_rows)
        self.history_box.setText(text)

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

    def get_result(self, code):
        """
        Get result of execution of the line of code
        :param code: string of code
        :type code: str
        :return: str
        """

        try:
            tree = ast.parse(code)
        except Exception, e:
            return str(e)
        if not tree.body:
            return ""
        if isinstance(tree.body[0], Expr):
            try:
                result = eval(code, self.globals)
            except Exception, e:
                return str(e)
            return str(result)
        else:
            try:
                exec code in self.globals
            except Exception, e:
                return str(e)
            return ""


def n_lines(string):
    """
    Get number of lines in a string
    :param string: input string
    :type string: str
    :return: number of lines
    :rtype: int
    """

    return len(string.split("\n"))
