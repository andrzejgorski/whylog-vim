from mock import MagicMock, patch
from whylog.log_reader import LogReader
from whylog.front.utils import FrontInput, LocallyAccessibleLogOpener
from whylog_vim.output_formater.log_reader_formater import LogReaderOutput


class LogReaderProxy():

    def __init__(self, editor):
        self.editor = editor
        self._log_reader = LogReader({})
        self.output_formater = LogReaderOutput()

    def new_query(self):
        self.editor.create_output_window()
        front_input = self.editor.get_front_input()

        # Mock
        with patch('whylog.log_reader.LogReader.get_causes') as mock:
            mock.return_value = self.mock_query_output()
            query_output = self._log_reader.get_causes(front_input)

        contents = self.output_formater.format_query(front_input, query_output)
        self.editor.set_output(contents, line=4)
        self.editor.go_to_output_window()
        return True

    def _handle_signal_on_output(self):
        current_line = self.editor.get_current_line()
        match = self.output_formater.match_output_line(current_line)
        if match is not False:
            file_name, offset = match
            self.editor.open_cause_window(file_name, offset)
        else:
            self.editor.close_output_window()

    def signal_1(self):
        if self.editor.cursor_at_output():
            self._handle_signal_on_output()
        else:
            self.editor.close_output_window()

    def signal_2(self):
        pass

    def get_tree(self, front_input):
        raise NotImplemented()

    # TOFIX
    def mock_query_output(self):
        if self.editor.get_cursor_offset() == 34:
            return [FrontInput(
                21, '2 root cause',
                LocallyAccessibleLogOpener(
                    self.editor.get_input_window_file_name()))
            ]
        else:
            return []
