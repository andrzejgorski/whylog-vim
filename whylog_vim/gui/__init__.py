from whylog import LineSource, FrontInput

from whylog_vim.input_reader import InputReader
from whylog_vim.consts import WindowTypes, WindowSizes
from whylog_vim.gui.vim_ui_wrapper import VimUIWrapper
from whylog_vim.gui.windows import WhylogWindowManager
from whylog_vim.gui.files_manager import FilesManager


class VimEditor(object):
    def __init__(self):
        self.window_manager = WhylogWindowManager()

    def get_input_content(self):
        return InputReader.filter_comments(
            self.window_manager.get_window_content(WindowTypes.INPUT)
        )

    def create_case_window(self, default_input=None):
        self.window_manager.create_window(WindowTypes.CASE, default_input)

    def create_input_window(self, default_input=None):
        self.window_manager.create_window(WindowTypes.INPUT, default_input, modifiable=True)

    def create_teacher_window(self, default_input=None):
        self.window_manager.create_window(WindowTypes.TEACHER, default_input)

    def create_query_window(self, default_input=None):
        self.window_manager.create_window(
            WindowTypes.QUERY, default_input, False, WindowSizes.QUERY_WINDOW
        )

    def go_to_file(self, filename, offset=1):
        FilesManager.go_to_file(filename, offset)

    def set_query_output(self, content):
        self.window_manager.set_content(WindowTypes.QUERY, content)

    def set_teacher_output(self, content):
        self.window_manager.set_content(WindowTypes.TEACHER, content)

    def is_any_whylog_window_open(self):
        return not self.window_manager.are_windows_closed()

    def close_window(self, filename):
        if not FilesManager.is_file_open(filename):
            VimUIWrapper.close_current_window()

    def get_button_name(self):
        return InputReader.get_button_name(
            VimUIWrapper.get_current_line(), VimUIWrapper.get_column()
        )

    def get_front_input(self):
        """
        This method returns Front Input object of the line where cursor is.
        """
        filename = self.get_current_filename()
        # TODO add proper host
        host = 'localhost'
        cursor_position = VimUIWrapper.get_cursor_offset()
        line_content = VimUIWrapper.get_current_line()
        line_source = LineSource(host, filename)
        return FrontInput(cursor_position, line_content, line_source)

    def close_query_window(self):
        self.window_manager.close_window(WindowTypes.QUERY)

    def close_teacher_window(self):
        self.window_manager.close_window(WindowTypes.TEACHER)

    def is_cursor_at_whylog_windows(self):
        return VimUIWrapper.get_current_window_id() in self.window_manager.get_windows_ids()

    def is_cursor_at_teacher_window(self):
        return VimUIWrapper.get_current_window_id() == self.window_manager.get_window_id(
            WindowTypes.TEACHER
        )

    def is_cursor_at_input_window(self):
        return VimUIWrapper.get_current_window_id() == self.window_manager.get_window_id(
            WindowTypes.INPUT
        )

    def is_cursor_at_case_window(self):
        return VimUIWrapper.get_current_window_id() == self.window_manager.get_window_id(
            WindowTypes.CASE
        )

    def go_to_query_window(self):
        self.window_manager.go_to_window(WindowTypes.QUERY)

    def go_to_offset(self, byte_offset):
        VimUIWrapper.go_to_offset(byte_offset)

    def set_syntax_folding(self):
        VimUIWrapper.set_syntax_folding()

    def open_fold(self):
        # normal command in vim which opens fold.
        VimUIWrapper.normal('zo')

    def get_current_line(self):
        return VimUIWrapper.get_current_line()

    def get_current_filename(self):
        return VimUIWrapper.get_current_filename()

    def get_line_number(self):
        return VimUIWrapper.get_line_number()

    def get_line_offset(self):
        return VimUIWrapper.get_line_offset()
