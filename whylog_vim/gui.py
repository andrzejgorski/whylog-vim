from whylog.front.utils import FrontInput, LocallyAccessibleLogOpener

from mock import MagicMock, patch
import os.path
import vim


class OutputWindowContext(object):
    def __init__(self, gui):
        self.gui = gui
        self.origin_window_id = gui.get_current_window_id()
        self.origin_window_name = gui.get_current_filename()

    def __enter__(self):
        self.gui.go_to_output_window()
        self.gui.set_window_writability(True)
        return vim.current.buffer

    def __exit__(self, type_, value, traceback):
        self.gui.set_window_writability(False)
        self.gui.go_to_window(self.origin_window_id)


class VimEditor():
    """
    Class witch is an implementation of AbstractEditor.
    This class provide all communication between Whylog and Vim.
    """

    TEMPORARY_BUFFER_NAME = 'whylog_output'
    WINDOW_WRITEABILITY_STATE_DICT = {
        True: 'modifiable',
        False: 'nomodifiable',
    }

    def create_output_window(self):
        """
        Method witch close window where is an output of the Whylog.
        """
        if not self.is_output_open():
            self._open_output_window()
        self.output_window_context = OutputWindowContext(self)

    def set_output(self, contents, line=None):
        """
        This method set content of the output window.
        """
        with self.output_window_context as output_buffer:
            output_buffer[:] = contents.split('\n')
            if line is not None:
                self._go_to_line(line)

    def set_window_writability(self, state):
        vim.command(':setlocal %s' % self.WINDOW_WRITEABILITY_STATE_DICT[state])

    def _get_output_window_id(self):
        for id_, window in enumerate(vim.windows):
            if window.buffer.name.endswith(os.path.join('', self.TEMPORARY_BUFFER_NAME)):
                return int(id_)+1
        return None

    def _get_output_buffer_id(self):
        for id_, buffer_ in enumerate(vim.buffers):
            if buffer_.name.endswith(os.path.join('', self.TEMPORARY_BUFFER_NAME)):
                return int(id_)
        return None

    def get_current_line(self):
        """
        Method returns content of the line where cursor is.
        """
        return vim.current.line

    def get_current_filename(self):
        return vim.current.buffer.name

    def get_current_window_id(self):
        return int(vim.eval('winnr()'))

    def get_cursor_offset(self):
        """
        This method return offset -
        byte of the first char of the line
        where is cursor, when the method is called.
        """
        return int(vim.eval('line2byte(line("."))'))

    def get_cursor_position(self):
        line = vim.current.line
        range_ = vim.current.range
        assert range_.start == range_.end
        return range_.start

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
        filename = self.get_current_filename()
        resource_location = LocallyAccessibleLogOpener(filename)
        cursor_position = self.get_cursor_offset()
        line_content = self.get_current_line()

        return FrontInput(cursor_position, line_content, resource_location)

    def close_output_window(self):
        """
        Same as name of the function. Closing window where is output of the Whylog.
        """
        self.go_to_output_window()
        vim.command(':q')

    def is_output_open(self):
        return self._get_output_window_id() is not None

    def go_to_window(self, window_id):
        assert window_id is not None
        vim.command('%dwincmd w' % window_id)

    def cursor_at_output(self):
        return self.get_current_window_id() == self._get_output_window_id()

    def _normal(self, command):
        vim.command("normal %s" % (command,))

    def _go_to_line(self, line):
        vim.command(':%d' % (line,))

    def _go_to_offset(self, byte_offset):
        vim.command(':go %d' % (byte_offset,))

    def go_to_output_window(self):
        """
        After call of this function cursor
        is moving to the output window.
        """
        self.go_to_window(self._get_output_window_id())

    def go_to_input_window(self):
        """
        After call of this function cursor
        is moving to the input window.
        """
        self.go_to_window(self.output_window_context.origin_window_id)

    def open_file_at_line(self, filename, line):
        vim.command(':edit %s' % (filename,))
        self._go_to_line(line)

    def open_cause_window(self, filename, offset):
        """
        This function move cursor to the file,
        specified by filename variable.
        If the window of this file is not open it creates new window.
        """
        self.go_to_input_window()
        if not self.output_window_context.origin_window_name.endswith(filename):
            vim.command(':vsplit {}'.format(filename))
        self._go_to_offset(offset)

    def _open_output_window(self):
        vim.command(':rightbelow split %s' % self.TEMPORARY_BUFFER_NAME)
        vim.command(':setlocal buftype=nowrite')
        vim.command(':resize 10')
        vim.command(':setlocal nomodifiable')
        vim.command(':wincmd k')
