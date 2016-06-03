from functools import partial

from whylog import FrontInput
from whylog.constraints.constraint_manager import ConstraintRegistry
from whylog_vim.input_reader.teacher_reader import TeacherReader
from whylog_vim.output_formater.input_windows_messages import InputMessages
from whylog_vim.input_reader import InputReader, ConstraintReader
from whylog_vim.consts import EditorStates


class MenuHandler(object):
    def edit_line_content(self, parser):
        output = InputMessages.get_edit_line_message(parser.line_content)
        is_effect = self.rule.effect_id == parser.line_id
        self.main_proxy.create_input_window(output.get_content())
        self.read_function = partial(self.back_after_edit_line_content, parser, is_effect)

    def back_after_edit_line_content(self, parser, is_effect):
        content = TeacherReader.read_single_line(self.editor.get_input_content())
        if content:
            front_input = FrontInput(None, content, None)
            self.teacher.add_line(parser.line_id, front_input, is_effect)
            return True
        return False

    def edit_regex(self, parser):
        output = InputMessages.get_edit_regex_message(parser.line_content, parser.pattern)
        self.main_proxy.create_input_window(output.get_content())
        self.read_function = partial(self.back_after_edit_regex, parser)

    def back_after_edit_regex(self, parser):
        content = TeacherReader.read_single_line(self.editor.get_input_content())
        if content:
            self.teacher.update_pattern(parser.line_id, content)
            return True
        return False

    def delete_parser(self, parser):
        self.teacher.remove_line(parser.line_id)
        self.print_teacher()

    def edit_log_type(self, parser):
        log_types = self.config.get_all_log_types()
        self.output = InputMessages.get_case_log_types_parser(
            parser, log_types, partial(self.set_parser_log_type, parser)
        )
        self.main_proxy.create_case_window(self.output.get_content())
        self.read_function = self.call_button

    def set_parser_log_type(self, parser, log_type):
        self.teacher.set_log_type(parser.line_id, log_type.name)
        return True

    def call_button(self):
        return self.output.call_button(self.editor.get_line_number())

    def edit_primary_key_groups(self, parser):
        self.output = InputMessages.get_primary_key_message(parser)
        self.main_proxy.create_input_window(self.output.get_content())
        self.read_function = partial(self.back_after_edit_primary_key_groups, parser)

    def back_after_edit_primary_key_groups(self, parser):
        primary_keys = TeacherReader.read_primary_key_groups(self.editor.get_input_content())
        self.teacher.set_primary_key(parser.line_id, primary_keys)
        return True

    def add_constraint(self):
        self.output = InputMessages.select_constraint(self.rule.parsers.values())
        self.main_proxy.create_case_window(self.output.get_content())
        self.read_function = self.write_constraint

    def write_constraint(self):
        button_name = self.editor.get_button_name()
        constraints = ConstraintRegistry.CONSTRAINTS.keys()
        if button_name in constraints:
            self.output = InputMessages.add_constraint(self.rule.parsers.values(), button_name)
            self.main_proxy.create_input_window(self.output.get_content())
            self.read_function = self.read_constraint
        else:
            six.print_('Wrong name')
        return False

    def read_constraint(self):
        constraint = ConstraintReader.create_constraint(self.editor.get_input_content())
        self.teacher.register_constraint(self.get_next_constraints_id(), constraint)
        return True

    def edit_constraint(self, constraint):
        self.teacher.remove_constraint(constraint.id_)
        self.output = InputMessages.add_constraint(self.rule.parsers.values(), constraint.type)
        self.main_proxy.create_input_window(self.output.get_content())
        self.read_function = self.read_constraint

    def delete_constraint(self, constraint):
        self.teacher.remove_constraint(constraint.id_)
        self.print_teacher()

    def edit_converter(self, parser, group):
        match = self.rule.parsers[parser.id_].groups[group].content
        self.output = InputMessages.get_converters(match)
        self.main_proxy.create_case_window(self.output.get_content())
        self.read_function = partial(self.set_converter, parser, group)

    def set_converter(self, parser, group):
        converter = self.editor.get_button_name()
        self.teacher.set_converter(parser.id_, group, converter)
        return True

    def abandon_rule(self):
        self.main_proxy.new_teacher()
        self.editor.close_teacher_window()

    def return_to_file(self):
        self.main_proxy.set_state(EditorStates.ADD_CAUSE)
        self.editor.close_teacher_window()

    def save(self):
        self.teacher.save()
        self.main_proxy.new_teacher()
        self.editor.close_teacher_window()
