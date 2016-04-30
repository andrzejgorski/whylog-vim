from mock import MagicMock, patch
from whylog.log_reader import LogReader
from whylog.front.utils import FrontInput
from whylog.config import LineSource
from whylog_vim.output_formater.log_reader_formater import LogReaderOutput
from whylog_vim.input_reader.log_reader import QueryInputReader


class LogReaderProxy():

    def __init__(self, editor, log_reader):
        self.editor = editor
        self._log_reader = log_reader
        self.output_formater = LogReaderOutput()
        self.input_reader = QueryInputReader()

    def new_query(self):
        front_input = self.editor.get_front_input()
        # Mock
        with patch('whylog.log_reader.LogReader.get_causes') as mock:
            mock.return_value = self.mock_query_output(front_input)
            query_output = self._log_reader.get_causes(front_input)

        contents = self.output_formater.format_query(front_input, query_output)
        self.editor.create_query_window(contents)
        self.editor.go_to_query_window()
        return True

    def _handle_signal_on_output(self):
        current_line = self.editor.get_current_line()
        match = self.input_reader.match_output_line(current_line)
        if match is not False:
            file_name, offset = match
            self.editor.go_to_file(file_name, offset)
        else:
            self.editor.close_query_window()

    def handle_action(self):
        if self.editor.cursor_at_output():
            self._handle_signal_on_output()
        else:
            self.editor.close_query_window()

    def get_tree(self, front_input):
        raise NotImplemented()

    # TOFIX
    def mock_query_output(self, front_input):
        if front_input.offset == 34:
            return [FrontInput(
                21, '2 root cause',
                LineSource('localhost', 'node_1.log'))
            ]
        else:
            return []
