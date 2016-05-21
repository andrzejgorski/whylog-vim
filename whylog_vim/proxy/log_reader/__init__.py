import six
from whylog.log_reader.exceptions import NoLogTypeError
from whylog_vim.output_formater.log_reader_formater import LogReaderOutput


class LogReaderProxy(object):
    def __init__(self, editor, log_reader, config):
        self.editor = editor
        self._log_reader = log_reader
        self.config = config

    def _ask_log_type(self):
        pass

    def new_query(self):
        front_input = self.editor.get_front_input()
        try:
            query_output = self._log_reader.get_causes(front_input)
        except NoLogTypeError:
            log_types = self.config.get_all_log_types()
            if log_types:
                self._ask_log_type(self, log_types)
            else:
                six.print_(Messages.EMPTY_DATA_BASE)
                return

        self.output = LogReaderOutput.format_query(front_input, query_output)
        self.output.set_default_callback_function(self.editor.close_query_window)
        self.editor.create_query_window(self.output.get_content())
        self.editor.go_to_query_window()

    def handle_action(self):
        if self.editor.is_cursor_at_whylog_windows():
            self.output.call_button(self.editor.get_current_line())
        else:
            self.editor.close_query_window()

    def get_tree(self, front_input):
        raise NotImplemented()
