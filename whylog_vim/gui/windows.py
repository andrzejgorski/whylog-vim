from whylog_vim.gui.exceptions import CannotFindWindowId
from whylog_vim.gui.files_manager import FilesManager
from whylog_vim.gui.vim_ui_wrapper import VimUIWrapper


class WindowContext(object):
    def __enter__(self):
        VimUIWrapper.set_modifiable()
        return VimUIWrapper.get_buffor()

    def __exit__(self, type_, value, traceback):
        VimUIWrapper.set_nomodifible()


class Window(object):
    def __init__(self,
                 name,
                 content=None,
                 modifiable=False,
                 splited_window_size=None):
        content = content or ''
        self.context = WindowContext()
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
            output_buffer[:] = contents.split('\n')

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
