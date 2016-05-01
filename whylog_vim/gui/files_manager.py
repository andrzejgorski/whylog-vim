import vim
from whylog_vim.gui.vim_commander import VimCommander


class FilesManager(object):

    @staticmethod
    def get_files_window_id(file_name):
        for window_id, window in enumerate(vim.windows):
            if window.buffer.name.endswith(file_name):
                return window_id + 1
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
