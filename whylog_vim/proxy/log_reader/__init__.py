from whylog import LogReader, FrontInput, LineSource
from whylog_vim.output_formater.log_reader_formater import LogReaderOutput


class LogReaderProxy(object):
    def __init__(self, editor, log_reader):
        self.editor = editor
        self._log_reader = log_reader

    def new_query(self):
        front_input = self.editor.get_front_input()
        query_output = self._log_reader.get_causes(front_input)

        self.output = LogReaderOutput.format_query(front_input, query_output)
        self.output.set_default_callback_function(self.editor.close_query_window)
        self.editor.create_query_window(self.output.get_content())
        self.editor.go_to_query_window()

    def handle_action(self):
        if self.editor.cursor_at_whylog_windows():
            self.output.call_button(self.editor.get_current_line())
        else:
            self.editor.close_query_window()

    def get_tree(self, front_input):
        raise NotImplemented()
