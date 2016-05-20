try:
    import vim.error
except:
    import vim

    class error(Exception):
        pass

    vim.error = error

import six
from functools import partial

from whylog import FrontInput
from whylog_vim.consts import EditorStates, Messages, ReadMessages
from whylog_vim.output_formater.teacher_formater import TeacherFormater
from whylog_vim.proxy.teacher.utils import get_next_parser_id
from whylog_vim.proxy.teacher.exceptions import CannotGoToPosition


def print_teacher(function):
    def wrapper(self, *agrs, **kwargs):
        function(self, *args, **kwargs)
        self.print_teacher()

    return wrapper


class TeacherProxy(object):
    def __init__(self, teacher, editor, main_proxy):
        self.teacher = teacher
        self.editor = editor
        self.main_proxy = main_proxy
        self.formater = TeacherFormater(self)

    def new_lesson(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(get_next_parser_id(), front_input, effect=True)
        self.origin_file_name = self.editor.get_current_filename()
        six.print_(Messages.ADDED_EFFECT)

    def add_cause(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(get_next_parser_id(), front_input)
        self.print_teacher()

    def handle_menu_signal(self):
        self._set_cursor_position()
        self.output.call_button(self.editor.get_line_number())
        if self.main_proxy.get_state() == EditorStates.TEACHER:
            self._return_cursor_to_position()

    def read_input(self):
        if self.read_function():
            self.print_teacher()
            self._return_cursor_to_position()

    def print_teacher(self):
        self.rule = self.teacher.get_rule()
        self.output = self.formater.format_rule(self.rule, None)
        # here should be the result from validate method of Teacher
        self.editor.create_teacher_window(self.output.get_content())
        self.editor.set_syntax_folding()
        self.main_proxy.set_state(EditorStates.TEACHER)

    def _set_cursor_position(self):
        self._return_offset = self.editor.get_line_offset()

    def _return_cursor_to_position(self):
        try:
            self.editor.go_to_offset(self._return_offset)
        except vim.error:
            raise CannotGoToPosition(self._return_offset)
        try:
            self.editor.open_fold()
        except Exception:
            # tryied to open fold but cannot.
            pass

    def edit_line_content(self, parser_id):
        old_line_content = [self.rule.parsers[parser_id].line_content]
        self.main_proxy.create_input_window(old_line_content)
        self.read_function = partial(self.back_edit_line_content, parser_id)

    def back_edit_line_content(self, parser_id):
        content = self.editor.get_input_content()
        if len(content) == 1:
            front_input = FrontInput(None, content[0], None)
            self.teacher.add_line(parser_id, front_input)
            return True
        else:
            six.print_(ReadMessages.TOO_MANY_LINES)
            return False

    def delete_parser(self, parser_id):
        pass

    def edit_regex(self, parser_id):
        pass

    def guess_regex(self, parser_id):
        pass

    def edit_converter(self, parser_id, group):
        pass

    def edit_log_type(self, parser_id):
        pass

    def edit_primary_key_groups(self, parser):
        pass

    def add_constraint(self, constraint):
        pass

    def delete_constraint(self, constraint):
        pass
