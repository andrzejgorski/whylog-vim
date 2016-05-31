import six
from whylog_vim.consts import ReadMessages
from whylog_vim.input_reader import InputReader


class TeacherReader(object):
    @classmethod
    def read_single_line(cls, editor_input):
        if len(editor_input) == 1:
            return editor_input[0]
        else:
            six.print_(ReadMessages.TOO_MANY_LINES)

    @classmethod
    def read_primary_key_groups(cls, editor_input):
        line = cls.read_single_line(editor_input)
        if line:
            return InputReader.parse_primary_key_groups([line])
