import vim

from whylog_vim.gui.vim_commander import VimCommander


class WindowContext(object):

    def __enter__(self):
        VimCommander.set_modifiable()
        return VimCommander.get_buffor()

    def __exit__(self, type_, value, traceback):
        VimCommander.set_nomodifible()


class Window(object):

    def __init__(self, name, content, modifiable, size=None):
        content = content or ''
        self.context = WindowContext()
        if size is None:
            VimCommander.open_file_at_window(name)
        else:
            VimCommander.split_window(name)
            VimCommander.resize(size)
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
        with self.context as output_buffer:
            return filter_comments(output_buffer[:])

    def _set_window_id(self):
        for window_id, window in enumerate(vim.windows):
            if window.buffer.name.endswith(self.name):
                self.window_id = window_id + 1


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
        return self.windows[window_type].get_content()

    def go_to_window(self, window_type):
        VimCommander.go_to_window(self.windows[window_type].window_id)

    def get_window_id(self, window_type):
        try:
            window_id = self.windows[window_type].window_id
        except KeyError:
            return None
        else:
            return window_id

    def close_window(self, window_type):
        self.go_to_window(window_type)
        VimCommander.close_current_window()
        del self.windows[window_type]

    def are_windows_closed(self):
        return not self.windows

    def get_windows_ids(self):
        return [window.window_id for window in self.windows.values()]

    def set_content(self, window_type, content):
        self.windows[window_type].set_output(content)
