from whylog.front.utils import FrontInput
from whylog.config import LineSource

from mock import MagicMock, patch
import os.path
import vim
from whylog_vim.input_reader.teacher_reader import get_button_name, filter_comments
from whylog_vim.consts import WindowTypes, WindowSizes



class WindowContext(object):

    def __init__(self, gui):
        self.gui = gui

    def __enter__(self):
        vim.command('setlocal modifiable')
        return vim.current.buffer

    def __exit__(self, type_, value, traceback):
        vim.command('setlocal nomodifiable')


class VimEditor():

    whylog_windows = [
        WindowTypes.QUERY,
        WindowTypes.TEACHER,
        WindowTypes.INPUT,
        WindowTypes.CASE,
    ]

    def get_input_content(self):
        with self.output_window_context as output_buffer:
            return filter_comments(output_buffer[:])

    def go_to_file(self, file_name, offset=1):
        id_ = self.get_files_window_id(file_name)
        if id_ is not None:
            self.go_to_window(id_)
            self.go_to_offset(offset)
        else:
            self.split_window()
            self.open_file_at_offset(file_name, offset)

    def create_case_window(self, default_input):
        self.output_window_context = WindowContext(self)
        vim.command(':e %s' % WindowTypes.CASE)
        vim.command(':setlocal buftype=nowrite')
        self.set_output(default_input)
        vim.command(':set nomodifiable')
        self._set_file_type()

    def create_input_window(self, default_input):
        self.output_window_context = WindowContext(self)
        vim.command(':e %s' % WindowTypes.INPUT)
        vim.command(':setlocal buftype=nowrite')
        self.set_output(default_input)
        vim.command(':set modifiable')
        self._set_file_type()

    def create_teacher_window(self):
        self.output_window_context = WindowContext(self)
        vim.command(':e %s' % WindowTypes.TEACHER)
        vim.command(':setlocal buftype=nowrite')
        vim.command(':set nomodifiable')
        self._set_file_type()

    def create_query_window(self):
        self.output_window_context = WindowContext(self)
        vim.command(':rightbelow split %s' % WindowTypes.QUERY)
        vim.command(':setlocal buftype=nowrite')
        self.resize(10)
        vim.command(':setlocal nomodifiable')
        self._set_file_type()

    def close_window(self, filename):
        self.go_to_file(filename)
        vim.command(':q')

    def get_button_name(self):
        return get_button_name(self.get_current_line(), self.get_col())

    def set_output(self, contents):
        with self.output_window_context as output_buffer:
            output_buffer[:] = contents.split('\n')

    def _get_output_window_id(self):
        for id_, window in enumerate(vim.windows):
            for name in self.whylog_windows:
                if window.buffer.name.endswith(name):
                    return int(id_)+1
        return None

    def get_cursor_offset(self):
        """
        This method return offset -
        byte of the first char of the line
        where is cursor, when the method is called.
        """
        return int(vim.eval('line2byte(line("."))'))

    def get_front_input(self):
        """
        This method return Front Input object of the line where cursor is,
        which is implemented in the whylog.front.utils.py file.
        """
        filename = self.get_current_filename()
        host = 'localhost'
        cursor_position = self.get_cursor_offset()
        line_content = self.get_current_line()
        line_source = LineSource(host, filename)
        return FrontInput(cursor_position, line_content, line_source)

    def close_output_window(self):
        """
        Same as name of the function. Closing window where is output of the Whylog.
        """
        self.go_to_output_window()
        vim.command(':q')

    def is_whylog_window_open(self):
        for id_, window in enumerate(vim.windows):
            for name in self.whylog_windows:
                if window.buffer.name.endswith(name):
                    return True
        return False

    def get_files_window_id(self, file_name):
        for id_, window in enumerate(vim.windows):
            if window.buffer.name.endswith(file_name):
                return (id_ + 1)
        return None

    def is_file_open(self, file_name):
        if self.get_files_window_id(file_name) is not None:
            return True
        else:
            return False

    def cursor_at_output(self):
        return self.get_current_window_id() == self._get_output_window_id()

    def cursor_at_teacher(self):
        return self.get_current_window_id() == self.get_files_window_id(WindowTypes.TEACHER)

    def cursor_at_input(self):
        return self.get_current_window_id() == self.get_files_window_id(WindowTypes.INPUT)

    def cursor_at_case(self):
        return self.get_current_window_id() == self.get_files_window_id(WindowTypes.CASE)

    def go_to_output_window(self):
        """
        After call of this function cursor
        is moving to the output window.
        """
        id_ = self._get_output_window_id()
        self.go_to_window(id_)

    def go_to_line(self, line):
        vim.command(':%d' % (line,))

    def go_to_offset(self, byte_offset):
        vim.command(':go %d' % (byte_offset,))

    def open_file_at_offset(self, filename, offset):
        vim.command(':edit %s' % (filename,))
        self.go_to_offset(offset)

    def go_to_window(self, window_id):
        assert window_id is not None
        vim.command('%dwincmd w' % window_id)

    def split_window(self):
        vim.command(':split')

    def set_syntax_folding(self):
        vim.command(':set foldmethod=syntax')

    def normal(self, command):
        vim.command("normal %s" % (command,))

    def get_col(self):
        return int(vim.eval('col(".")'))

    def get_current_window_id(self):
        return int(vim.eval('winnr()'))

    def get_current_line(self):
        """
        Method returns content of the line where cursor is.
        """
        return vim.current.line

    def get_current_filename(self):
        return vim.current.buffer.name

    def get_line_number(self):
        return int(vim.eval('line(".")'))

    def get_offset(self):
        return int(vim.eval('line2byte(line("."))+col(".")'))

    def resize(self, size):
        vim.command('resize %s' % size)

    def _set_file_type(self):
        vim.command('setlocal filetype=whylog')

