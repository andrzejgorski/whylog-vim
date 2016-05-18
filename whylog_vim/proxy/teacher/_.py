import re

from whylog_vim.input_reader.teacher_reader import (
    get_button_name,
    parse_log_type,
    parse_primary_key_groups,
    parse_param,
    parse_constraint,
    parse_constraint_group,
)
from whylog_vim.consts import ButtonsMetaConsts as BMC, EditorStates
from whylog_vim.proxy.teacher.exceptions import CannotGoToPosition
from whylog_vim.proxy.teacher.consts import ButtonsNames
from whylog_vim.proxy.teacher.performer import TeacherPerformer
from whylog_vim.proxy.teacher.utils import ReadInputInfo


class TeacherProxy():

    def __init__(self, teacher, editor, main_proxy):
        self.performer = TeacherPerformer(self, teacher, editor, main_proxy)
        self.editor = editor
        self.buttons = {
            ButtonsNames.COPY_LINE: self.performer.copy_line,
            ButtonsNames.DELETE_LINE: self.performer.delete_line,
            ButtonsNames.GUESS_REGEX: self.performer.guess_regex,
            ButtonsNames.ADD_CONSTRAINT: self.performer.add_constraint,
            ButtonsNames.DELETE_CONSTRAINT: self.performer.delete_constraint,
            ButtonsNames.SAVE: self.performer.save,
            ButtonsNames.TEST_RULE: self.performer.test_rule,
            ButtonsNames.RETURN_TO_FILE: self.performer.return_to_file,
            ButtonsNames.ABANDON_RULE: self.performer.give_up_rule,
        }
        self.main_proxy = main_proxy

    def new_lesson(self):
        self.performer.new_lesson()

    def add_cause(self):
        self.performer.add_cause()

    def read_input(self):
        self.read_input_info.load_input()
        return_function = self.read_input_info.return_function
        if return_function(self.read_input_info):
            self.editor.create_teacher_window()
            self.performer.print_teacher()

            del self.read_input_info
            self._return_cursor_to_position()

    def set_return_function(self, function):
        self.read_input_info.return_function = function

    def _set_cursor_position(self):
        self._return_offset = self.editor.get_offset()

    def set_output(self, output):
        self.output = output

    def _set_read_input_info(self, function, meta_info=None, loader=None):
        self.read_input_info = ReadInputInfo(self, function, meta_info, loader)
        self.main_proxy.set_state(EditorStates.TEACHER_INPUT)

    def handle_menu_signal(self):
        self._set_cursor_position()
        line_number = self.editor.get_line_number()
        meta = self.output.get_button_meta(line_number)
        try:
            func = meta[BMC.FUNCTION]
        except KeyError:
            try:
                func = self.buttons[self.editor.get_button_name()]
            except KeyError:
                print 'This line is not editable'
            else:
                func(**meta)
        else:
            del meta[BMC.FUNCTION]
            func(**meta)

        if self.main_proxy.get_state() == EditorStates.TEACHER:
            self._return_cursor_to_position()

    def _return_cursor_to_position(self):
        try:
           self.editor.go_to_offset(self._return_offset)
        except Exception:
            raise CannotGoToPosition(self._return_offset)
        try:
            self.editor.open_fold()
        except Exception:
            # Fold opening error. Nothing to do.
            pass
