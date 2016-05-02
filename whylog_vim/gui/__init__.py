from whylog import LineSource, FrontInput

from mock import MagicMock, patch
import os.path
import vim
from whylog_vim.input_reader.teacher_reader import get_button_name, filter_comments
from whylog_vim.consts import WindowTypes, WindowSizes
from whylog_vim.gui.vim_commander import VimCommander
from whylog_vim.gui.windows import WhylogWindowManager
from whylog_vim.gui.files_manager import FilesManager


class VimEditor(object):

    def __init__(self):
        self.window_manager = WhylogWindowManager()

    def get_input_content(self):
        return filter_comments(
            self.window_manager.get_window_content(WindowTypes.INPUT))

    def create_case_window(self, default_input=None):
        self.window_manager.create_window(WindowTypes.CASE, default_input)

    def create_input_window(self, default_input=None):
        self.window_manager.create_window(WindowTypes.INPUT, default_input, modifiable=True)

    def create_teacher_window(self, default_input=None):
        self.window_manager.create_window(WindowTypes.TEACHER, default_input)

    def create_query_window(self, default_input=None):
        self.window_manager.create_window(WindowTypes.QUERY, default_input, False, WindowSizes.QUERY_WINDOW)

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
            VimCommand.close_current_window()

    def get_button_name(self):
        return get_button_name(VimCommander.get_current_line(), VimCommander.get_column())

    def get_front_input(self):
        """
        This method returns Front Input object of the line where cursor is.
        """
        filename = self.get_current_filename()
        # TODO add proper host
        host = 'localhost'
        cursor_position = VimCommander.get_cursor_offset()
        line_content = VimCommander.get_current_line()
        line_source = LineSource(host, filename)
        return FrontInput(cursor_position, line_content, line_source)

    def close_query_window(self):
        self.window_manager.close_window(WindowTypes.QUERY)

    def close_teacher_window(self):
        self.window_manager.close_window(WindowTypes.TEACHER)

    def cursor_at_whylog_windows(self):
        return VimCommander.get_current_window_id() in self.window_manager.get_windows_ids()

    def cursor_at_teacher_window(self):
        return VimCommander.get_current_window_id() == self.window_manager.get_window_id(WindowTypes.TEACHER)

    def cursor_at_input_window(self):
        return VimCommander.get_current_window_id() == self.window_manager.get_window_id(WindowTypes.INPUT)

    def cursor_at_case_window(self):
        return VimCommander.get_current_window_id() == self.window_manager.get_window_id(WindowTypes.CASE)

    def go_to_query_window(self):
        self.window_manager.go_to_window(WindowTypes.QUERY)

    def go_to_offset(self, byte_offset):
        VimCommander.go_to_offset(byte_offset)

    def set_syntax_folding(self):
        VimCommander.set_syntax_folding()

    def open_fold(self):
        # normal command in vim which opens fold.
        VimCommander.normal('zo')

    def get_current_line(self):
        return VimCommander.get_current_line()

    def get_current_filename(self):
        return VimCommander.get_current_filename()

    def get_line_number(self):
        return VimCommander.get_line_number()

    def get_offset(self):
        return VimCommander.get_offset()
