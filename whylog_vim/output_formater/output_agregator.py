import re
from whylog_vim.consts import Messages


class OutputAgregator(object):
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

    def create_button_on_line(self, click_function, line, **params):
        self.buttons[line] = partial(click_function, **params)

    def call_button(self, line_number):
        try:
            self.buttons[line_number]()
        except KeyError:
            pass

    def _get_current_line_number(self):
        return len(self.output_lines)