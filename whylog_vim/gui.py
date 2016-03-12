import os.path
import vim
from whylog_vim.const import LOG_FILE, WHYLOG_OUTPUT


class Window():

    def __init__(self, gui, filename, window_id):
        self.filename = filename
        self.window_id = window_id


class OutputWindowContext(object):
    def __init__(self, gui):
        self.gui = gui
        self.origin_window_id = gui.get_current_window_id()

    def __enter__(self):
        self.gui.go_to_output_window()
        self.gui.set_window_writability(True)
        return vim.current.buffer

    def __exit__(self, type_, value, traceback):
        self.gui.set_window_writability(False)
        self.gui.go_to_window(self.origin_window_id)


class VimGUI(object): #(AbstractGUI):
    TEMPORARY_BUFFER_NAME = 'whylog_output'

    WINDOW_WRITEABILITY_STATE_DICT = {
        True: 'modifiable',
        False: 'nomodifiable',
    }

    def init_gui(self):
        self.set_input_window()
        self.create_output_window()

    def create_output_window(self):
        if not self._is_output_open():
            self._open_output_window()
        self.output_window_context = OutputWindowContext(self)

    def set_input_window(self):
        filename = self.get_current_filename()
        window_id = self.get_current_window_id()
        self.input_window = Window(self, filename, window_id)

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

    def close_output_window(self):
        self.go_to_output_window()
        vim.command(':q')

    def get_current_line(self):
        return vim.current.line

    def get_current_filename(self):
        return vim.current.buffer.name

    def get_current_window_id(self):
        return int(vim.eval('winnr()'))

    def get_cursor_offset(self):
        return int(vim.eval('line2byte(line("."))'))

    def get_cursor_position(self):
        line = vim.current.line
        range_ = vim.current.range
        assert range_.start == range_.end
        return range_.start

    def _is_output_open(self):
        return self._get_output_window_id() is not None

    def go_to_window(self, id_):
        assert id_ is not None
        vim.command('%dwincmd w' % id_)

    def triggered_from_output_window(self):
        return self.get_current_window_id() == self._get_output_window_id()

    def get_window_type(self):
        if self.triggered_from_output_window():
            return WHYLOG_OUTPUT
        else:
            return LOG_FILE

    def _normal(self, command):
        vim.command("normal %s" % (command,))

    def _go_to_line(self, line):
        vim.command(':%d' % (line,))

    def _go_to_offset(self, byte_offset):
        vim.command(':go %d' % (byte_offset,))

    def go_to_output_window(self):
        self.go_to_window(self._get_output_window_id())

    def go_to_input_window(self):
        self.go_to_window(self.input_window.window_id)

    def open_file_at_line(self, filename, line):
        vim.command(':edit %s' % (filename,))
        self._go_to_line(line)

    def open_cause_window(self, filename, offset):
        self.go_to_input_window()
        if not self.input_window.filename.endswith(filename):
            vim.command(':vsplit {}'.format(filename))
        self._go_to_offset(offset)

    def _open_output_window(self):
        vim.command(':rightbelow split %s' % self.TEMPORARY_BUFFER_NAME)
        vim.command(':setlocal buftype=nowrite')
        vim.command(':resize 10')
        vim.command(':setlocal nomodifiable')
        vim.command(':wincmd k')

    def set_output(self, contents, line=None):
        with self.output_window_context as output_buffer:
            output_buffer[:] = contents.split('\n')
            if line is not None:
                self._go_to_line(line)

    def set_window_writability(self, state):
        vim.command(':setlocal %s' % self.WINDOW_WRITEABILITY_STATE_DICT[state])


def get_gui_object():
    return VimGUI()
