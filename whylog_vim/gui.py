from whylog.front.utils import FrontInput, LocallyAccessibleLogOpener

from mock import MagicMock, patch
import os.path
import vim
from whylog_vim.input_reader.teacher_reader import get_button_name


def go_to_line(line):
    vim.command(':%d' % (line,))

def go_to_offset(byte_offset):
    vim.command(':go %d' % (byte_offset,))

def open_file_at_offset(filename, offset):
    vim.command(':edit %s' % (filename,))
    go_to_offset(offset)

def open_file_at_line(filename, line):
    vim.command(':edit %s' % (filename,))
    go_to_line(line)

def go_to_window(window_id):
    assert window_id is not None
    vim.command('%dwincmd w' % window_id)

def split_window():
    vim.command(':split')

def set_syntax_folding():
    vim.command(':set foldmethod=syntax')

def normal(command):
    vim.command("normal %s" % (command,))

def get_cursor_position():
    line = vim.current.line
    range_ = vim.current.range
    assert range_.start == range_.end
    return range_.start

def get_col():
    return int(vim.eval('col(".")'))

def get_current_window_id():
    return int(vim.eval('winnr()'))

def get_current_line():
    """
    Method returns content of the line where cursor is.
    """
    return vim.current.line

def get_current_filename():
    return vim.current.buffer.name

def get_line_number():
    return int(vim.eval('line(".")'))

def resize(size):
    vim.command('resize %s' % size)


class OutputWindowContext(object):
    def __init__(self, gui):
        self.gui = gui
        self.origin_window_id = get_current_window_id()
        self.origin_window_name = get_current_filename()

    def __enter__(self):
        self.gui.go_to_output_window()
        self.gui.set_window_writability(True)
        return vim.current.buffer

    def __exit__(self, type_, value, traceback):
        self.gui.set_window_writability(False)
        go_to_window(self.origin_window_id)


WhylogWindowsTypes = {
    'query': 'whylog_query_output',
    'teacher': 'whylog_teacher',
    'input': 'whylog_input',
    'message': 'whylog_message',
}


class VimEditor():

    WINDOW_WRITEABILITY_STATE_DICT = {
        True: 'modifiable',
        False: 'nomodifiable',
    }

    def get_input_content(self):
        with self.output_window_context as output_buffer:
            return output_buffer[:]

    def go_to_file(self, file_name, offset):
        id_ = self.get_files_window_id(file_name)
        if id_ is not None:
            go_to_window(id_)
            go_to_offset(offset)
        else:
            split_window()
            open_file_at_offset(file_name, offset)

    def create_input_window(self, default_input):
        self.output_window_context = OutputWindowContext(self)
        vim.command(':e %s' % WhylogWindowsTypes['input'])
        vim.command(':setlocal buftype=nowrite')
        self.set_output(default_input)
        vim.command(':set modifiable')

    def change_to_teacher_window(self):
        self.output_window_context = OutputWindowContext(self)
        vim.command(':e %s' % WhylogWindowsTypes['teacher'])
        vim.command(':setlocal buftype=nowrite')

    def create_query_window(self):
        """
        Method witch close window where is an output of the Whylog.
        """
        if not self.is_whylog_window_open():
            vim.command(':rightbelow split %s' % WhylogWindowsTypes['query'])
            vim.command(':setlocal buftype=nowrite')
            vim.command(':resize 10')
            vim.command(':setlocal nomodifiable')
            vim.command(':wincmd k')
        self.output_window_context = OutputWindowContext(self)

    def create_teacher_window(self):
        """
        Method witch close window where is an output of the Whylog.
        """
        if not self.is_whylog_window_open():
            vim.command(':rightbelow split %s' % WhylogWindowsTypes['teacher'])
            vim.command(':setlocal buftype=nowrite')
            vim.command(':resize 100')
        self.output_window_context = OutputWindowContext(self)
        self.get_files_window_id(WhylogWindowsTypes['teacher'])

    def get_button_name(self):
        line_content = get_current_line()
        offset = get_col()
        return get_button_name(line_content, offset)

    def set_output(self, contents, line=None):
        """
        This method set content of the output window.
        """
        with self.output_window_context as output_buffer:
            output_buffer[:] = contents.split('\n')
            if line is not None:
                go_to_line(line)

    def set_window_writability(self, state):
        vim.command(':setlocal %s' % self.WINDOW_WRITEABILITY_STATE_DICT[state])

    def _get_output_window_id(self):
        for id_, window in enumerate(vim.windows):
            for name in WhylogWindowsTypes.values():
                if window.buffer.name.endswith(name):
                    return int(id_)+1
        return None

    def _get_output_buffer_id(self):
        for id_, buffer_ in enumerate(vim.buffers):
            if buffer_.name.endswith(os.path.join('', self.TEMPORARY_BUFFER_NAME)):
                return int(id_)
        return None

    def get_cursor_offset(self):
        """
        This method return offset -
        byte of the first char of the line
        where is cursor, when the method is called.
        """
        return int(vim.eval('line2byte(line("."))'))

    def get_input_window_file_name(self):
        """
        This method returns path of the window
        called as input window.
        """
        return self.output_window_context.origin_window_name

    def get_front_input(self):
        """
        This method return Front Input object of the line where cursor is,
        which is implemented in the whylog.front.utils.py file.
        """
        filename = get_current_filename()
        resource_location = LocallyAccessibleLogOpener(filename)
        cursor_position = self.get_cursor_offset()
        line_content = get_current_line()
        return FrontInput(cursor_position, line_content, resource_location)

    def close_output_window(self):
        """
        Same as name of the function. Closing window where is output of the Whylog.
        """
        self.go_to_output_window()
        vim.command(':q')

    def is_whylog_window_open(self):
        whylog_windows = WhylogWindowsTypes.values()
        for id_, window in enumerate(vim.windows):
            for name in whylog_windows:
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
        return get_current_window_id() == self._get_output_window_id()

    def close_teacher_window(self):
        id_ = self.get_files_window_id(WhylogWindowsTypes['teacher'])
        go_to_window(id_)
        vim.command(':q')

    def go_to_output_window(self):
        """
        After call of this function cursor
        is moving to the output window.
        """
        id_ = self._get_output_window_id()
        go_to_window(id_)

    def go_to_input_window(self):
        """
        After call of this function cursor
        is moving to the input window.
        """
        go_to_window(self.output_window_context.origin_window_id)
