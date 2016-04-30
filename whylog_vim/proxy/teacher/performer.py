import re

from whylog.teacher import Teacher
from whylog.front.utils import FrontInput

from whylog_vim.output_formater.teacher_formater import TeacherOutput, OutputAgregator, get_log_types_message, get_primary_key_message, to_buttons, get_constraint_message

from whylog_vim.input_reader.teacher_reader import (
    ConstraintGroupLoader,
    ConstraintLoader,
    LogTypeLoader,
    NewLogTypeLoader,
    PrimaryKeyLoader,
    ParseParamLoader,
)
from whylog_vim.consts import ButtonsMetaConsts as BMC, EditorStates, Messages, WindowTypes

# TODO delete it
from whylog_vim.mocks import converter_returner, log_type_returner, constraint_returner
from whylog_vim.proxy.teacher.utils import parsers_ids
from whylog_vim.proxy.teacher.consts import ReadInputMetaKeys, Keys


class TeacherPerformer():

    def __init__(self, teacher_proxy, teacher, editor, main_proxy):
        self.teacher_proxy = teacher_proxy
        self.teacher = teacher
        self.editor = editor
        self.main_proxy = main_proxy
        self.output_formater = TeacherOutput(self)
        self.warnings = []

    def new_lesson(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(next(parsers_ids), front_input, effect=True)
        self.origin_file_name = self.editor.get_current_filename()

        # TODO Add consts dialoges
        print '### WHYLOG ### You added line as effect. Select cause and press <F4>.'

    def add_cause(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(next(parsers_ids) , front_input)
        self.editor.create_teacher_window()
        self.print_teacher()

    def print_teacher(self):
        self.raw_output = self.teacher.get_rule()
        output = self.output_formater.format_rule(self.raw_output)
        self.teacher_proxy.set_output(output)
        self.editor.set_teacher_output(output.get_content())
        self.editor.set_syntax_folding()
        self.main_proxy.set_state(EditorStates.TEACHER)

    def reprint_teacher(self, _=None):
        self.editor.create_teacher_window()
        self.print_teacher()
        return True

    def edit_content(self, line_id):
        default_content = self.raw_output.parsers[line_id].line_content
        self.editor.create_input_window(default_content)
        # TODO uncomment this funciton
        # self.teacher.remove_line(parser)
        meta_info = {ReadInputMetaKeys.PARSER: line_id}
        self.teacher_proxy._set_read_input_info(self.back_edit_content, meta_info)
        print 'edit_content executed with parser: %s' % line_id

    def back_edit_content(self, read_input_info):
        line_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        content = read_input_info.content
        front_input = FrontInput(0, content, None)
        self.teacher.add_line(line_id, front_input)
        print 'back_edit_content, %s' % content
        return True

    def copy_line(self, line_id):
        new_id = next(parsers_ids)
        self.teacher.add_line(new_id, self.teacher._lines[line_id])
        self.reprint_teacher()
        print 'copy_line executed with line_id: %s, new_id = %s ' % (line_id, new_id)

    def delete_line(self, line_id):
        self.teacher.remove_line(line_id)
        self.reprint_teacher()
        print 'delete_line executed with line_id: %s' % line_id

    def edit_regex_name(self, line_id):
        parser = self.raw_output.parsers[line_id]

        output = OutputAgregator()
        self.output_formater.parser.format_regexes_message(output, parser)
        default_content = parser.pattern_name
        self.editor.create_input_window(default_content, output.get_content())

        meta_info = {ReadInputMetaKeys.PARSER: line_id}
        self.teacher_proxy._set_read_input_info(self.back_edit_regex_name, meta_info)
        print 'edit_regex_name executed with line_id: %s' % line_id

    def back_edit_regex_name(self, read_input_info):
        line_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        regex_name = read_input_info.content
        # self.teacher.update_pattern_name(line_id, regex_name)
        print 'back_edit_regex_name %s ' % regex_name
        return True

    def edit_regex(self, line_id):
        parser = self.raw_output.parsers[line_id]

        message = [Messages.REGEX, parser.line_content]
        output = OutputAgregator()
        output.add_message(message)
        output.add(parser.pattern)
        self.editor.create_input_window(output.get_content())

        meta_info = {ReadInputMetaKeys.PARSER: line_id}
        self.teacher_proxy._set_read_input_info(self.back_edit_regex, meta_info)
        print 'edit_regex executed with line_id: %s' % line_id

    def back_edit_regex(self, read_input_info):
        line_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        # TODO parse input
        regex = read_input_info.content
        self.teacher.update_pattern(line_id, regex)
        print 'back_edit_regex %s ' % regex
        return True

    def guess_regex(self, line_id):
        self.teacher.guess_pattern(line_id)
        self.reprint_teacher()
        print 'guess_regex executed with line_id: %s' % line_id

    def edit_group(self, line_id, group_id):
        group = self.raw_output.parsers[line_id].groups[group_id]

        output = OutputAgregator()
        output.add_message([Messages.CONVERTER % group.content], WindowTypes.CASE)
        output.add(to_buttons(converter_returner()))
        self.editor.create_case_window(output.get_content())

        meta_info = {
            ReadInputMetaKeys.PARSER: line_id,
            ReadInputMetaKeys.GROUP: group_id,
        }
        loader = self.editor.get_button_name
        self.teacher_proxy._set_read_input_info(self.back_edit_group, meta_info, loader)
        print 'edit executed with parser: %s and group %s' % (line_id, group_id)

    def back_edit_group(self, read_input_info):
        line_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        group_id = read_input_info.meta_info[ReadInputMetaKeys.GROUP]
        converter = read_input_info.content
        if converter is not None:
            pass
            # self.teacher.set_converter(line_id, group_id, converter)
        return True

    def edit_log_type(self, line_id, log_type):
        parser = self.raw_output.parsers[line_id]

        output = OutputAgregator()
        output.add_message(get_log_types_message(parser), WindowTypes.CASE)
        self.output_formater.format_log_type(output, log_type_returner())
        self.editor.create_case_window(output.get_content())

        meta_info = {
            ReadInputMetaKeys.PARSER: line_id,
            ReadInputMetaKeys.CONTENT: output,
        }
        loader = LogTypeLoader(
            output,
            self.editor.get_line_number,
            self.teacher_proxy.set_return_function,
        )
        self.teacher_proxy._set_read_input_info(self.back_edit_log_type, meta_info, loader)
        print 'edit_log_type executed with line_id: %s' % line_id

    def back_edit_log_type(self, read_input_info):
        line_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        logtype = read_input_info.content
        if logtype is None:
            return False
        self.teacher.set_log_type(line_id, logtype)
        print 'back_edit_log_type %s ' % logtype.name
        print 'back_edit_log_type %s ' % logtype.name
        return True

    def new_log_type(self, read_input_info):
        line_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        parser = self.raw_output.parsers[line_id]

        output = OutputAgregator()
        output.add_message(get_log_types_message(parser), WindowTypes.INPUT)

        output.add(self.output_formater.get_log_type_template())
        self.editor.create_input_window(output.get_content())
        meta_info = {
            ReadInputMetaKeys.PARSER: line_id,
        }
        loader = NewLogTypeLoader(self.editor.get_input_content)
        self.teacher_proxy._set_read_input_info(self.back_new_log_type, meta_info, loader)
        return False

    def back_new_log_type(self, read_input_info):
        log_type = read_input_info.content
        # self.teacher.config.add_new_log_type(log_type)
        print log_type
        print log_type
        return True

    def edit_primary_key_groups(self, line_id, primary_key):
        parser = self.raw_output.parsers[line_id]

        output = OutputAgregator()
        output.add_message(get_primary_key_message(parser), WindowTypes.INPUT)

        output.add(self.output_formater.format_comma(parser.primary_key_groups))

        self.editor.create_input_window(output.get_content())

        meta_info = {
            ReadInputMetaKeys.PARSER: line_id,
        }
        loader = PrimaryKeyLoader(self.editor.get_input_content)
        self.teacher_proxy._set_read_input_info(self.back_edit_primary_key, meta_info, loader)
        print 'edit_primary_key_groups executed with line_id: %s' % line_id

    def back_edit_primary_key(self, read_input_info):
        line_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        groups = read_input_info.content
        # self.teacher.set_primary_key(line_id, groups)
        print groups
        print 'back_edit_primary_key %s ' % groups
        return True

    def add_constraint(self):
        # TODO add select window between teacher and input window
        parsers = self.raw_output.parsers.values()
        output = OutputAgregator()
        output.add_message([], WindowTypes.CASE)
        output.add(to_buttons(constraint_returner()))
        self.editor.create_case_window(output.get_content())

        loader = self.editor.get_button_name
        self.teacher_proxy._set_read_input_info(self.mid_add_constraint, {}, loader)
        print 'add_constraint executed'

    def mid_add_constraint(self, read_input_info):
        constraint_type = read_input_info.content
        output = OutputAgregator()
        parsers = self.raw_output.parsers.values()
        output.add_message(get_constraint_message(parsers))
        output.add(self.output_formater.get_constraint_template(constraint_type))
        self.editor.create_input_window(output.get_content())
        meta_info = {
            ReadInputMetaKeys.CONSTRAINT: constraint_type,
        }
        loader = ConstraintLoader(self.editor.get_input_content)

        self.teacher_proxy._set_read_input_info(self.back_add_constraint, meta_info, loader)
        return False

    def back_add_constraint(self, read_input_info):
        constraint = read_input_info.content
        print constraint
        # self.teacher.register_constraint(constraint)
        return True

    def edit_constraint(self, constraint):
        output = OutputAgregator()
        parsers = self.raw_output.parsers.values()
        output.add_message(get_constraint_message(parsers))
        self.output_formater.get_constraint_content(output, constraint)
        self.editor.create_input_window(output.get_content())
        meta_info = {
            ReadInputMetaKeys.CONSTRAINT: constraint,
        }
        loader = ConstraintLoader(self.editor.get_input_content)

        self.teacher_proxy._set_read_input_info(self.back_add_constraint, meta_info, loader)
        return False

    def back_add_constraint(self, read_input_info):
        constraint = read_input_info.content
        old_constraint = read_input_info.meta_info[ReadInputMetaKeys.CONSTRAINT]
        # self.teacher.delete_constraint(old_constraint)
        # self.teacher.register_constraint(constraint)
        return True

    def delete_constraint(self, constraint):
        self.teacher.remove_constraint(constraint)
        self.reprint_teacher()
        print 'delete_constraint executed with constraint %s' % constraint

    # TODO add buttons and implement funcitons:
    # 1. Delete param
    # 2. Delete group
    # Usunac constrainta dodac nowego

    def save(self):
        self.teacher.save()
        print 'save executed'

    def test_rule(self):
        if self.warnings:
            self.skip_to_warning()
        else:
            print 'Rule is correct.'

    def return_to_file(self):
        self.main_proxy.set_state(EditorStates.ADD_CAUSE)
        self.editor.go_to_file(self.origin_file_name, 1)
        self.editor.close_teacher_window()
        print 'return_to_file executed'

    def give_up_rule(self):
        self.editor.close_teacher_window()
        self.main_proxy.new_teacher()
        print 'give_up_rule executed'
