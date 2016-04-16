import re

from whylog.teacher import Teacher
from whylog.front.utils import FrontInput, LocallyAccessibleLogOpener

from whylog_vim.output_formater.teacher_formater import TeacherOutput, OutputAgregator

from whylog_vim.input_reader.teacher_reader import (
    ConstraintGroupLoader,
    ConstraintLoader,
    LogTypeLoader,
    NewLogTypeLoader,
    PrimaryKeyLoader,
    ParseParamLoader,
)
from whylog_vim.consts import ButtonsMetaConsts as BMC

# TODO delete it
from whylog_vim.mocks import converter_returner, log_type_returner, constraint_returner
from whylog_vim.proxy.teacher.utils import parsers_ids
from whylog_vim.proxy.teacher.consts import TeacherProxyStates as States, ReadInputMetaKeys, Keys


class TeacherPerformer():

    def __init__(self, teacher_proxy, teacher, editor, main_proxy):
        self.teacher_proxy = teacher_proxy
        self.teacher = teacher
        self.editor = editor
        self.main_proxy = main_proxy
        self.output_formater = TeacherOutput(self)

    def new_lesson(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(next(parsers_ids), front_input)
        self.origin_file_name = self.editor.get_current_filename()

        # TODO Add consts dialoges
        print '### WHYLOG ### You added line \'%s\' as effect. Select cause and press <F4>.' % front_input.line_content

    def add_cause(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(next(parsers_ids) , front_input)
        self.editor.create_teacher_window()
        self.print_teacher()

    def print_teacher(self):
        self.raw_output = self.teacher.get_rule()
        output = self.output_formater.format_rule(self.raw_output)
        self.teacher_proxy.set_output(output)
        self.editor.set_output(output.get_content())
        self.editor.set_syntax_folding()
        self.teacher_proxy.set_main_state()

    def _reprint_teacher(self):
        self.editor.change_to_teacher_window()
        self.print_teacher()

    def edit_content(self, parser_id):
        default_content = self.raw_output.parsers[parser_id].line_content
        self.editor.create_input_window(default_content)
        # TODO uncomment this funciton
        # self.teacher.remove_line(parser)
        meta_info = {ReadInputMetaKeys.PARSER: parser_id}
        self.teacher_proxy._set_read_input_info(self.back_edit_content, meta_info)
        print 'edit_content executed with parser: %s' % parser_id

    def back_edit_content(self, read_input_info):
        parser_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        content = read_input_info.content
        front_input = FrontInput(0, content, None)
        self.teacher.add_line(parser_id, front_input)
        print 'back_edit_content, %s' % content
        return True

    def copy_line(self, parser_id):
        new_id = next(parsers_ids)
        self.teacher.add_line(new_id, self.teacher._lines[parser_id])
        self._reprint_teacher()
        print 'copy_line executed with parser_id: %s, new_id = %s ' % (parser_id, new_id)

    def delete_line(self, parser_id):
        self.teacher.remove_line(parser_id)
        self._reprint_teacher()
        print 'delete_line executed with parser_id: %s' % parser_id

    def edit_regex_name(self, parser_id):
        parser = self.raw_output.parsers[parser_id]

        output = OutputAgregator()
        self.output_formater.parser.format_regexes_message(output, parser)
        default_content = parser.pattern_name
        self.editor.create_input_window(default_content, output.get_content())

        meta_info = {ReadInputMetaKeys.PARSER: parser_id}
        self.teacher_proxy._set_read_input_info(self.back_edit_regex_name, meta_info)
        print 'edit_regex_name executed with parser_id: %s' % parser_id

    def back_edit_regex_name(self, read_input_info):
        parser_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        regex_name = read_input_info.content
        # self.teacher.update_pattern_name(parser_id, regex_name)
        print 'back_edit_regex_name %s ' % regex_name
        return True

    def edit_regex(self, parser_id):
        parser = self.raw_output.parsers[parser_id]

        default_content = parser.pattern
        message = parser.line_content
        self.editor.create_input_window(default_content, message)

        meta_info = {ReadInputMetaKeys.PARSER: parser_id}
        self.teacher_proxy._set_read_input_info(self.back_edit_regex, meta_info)
        print 'edit_regex executed with parser_id: %s' % parser_id

    def back_edit_regex(self, read_input_info):
        parser_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        # TODO parse input
        regex = read_input_info.content
        self.teacher.update_pattern(parser_id, regex)
        print 'back_edit_regex %s ' % regex
        return True

    def guess_regex(self, parser_id):
        self.teacher.guess_pattern(parser_id)
        self._reprint_teacher()
        print 'guess_regex executed with parser_id: %s' % parser_id

    def edit_group(self, parser_id, group_id):
        group = self.raw_output.parsers[parser_id].groups[group_id]

        default_content = self.output_formater.to_buttons(converter_returner())
        message = self.output_formater.format_match(group)
        self.editor.create_case_window(default_content, message)

        meta_info = {
            ReadInputMetaKeys.PARSER: parser_id,
            ReadInputMetaKeys.GROUP: group_id,
        }
        loader = self.editor.get_button_name
        self.teacher_proxy._set_read_input_info(self.back_edit_group, meta_info, loader)
        print 'edit executed with parser: %s and group %s' % (parser_id, group_id)

    def back_edit_group(self, read_input_info):
        parser_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        group_id = read_input_info.meta_info[ReadInputMetaKeys.GROUP]
        converter = read_input_info.content
        # self.teacher.set_converter(parser_id, group_id, converter)
        return True

    def edit_log_type(self, parser_id, log_type):
        parser = self.raw_output.parsers[parser_id]

        log_types_menu = self.output_formater.format_log_type(log_type_returner())
        output = OutputAgregator()
        self.output_formater.parser.format_line_headers(output, parser)
        self.editor.create_case_window(log_types_menu.get_content(), output.get_content())

        meta_info = {
            ReadInputMetaKeys.PARSER: parser_id,
            ReadInputMetaKeys.CONTENT: log_types_menu,
        }
        loader = LogTypeLoader(log_types_menu, self.editor.get_line_number)
        self.teacher_proxy._set_read_input_info(self.back_edit_log_type, meta_info, loader)
        print 'edit_log_type executed with parser_id: %s' % parser_id

    def back_edit_log_type(self, read_input_info):
        parser_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        content = read_input_info.content
        if content == BMC.BUTTON:
            # new log type
            parser = self.raw_output.parsers[parser_id]

            log_types_menu = self.output_formater.get_log_type_template()
            output = OutputAgregator()
            self.output_formater.parser.format_line_headers(output, parser)
            self.editor.create_input_window(log_types_menu, output.get_content())
            meta_info = {
                ReadInputMetaKeys.PARSER: parser_id,
            }
            loader = NewLogTypeLoader(self.editor.get_input_content)
            self.teacher_proxy._set_read_input_info(self.back_new_log_type, meta_info, loader)
            return False
        else:
            # content is logtype
            self.teacher.set_log_type(parser_id, content)
            print 'back_edit_log_type %s ' % content._name
            print 'back_edit_log_type %s ' % content._name
            return True

    def back_new_log_type(self, read_input_info):
        log_type = read_input_info.content
        # self.teacher.config.add_new_log_type(log_type)
        print log_type
        return True

    def edit_primary_key_groups(self, parser_id, primary_key):
        parser = self.raw_output.parsers[parser_id]

        defaut_content = self.output_formater.format_comma(parser.primary_key_groups)
        output = OutputAgregator()
        self.output_formater.parser.format_line_headers(output, parser)
        self.output_formater.parser.format_regexes_message(output, parser)

        self.editor.create_input_window(defaut_content, output.get_content())

        meta_info = {
            ReadInputMetaKeys.PARSER: parser_id,
        }
        loader = PrimaryKeyLoader(self.editor.get_input_content)
        self.teacher_proxy._set_read_input_info(self.back_edit_primary_key, meta_info, loader)
        print 'edit_primary_key_groups executed with parser_id: %s' % parser_id

    def back_edit_primary_key(self, read_input_info):
        parser_id = read_input_info.meta_info[ReadInputMetaKeys.PARSER]
        groups = read_input_info.content
        # self.teacher.set_primary_key(parser_id, groups)
        print groups
        print 'back_edit_primary_key %s ' % groups
        return True

    def add_constraint(self):
        # TODO add select window between teacher and input window
        output = OutputAgregator()
        parsers = self.raw_output.parsers.values()
        self.output_formater.parser.format_constraint_message(output, parsers)
        content = self.output_formater.to_buttons(constraint_returner())
        self.editor.create_case_window(content, output.get_content())

        loader = self.editor.get_button_name
        self.teacher_proxy._set_read_input_info(self.mid_add_constraint, {}, loader)
        print 'add_constraint executed'

    def mid_add_constraint(self, read_input_info):
        constraint_type = read_input_info.content
        print constraint_type
        output = OutputAgregator()
        parsers = self.raw_output.parsers.values()
        self.output_formater.parser.format_constraint_message(output, parsers)
        content = self.output_formater.get_constraint_template(constraint_type)
        self.editor.create_input_window(content, output.get_content())
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

    def delete_constraint(self, constraint):
        self.teacher.remove_constraint(constraint)
        self._reprint_teacher()
        print 'delete_constraint executed with constraint %s' % constraint

    def add_param(self, constraint):
        output = OutputAgregator()

        content = self.output_formater.format_param(Keys.PARAM_KEY, Keys.PARAM_VALUE)
        self.output_formater.constraint.format_constraint(output, constraint)

        self.editor.create_input_window(content, output.get_content())
        meta_info = {ReadInputMetaKeys.CONSTRAINT: constraint}
        loader = ParseParamLoader(self.editor.get_input_content)
        self.teacher_proxy._set_read_input_info(self.back_add_param, meta_info, loader)
        print 'add_param executed with constraint %s' % constraint

    def back_add_param(self, read_input_info):
        param = read_input_info.content
        constraint = read_input_info.meta_info[ReadInputMetaKeys.CONSTRAINT]
        # self.teacher.register_constraint(constraint)
        print 'back_add_param %s ' % param
        return True

    def edit_constraint_group(self, constraint, constraint_group):
        output = OutputAgregator()
        parsers = self.raw_output.parsers.values()
        self.output_formater.constraint.format_constraint(output, constraint)
        self.output_formater.parser.format_constraint_message(output, parsers)
        content = self.output_formater.format_comma(constraint_group)
        self.editor.create_input_window(content, output.get_content())

        meta_info = {ReadInputMetaKeys.CONSTRAINT: constraint, ReadInputMetaKeys.GROUP: constraint_group}
        loader = ConstraintGroupLoader(self.editor.get_input_content)
        self.teacher_proxy._set_read_input_info(self.back_edit_constraint_group, meta_info)
        print 'edit_constraint executed with %s and %s ' % (constraint, constraint_group)

    def back_edit_constraint_group(self, read_input_info):
        group_constraint = read_input_info.content
        # TODO parse group
        constraint = read_input_info.meta_info[ReadInputMetaKeys.CONSTRAINT]
        constraint_group = read_input_info.meta_info[ReadInputMetaKeys.GROUP]
        # TODO nowy constraint
        # self.teacher.update_constraint_group(constraint, group_id, group_content)
        print 'back_edit_constraint_group %s' % constraint_group
        return True

    def edit_constraint_param(self, constraint, param):
        output = OutputAgregator()
        content = self.output_formater.format_param(param, constraint.params[param])
        self.output_formater.constraint.format_constraint(output, constraint)
        self.editor.create_input_window(content, output.get_content())

        meta_info = {
            ReadInputMetaKeys.CONSTRAINT: constraint,
            ReadInputMetaKeys.PARAM: param
        }
        loader = ParseParamLoader(self.editor.get_input_content)
        self.teacher_proxy._set_read_input_info(self.back_edit_constraint_param, meta_info, loader)
        print 'edit_constraint_param executed with %s and %s' % (constraint, param)

    def back_edit_constraint_param(self, read_input_info):
        param = read_input_info.content
        constraint = read_input_info.meta_info[ReadInputMetaKeys.CONSTRAINT]
        # self.teacher.update_constraint_param(constraint, param, param_content)
        print 'back_edit_constraint_param %s' % param
        return True

    # TODO add buttons and implement funcitons:
    # 1. Delete param
    # 2. Delete group
    # Usunac constrainta dodac nowego

    def save(self):
        self.teacher.save()
        print 'save executed'

    # TODO check rule
    def test_rule(self):
        # TODO ?? test_rule
        print 'test rule executed'

    def return_to_file(self):
        self.editor.go_to_file(self.origin_file_name, 1)
        self.editor.close_teacher_window()
        print 'return_to_file executed'

    def give_up_rule(self):
        self.editor.close_output_window()
        self.main_proxy.new_teacher()
        print 'give_up_rule executed'
