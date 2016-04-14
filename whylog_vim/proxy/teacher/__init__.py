import re

from whylog.teacher import Teacher
from whylog.front.utils import FrontInput, LocallyAccessibleLogOpener

from whylog_vim.consts import ButtonsMetaConsts as BMC
from whylog_vim.gui import (
    go_to_offset,
    normal,
    get_offset,
    get_line_number,
)
from whylog_vim.output_formater.teacher_formater import TeacherOutput, OutputAgregator

from whylog_vim.input_reader.teacher_reader import (
    get_button_name,
    parse_log_type,
    parse_primary_key_groups,
    parse_param,
    parse_constraint,
    parse_constraint_group,
)
# TODO delete it
from whylog_vim.gui import (
    set_syntax_folding,
    get_current_line,
    get_current_filename,
    resize,
    get_line_number,
)
from whylog_vim.consts import ButtonsMetaConsts as BMC
from whylog_vim.proxy.teacher.consts import TeacherProxyStates as States
from whylog_vim.proxy.teacher.performer import TeacherPerformer
from whylog_vim.proxy.teacher.utils import (
    ReadInputInfo,
)


class TeacherProxy():

    def __init__(self, teacher, editor, main_proxy):
        self.teacher_performer = TeacherPerformer(self, teacher, editor, main_proxy)
        self.editor = editor
        self.state = States.BEGIN
        self.buttons = {
            # TODO use consts here
            'copy_line': self.teacher_performer.copy_line,
            'delete_line': self.teacher_performer.delete_line,
            'guess_regex': self.teacher_performer.guess_regex,
            'add_constraint': self.teacher_performer.add_constraint,
            'delete_constraint': self.teacher_performer.delete_constraint,
            'add_param': self.teacher_performer.add_param,
            'save': self.teacher_performer.save,
            'test_rule': self.teacher_performer.test_rule,
            'return_to_file': self.teacher_performer.return_to_file,
            'give_up_rule': self.teacher_performer.give_up_rule,
        }

    def signal_1(self):
        if self.editor.cursor_at_teacher():
            if self.state == States.MAIN_WINDOW:
                self.action()
        elif self.editor.cursor_at_input() or self.editor.cursor_at_case():
            if self.state == States.INPUT:
                self._read_input()

    def signal_2(self):
        if not self.editor.cursor_at_output():
            if self.state == States.BEGIN:
                self.state = States.EFFECT_ADDED
                self.teacher_performer.new_lesson()
            elif self.state == States.EFFECT_ADDED:
                self.teacher_performer.add_cause()
            else:
                self._add_cause()

    def _read_input(self):
        self.read_input_info.load_input()
        return_function = self.read_input_info.return_function
        if return_function(self.read_input_info):
            self.editor.close_message_window()
            self.editor.change_to_teacher_window()
            self.teacher_performer.print_teacher()

            del self.read_input_info
            self._return_cursor_to_position()

    def _set_cursor_position(self):
        self._return_offset = get_offset()

    def set_output(self, output):
        self.output = output

    def set_main_state(self):
        self.state = States.MAIN_WINDOW

    def _set_read_input_info(self, function, meta_info=None, loader=None):
        self.read_input_info = ReadInputInfo(self, function, meta_info, loader)
        self.state = States.INPUT

    def action(self):
        self._set_cursor_position()
        line_number = get_line_number()
        meta = self.output.get_button_meta(line_number)
        try:
            func = meta[BMC.FUNCTION]
        except KeyError:
            pass
        else:
            del meta[BMC.FUNCTION]
            func(**meta)
            return

        try:
            name = self.editor.get_button_name()
            func = self.buttons[name]
        except KeyError:
            try:
                func = self.buttons[(name, tuple(meta.keys()))]
            except KeyError:
                # TODO add WhylogVIMException
                print ('Cannot execute "%s" with params %s, %s' %
                       (name, meta, tuple(meta.keys())))
            else:
                func(**meta)
        else:
            func(**meta)
        if self.state == States.MAIN_WINDOW:
            self._return_cursor_to_position()

    def _return_cursor_to_position(self):
        try:
            go_to_offset(self._return_offset)
        except Exception:
            # Can't go to the offset. Nothing to do.
            pass
        else:
            try:
                normal('zo')
            except Exception:
                # Fold opening error. Nothing to do.
                pass
