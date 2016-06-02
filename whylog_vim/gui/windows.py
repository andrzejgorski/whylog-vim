import six

from whylog_vim.gui.exceptions import CannotFindWindowId, CannotSwitchToWindow
from whylog_vim.gui.files_manager import FilesManager
from whylog_vim.gui.vim_ui_wrapper import VimUIWrapper


class WindowContext(object):
    def __init__(self, modifiable):
        self.modifiable = modifiable

    def __enter__(self):
        VimUIWrapper.set_modifiable()
        return VimUIWrapper.get_buffer()

    def __exit__(self, type_, value, traceback):
        if not self.modifiable:
            VimUIWrapper.set_nomodifible()


class Window(object):
    def __init__(self, name, content, modifiable=False, splited_window_size=None):
        assert content
        self.context = WindowContext(modifiable)
        if splited_window_size is None:
            VimUIWrapper.open_file_at_window(name)
        else:
            VimUIWrapper.split_window(name)
            VimUIWrapper.resize(splited_window_size)
        VimUIWrapper.set_nowritable()
        self.set_content(content)
        self.set_modifiable(modifiable)
        self.name = name
        VimUIWrapper.set_file_type()

    def set_content(self, contents):
        with self.context as output_buffer:
            output_buffer[:] = contents

    def set_modifiable(self, modifiable):
        if modifiable:
            VimUIWrapper.set_modifiable()
        else:
            VimUIWrapper.set_nomodifible()

    def get_content(self):
        with self.context as output_buffer:
            return output_buffer[:]

    def get_window_id(self):
        window_id = FilesManager.get_files_window_id(self.name)
        if window_id:
            return window_id
        raise CannotFindWindowId(self.name)


def catch_key_error(function):
    def wrapper(window_type, *args, **kwargs):
        try:
            return function(window_type, *args, **kwargs)
        except KeyError:
            raise CannotSwitchToWindow(window_type)

    return wrapper


class WhylogWindowManager(object):
    def __init__(self):
        self.windows = dict()

    def create_window(self, window_type, content, modifiable=False, size=None):
        if not self.windows:
            self.origin_filename = VimUIWrapper.get_current_filename()
            self.origin_offset = VimUIWrapper.get_cursor_offset()
        self.windows[window_type] = Window(window_type, content, modifiable, size)
        for window in six.iterkeys(self.windows):
            if self.origin_filename.endswith(window):
                del self.windows[window]
                break

    @catch_key_error
    def get_window_content(self, window_type):
        return self.windows[window_type].get_content()

    @catch_key_error
    def go_to_window(self, window_type):
        VimUIWrapper.go_to_window(self.windows[window_type].get_window_id())

    def get_window_id(self, window_type):
        window = self.windows.get(window_type)
        if window is not None:
            return window.get_window_id()

    def close_window(self, window_type):
        FilesManager.go_to_file(self.origin_filename, self.origin_offset)
        self.go_to_window(window_type)
        VimUIWrapper.close_current_window()
        del self.windows[window_type]

    def are_windows_closed(self):
        for window in self.windows.keys():
            try:
                self.windows[window].get_window_id()
            except CannotFindWindowId:
                del self.windows[window]
        return not self.windows

    def get_windows_ids(self):
        return [window.get_window_id() for window in six.itervalues(self.windows)]

    @catch_key_error
    def set_content(self, window_type, content):
        self.windows[window_type].set_content(content)
