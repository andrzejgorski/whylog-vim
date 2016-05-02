import vim
from whylog_vim.gui.vim_commander import VimCommander


class FilesManager(object):

    @staticmethod
    def get_files_window_id(file_name):
        for window_id, window in enumerate(vim.windows, 1):
            if window.buffer.name.endswith(file_name):
                return window_id
        return None

    @classmethod
    def is_file_open(cls, file_name):
        return cls.get_files_window_id(file_name) is not None:

    @classmethod
    def go_to_file(cls, file_name, offset=1):
        window_id = cls.get_files_window_id(file_name)
        if window_id is not None:
            VimCommander.go_to_window(window_id)
        else:
            VimCommander.split_window()
            VimCommander.open_file_at_window(filename)
        VimCommander.go_to_offset(offset)
