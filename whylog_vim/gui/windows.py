import vim

from whylog_vim.consts import WindowTypes
from whylog_vim.gui.files_manager import FilesManager
from whylog_vim.gui.exceptions import (
    CannotCloseWindow, CannotGetWindowContent, CannotFindWindowId,
    CannotSetWindowContent, CannotSwitchToWindow)
from whylog_vim.gui.vim_commander import VimCommander


class WindowContext(object):

    def __enter__(self):
        VimCommander.set_modifiable()
        return VimCommander.get_buffor()

    def __exit__(self, type_, value, traceback):
        VimCommander.set_nomodifible()


class Window(object):

    def __init__(
            self,
            name,
            content=None,
            modifiable=False,
            splited_window_size=None
    ):
        content = content or ''
        self.context = WindowContext()
        if splited_window_size is None:
            VimCommander.open_file_at_window(name)
        else:
            VimCommander.split_window(name)
            VimCommander.resize(splited_window_size)
        VimCommander.set_nowritable()
        self.set_content(content)
        self.set_modifiable(modifiable)
        self.name = name
        VimCommander.set_file_type()

    def set_content(self, contents):
        with self.context as output_buffer:
            output_buffer[:] = contents.split('\n')

    def set_modifiable(self, modifiable):
        if modifiable:
            VimCommander.set_modifiable()
        else:
            VimCommander.set_nomodifible()

    def get_content(self):
        with self.context as output_buffer:
            return output_buffer[:]

    def get_window_id(self):
        window_id = FilesManager.get_files_window_id(self.name)
        if window_id:
            return window_id
        raise CannotFindWindowId(self.name)


class WhylogWindowManager(object):

    whylog_windows = [
        WindowTypes.QUERY,
        WindowTypes.TEACHER,
        WindowTypes.INPUT,
        WindowTypes.CASE,
    ]

    def __init__(self):
        self.windows = dict()

    def create_window(self, window_type, content, modifiable=False, size=None):
        self.windows[window_type] = Window(window_type, content, modifiable, size)

    def get_window_content(self, window_type):
        try:
            content = self.windows[window_type].get_content()
        except KeyError:
            raise CannotGetWindowContent(window_type)

    def go_to_window(self, window_type):
        try:
            VimCommander.go_to_window(self.windows[window_type].get_window_id())
        except KeyError:
            raise CannotSwitchToWindow(window_type)

    def get_window_id(self, window_type):
        try:
            window_id = self.windows[window_type].get_window_id()
        except KeyError:
            return None
        else:
            return window_id

    def close_window(self, window_type):
        try:
            self.go_to_window(window_type)
        except CannotSwitchToWindow:
            raise CannotCloseWindow(window_type)
        VimCommander.close_current_window()
        del self.windows[window_type]

    def are_windows_closed(self):
        return not self.windows

    def get_windows_ids(self):
        return [window.get_window_id() for window in self.windows.values()]

    def set_content(self, window_type, content):
        try:
            self.windows[window_type].set_content(content)
        except KeyError:
            CannotSetWindowContent(window_type)
