import six

from functools import partial
from whylog_vim.consts import Messages


class OutputAggregator(object):
    def __init__(self):
        self.function_lines = {}
        self.callbacks = {}
        self.output_lines = []

    def add(self, element):
        self.output_lines.append(element)

    def add_commented(self, content):
        self.add(Messages.COMMENT_PREFIX % content)

    def get_content(self):
        # The same type as vim buffor.
        return self.output_lines

    def create_button(self, callback_function, function_meta, line=None):
        line = line or self._get_current_line_number()
        self.function_lines[function_meta] = line
        self.callbacks[line] = callback_function

    def set_default_callback_function(self, default_callback_function):
        self.default_callback_function = default_callback_function

    def call_by_menu_function(self, menu_function):
        self.call_button(self.function_lines[menu_function])

    def get_line_number(self, function_meta):
        return self.function_lines[function_meta]

    def call_button(self, line_number):
        try:
            self.callbacks[line_number]()
        except KeyError:
            try:
                self.default_callback_function()
            except AttributeError:
                pass

    def _get_current_line_number(self):
        return len(self.output_lines)
