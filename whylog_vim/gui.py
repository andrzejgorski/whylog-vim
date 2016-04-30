from whylog import LineSource, FrontInput

from mock import MagicMock, patch
import os.path
import vim
from whylog_vim.input_reader.teacher_reader import get_button_name, filter_comments
from whylog_vim.consts import WindowTypes, WindowSizes


class VimCommander(object):

    @staticmethod
    def resize(size):
        vim.command('resize %s' % size)

    @staticmethod
    def set_file_type():
        vim.command('setlocal filetype=whylog')

    @staticmethod
    def get_column():
        return int(vim.eval('col(".")'))

    @staticmethod
    def get_current_window_id():
        return int(vim.eval('winnr()'))

    @staticmethod
    def normal(command):
        vim.command("normal %s" % (command,))

    @staticmethod
    def go_to_window(window_id):
        assert window_id is not None
        vim.command('%dwincmd w' % window_id)

    @staticmethod
    def split_window():
        vim.command(':split')

    @staticmethod
    def set_modifiable():
        vim.command('setlocal modifiable')

    @staticmethod
    def set_nomodifible():
        vim.command('setlocal nomodifiable')

    @staticmethod
    def open_file_at_window(filename):
        vim.command(':e %s' % filename)

    @staticmethod
    def set_nowritable():
        vim.command('setlocal buftype=nowrite')

    @staticmethod
    def close_current_window():
        vim.command(':q')

    @staticmethod
    def get_current_line():
        return vim.current.line

    @staticmethod
    def go_to_offset():
        vim.command(':go %d' % (byte_offset,))

    @staticmethod
    def _get_cursor_offset():
        return int(vim.eval('line2byte(line("."))'))

    @staticmethod
    def set_syntax_folding():
        vim.command(':set foldmethod=syntax')

    @staticmethod
    def get_current_filename():
        return vim.current.buffer.name

    @staticmethod
    def get_line_number():
        return int(vim.eval('line(".")'))

    @staticmethod
    def get_offset():
        return int(vim.eval('line2byte(line("."))+col(".")'))


class WindowContect(object):

    def __enter__(self):
        VimCommander.set_modifiable
        return vim.current.buffer

    def __exit__(self, type_, value, traceback):
        VimCommander.set_nomodifible


class Window(object):

    def __init__(self, name, content, modifiable):
        content = content or []
        self.context = WindowContext()
        VimCommander.open_file_at_window(name)
        VimCommander.set_nowritable()
        self.set_output(content)
        self.set_modifiable(modifiable)
        self.name = name
        VimCommander.set_file_type()
        self._set_window_id()

    def set_output(self, contents):
        with self.context as output_buffer:
            output_buffer[:] = contents.split('\n')

    def set_modifiable(self, modifiable):
        if modifiable:
            VimCommander.set_modifiable()
        else:
            VimCommander.set_nomodifible()

    def get_content(self):
        with self.output_window_context as output_buffer:
            return filter_comments(output_buffer[:])

    def _set_window_id(self):
        for window_id, window in enumerate(vim.windows):
            if window.buffer.name.endswith(self.name):
                self.window_id = window_id


class WhylogWindowManager(object):

    whylog_windows = [
        WindowTypes.QUERY,
        WindowTypes.TEACHER,
        WindowTypes.INPUT,
        WindowTypes.CASE,
    ]

    def __init__(self):
        self.windows = dict()

    def create_window(self, window_type, content=None, modifiable=False):
        self.windows[window_type] = Window(window_type, content, modifiable)

    def get_input_content(self, window_type):
        return self.windows[window_type].get_content()

    def go_to_window(self, window_type):
        VimCommander.go_to_window(self.windows[window_type].window_id)

    def close_window(self, window_type):
        self.go_to_window()
        VimCommander.close_current_window()
        del self.windows[window_type]

    def are_windows_closed(self):
        return len(self.windows) == 0


class FilesManager(object):

    @staticmethod
    def get_files_window_id(file_name):
        for id_, window in enumerate(vim.windows):
            if window.buffer.name.endswith(file_name):
                return (id_ + 1)
        return None

    @classmethod
    def is_file_open(cls, file_name):
        if FilesManager.get_files_window_id(file_name) is not None:
            return True
        return False

    @staticmethod
    def go_to_file(file_name, offset=1):
        window_id = FilesManager.get_files_window_id(file_name)
        if window_id is not None:
            VimCommander.go_to_window(window_id)
        else:
            VimCommander.split_window()
            VimCommander.open_file_at_window(filename)
        VimCommander.go_to_offset(offset)


class VimEditor(object):

    def __init__(self):
        self.window_manager = WhylogWindowManager()

    def get_input_content(self):
        return filter_comments(
            self.window_manager.get_window_content(WindowTypes.INPUT))

    def create_case_window(self, default_input):
        self.window_manager.create_window(WindowTypes.CASE, default_input)

    def create_input_window(self, default_input=None):
        self.window_manager.create_window(WindowTypes.INPUT, default_input, modifiable=True)

    def create_teacher_window(self):
        self.window_manager.create_window(WindowTypes.TEACHER)

    def create_query_window(self):
        self.window_manager.create_window(WindowTypes.QUERY)

    def is_any_whylog_window_open(self):
        return not self.window_manager.are_windows_closed()

    def close_window(self, filename):
        if not FileManager.is_file_open(filename):
            VimCommand.close_current_window()

    def get_button_name(self):
        return get_button_name(VimCommander.get_current_line(), VimCommander.get_column())

    def get_front_input(self):
        """
        This method returns Front Input object of the line where cursor is,
        """
        filename = self.get_current_filename()
        host = 'localhost'
        cursor_position = VimCommander.get_cursor_offset()
        line_content = VimCommander.get_current_line()
        line_source = LineSource(host, filename)
        return FrontInput(cursor_position, line_content, line_source)

    def close_query_window(self):
        self.window_manager.close(WindowTypes.QUERY)

    def close_teacher_window(self):
        self.window_manager.close(WindowTypes.TEACHER)

    def cursor_at_output(self):
        return VimCommander.get_current_window_id() == self._get_output_window_id()

    def cursor_at_teacher(self):
        return VimCommander.get_current_window_id() == self._get_files_window_id(WindowTypes.TEACHER)

    def cursor_at_input(self):
        return VimCommander.get_current_window_id() == self._get_files_window_id(WindowTypes.INPUT)

    def cursor_at_case(self):
        return VimCommander.get_current_window_id() == self._get_files_window_id(WindowTypes.CASE)

    def go_to_output_window(self):
        self.window_manager.go_to_window(WindowTypes.QUERY)

    def go_to_offset(self, byte_offset):
        VimCommander.go_to_offset(offset)

    def set_syntax_folding(self):
        VimCommander.set_syntax_folding()

    def open_fold(self):
        # normal command in vim witch opens fold.
        VimCommander.normal('zo')

    def get_current_line(self):
        return VimCommander.get_current_line()

    def get_current_filename(self):
        return VimCommander.get_current_filename()

    def get_line_number(self):
        return VimCommander.get_line_number()

    def get_offset(self):
        return VimCommander.get_offset()
