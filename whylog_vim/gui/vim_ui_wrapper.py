import vim


class VimUIWrapper(object):
    @classmethod
    def resize(cls, size):
        vim.command('resize %s' % size)

    @classmethod
    def set_file_type(cls):
        vim.command('setlocal filetype=whylog')

    @classmethod
    def get_column(cls):
        return int(vim.eval('col(".")'))

    @classmethod
    def get_current_window_id(cls):
        return int(vim.eval('winnr()'))

    @classmethod
    def normal(cls, command):
        vim.command("normal %s" % command)

    @classmethod
    def go_to_window(cls, window_id):
        assert window_id is not None
        vim.command('%dwincmd w' % window_id)

    @classmethod
    def split_window(cls, name=''):
        vim.command(':rightbelow split %s' % name)

    @classmethod
    def set_modifiable(cls):
        vim.command('setlocal modifiable')

    @classmethod
    def set_nomodifible(cls):
        vim.command('setlocal nomodifiable')

    @classmethod
    def open_file_at_window(cls, filename):
        vim.command(':e %s' % filename)

    @classmethod
    def set_nowritable(cls):
        vim.command('setlocal buftype=nowrite')

    @classmethod
    def close_current_window(cls):
        vim.command(':q')

    @classmethod
    def get_current_line(cls):
        return vim.current.line

    @classmethod
    def go_to_offset(cls, byte_offset):
        vim.command(':go %d' % byte_offset)

    @classmethod
    def get_line_offset(cls):
        return int(vim.eval('line2byte(line("."))'))

    @classmethod
    def set_syntax_folding(cls):
        vim.command(':set foldmethod=syntax')

    @classmethod
    def get_current_filename(cls):
        return vim.current.buffer.name

    @classmethod
    def get_line_number(cls):
        return int(vim.eval('line(".")'))

    @classmethod
    def get_cursor_offset(cls):
        return int(vim.eval('line2byte(line("."))+col(".")'))

    @classmethod
    def get_buffer(cls):
        return vim.current.buffer

    @classmethod
    def get_windows(cls):
        return vim.windows
