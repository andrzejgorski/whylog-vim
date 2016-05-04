import vim


class VimCommander(object):

    @staticmethod
    def resize(size):
        vim.command('resize %s' % size)

    @staticmethod
    def set_file_type():
        vim.command('setlocal filetype=whylog')

    @staticmethod
    def get_column():
        return int(vim.eval('col(".")'))

    @staticmethod
    def get_current_window_id():
        return int(vim.eval('winnr()'))

    @staticmethod
    def normal(command):
        vim.command("normal %s" % command)

    @staticmethod
    def go_to_window(window_id):
        assert window_id is not None
        vim.command('%dwincmd w' % window_id)

    @staticmethod
    def split_window(name=None):
        name = name or ''
        vim.command(':rightbelow split %s' % name)

    @staticmethod
    def set_modifiable():
        vim.command('setlocal modifiable')

    @staticmethod
    def set_nomodifible():
        vim.command('setlocal nomodifiable')

    @staticmethod
    def open_file_at_window(filename):
        vim.command(':e %s' % filename)

    @staticmethod
    def set_nowritable():
        vim.command('setlocal buftype=nowrite')

    @staticmethod
    def close_current_window():
        vim.command(':q')

    @staticmethod
    def get_current_line():
        return vim.current.line

    @staticmethod
    def go_to_offset(byte_offset):
        vim.command(':go %d' % byte_offset)

    @staticmethod
    def get_cursor_offset():
        return int(vim.eval('line2byte(line("."))'))

    @staticmethod
    def set_syntax_folding():
        vim.command(':set foldmethod=syntax')

    @staticmethod
    def get_current_filename():
        return vim.current.buffer.name

    @staticmethod
    def get_line_number():
        return int(vim.eval('line(".")'))

    @staticmethod
    def get_offset():
        return int(vim.eval('line2byte(line("."))+col(".")'))

    @staticmethod
    def get_buffor():
        return vim.current.buffer
