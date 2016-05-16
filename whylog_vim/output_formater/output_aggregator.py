from functools import partial
from whylog_vim.consts import Messages


class OutputAggregator(object):
    def __init__(self):
        self.buttons = {}
        self.output_lines = []

    def add(self, element):
        self.output_lines.append(element)

    def add_commented(self, content):
        self.add(Messages.COMMENT_PREFIX % content)

    def get_content(self):
        # The same type as vim buffor.
        return self.output_lines

    def create_button(self, callback_function, line=None):
        line = line or self._get_current_line_number()
        self.buttons[line] = callback_function

    def call_button(self, line_number):
        try:
            self.buttons[line_number]()
        except KeyError:
            pass

    def _get_current_line_number(self):
        return len(self.output_lines)
