from whylog_vim.consts import Messages


def pass_function():
    pass


class OutputAggregator(object):
    def __init__(self):
        """
        This class represents the content of the window in vim editor.
        The output_lines attribute stores content of the output in the list.

        The callbacks attribute is the dict with key the line number and
        the value callback function which will be called when user do action
        on that line.

        The function_lines is the dict with key the touple
        (function_name, *params_identity).
        function_name is a string which represent the function.
        *params_identity is value or are values for function which is for
        identify the params of the function.
        Example of the key of function_lines is ('delete parser', 2) where
        2 is the id of the parser which will be deleted.
        The value of the function_lines dict is the line number where the
        specified by key function can be called, when the line will be pressed.

        The default_callback_function is the callback for the line number
        which is not stored in callbacks.
        """
        self.output_lines = []
        self.callbacks = {}
        self.function_lines = {}
        self.default_callback_function = pass_function

    def add(self, element):
        self.output_lines.append(element)

    def add_commented(self, content):
        self.add(Messages.COMMENT_PREFIX % content)

    def get_content(self):
        # The same type as vim buffor.
        return self.output_lines

    def create_button(self, callback_function, function_meta, line=None):
        """
        This function create callback_function for the specified line.
        The function_meta param is the key for function_lines.
        By default function_meta should be touple of the
        (function_name, *params_identity)
        The meaning of the touple is described in __init__ docstring.
        """
        line = line or self._get_current_line_number()
        self.function_lines[function_meta] = line
        self.callbacks[line] = callback_function

    def set_default_callback_function(self, default_callback_function):
        self.default_callback_function = default_callback_function

    def call_by_menu_function(self, function_meta):
        """
        This function calls specified by meta params function.
        function_meta is described in __init__ docstring.
        """
        self.call_button(self.function_lines[function_meta])

    def call_button(self, line_number):
        callback = self.callbacks.get(line_number, self.default_callback_function)
        return callback()

    def _get_current_line_number(self):
        return len(self.output_lines)
