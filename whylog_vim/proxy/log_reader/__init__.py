import six
from whylog.log_reader.exceptions import NoLogTypeError
from whylog_vim.consts import EditorStates, Messages
from whylog_vim.output_formater.log_reader_formater import LogReaderOutput


class LogReaderProxy(object):
    def __init__(self, log_reader, config, editor, main_proxy):
        self._log_reader = log_reader
        self._config = config
        self._editor = editor
        self._main_proxy = main_proxy

    def _ask_log_type(self, log_types):
        pass

    def new_query(self):
        front_input = self._editor.get_front_input()
        try:
            query_output = self._log_reader.get_causes(front_input)
        except NoLogTypeError:
            log_types = [logType for logType in self._config.get_all_log_types()]
            if log_types:
                self._ask_log_type(log_types)
            else:
                six.print_(Messages.EMPTY_DATABASE)
                self._main_proxy.set_state(EditorStates.EDITOR_NORMAL)
        else:
            self.output = LogReaderOutput.format_query(front_input, query_output)
            self.output.set_default_callback_function(self._editor.close_query_window)
            self._editor.create_query_window(self.output.get_content())
            self._editor.go_to_query_window()

    def handle_action(self):
        if self._editor.is_cursor_at_whylog_windows():
            self.output.call_button(self._editor.get_current_line())
        else:
            self._editor.close_query_window()

    def get_tree(self, front_input):
        raise NotImplemented()
