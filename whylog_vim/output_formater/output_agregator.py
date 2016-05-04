import re
from whylog_vim.consts import Messages


class Button():
    def __init__(self, function, **params):
        self.function = function
        self.params = params

    def __call__(self):
        self.function(**self.params)


class OutputAgregator():
    def __init__(self):
        self.buttons = {}
        self.output_lines = []

    def add(self, element):
        self.output_lines.append(element)

    def add_commented(self, content):
        self.add(Messages.PREFIX % content)

    def get_content(self):
        # The same type as vim buffor.
        return self.output_lines

    def set_button(self, button):
        line = self._get_line()
        self.buttons[line] = button

    def create_button(self, function, **params):
        line = self._get_line()
        self.buttons[line] = Button(function, **params)

    def call_button(self, line):
        try:
            self.buttons[line]()
        except KeyError:
            pass

    def _get_line(self):
        return len(self.output_lines)
