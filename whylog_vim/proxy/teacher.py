import re

from whylog.teacher import Teacher
from whylog.front.utils import FrontInput, LocallyAccessibleLogOpener

from whylog_vim.output_formater.teacher_formater import TeacherOutput, OutputAgregator
from whylog_vim.input_reader.teacher_reader import get_button_name
from whylog_vim.gui import set_syntax_folding, get_line_number, get_current_line, go_to_offset, get_current_filename, resize, go_to_offset, normal, get_offset
from whylog_vim.consts import ButtonsMetaConsts as BMC, get_constraint_template


# TODO move this function to utils file
def naturals_generator():
    i = 0
    while True:
        yield i
        i += 1


parsers_ids = naturals_generator()


# TODO add error message.


# TODO move it to the consts file
INPUT = 'input'
EFFECT_ADDED = 'efect added'
BEGIN = 'begin'
NORMAL = 'normal'
FUNCTION = 'function'
CHECK_FUNCTION = 'check_function'
PARSER = 'parser'
GROUP = 'group'
CONSTRAINT = 'constraint'
PARAM = 'param'
PARAM_KEY = '<param_key>'
PARAM_VALUE = '<param_value>'


# TODO Move this function to teacher utils file
class ReadInputInfo():

    def __init__(self, function, meta_info=None):
        self.function=function
        self.meta_info=meta_info

    def set_content(self, content):
        self.content = content


# TODO add lines_button parsed
# TODO add docsstrings


class TeacherProxy():

    def __init__(self, editor, teacher, proxy):
        self.editor = editor
        self.teacher = teacher
        self.output_formater = TeacherOutput()
        self._prepare_buttons()
        self.main_proxy = proxy
        self._state = BEGIN

    def _press_button(self):
        self._set_cursor_position()
        name = self.editor.get_button_name()
        meta = self.output.get_button_meta(get_line_number())
        try:
            func = self.buttons[name]
        except KeyError:
            try:
                func = self.buttons[(name, tuple(meta.keys()))]
            except KeyError:
                # TODO add WhylogVIMException
                print 'Cannot execute "%s" with params %s, %s' % (name, meta, tuple(meta.keys()))
                print '%s' % self.buttons.keys()
            else:
                self._return_info = {}
                func(**meta)
        else:
            self._return_info = {}
            func(**meta)
        if self._state == NORMAL:
            self._return_cursor_to_position()

    def _warning(self, message):
        print 'Warning! % s' % message

    def _read_input(self):
        self.read_input_info.set_content(self.editor.get_input_content())
        function = self.read_input_info.function
        function(self.read_input_info)

        self.editor.close_message_window()
        self.editor.change_to_teacher_window()
        self._print_teacher()
        self._return_cursor_to_position()

        del self.read_input_info
        self._return_cursor_to_position()

    def _set_cursor_position(self):
        self._return_offset = get_offset()

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

    def signal_1(self):
        if self.editor.cursor_at_teacher():
            if self._state == NORMAL:
                self._press_button()
            # self.editor.go_to_input_window()
        elif self.editor.cursor_at_input():
            if self._state == INPUT:
                self._read_input()

    def signal_2(self):
        if not self.editor.cursor_at_output():
            if self._state == BEGIN:
                self._new_lesson()
            elif self._state == EFFECT_ADDED:
                self._add_cause()
            else:
                self._add_cause()

    def _new_lesson(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(next(parsers_ids), front_input)
        self.origin_file_name = get_current_filename()

        self._state = EFFECT_ADDED
        # TODO Add consts dialoges
        print '### WHYLOG ### You added line {} as effect. Select cause and press <F4>.'

    def _add_cause(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(next(parsers_ids) , front_input)
        self.editor.create_teacher_window()
        self._print_teacher()

    def _print_teacher(self):
        self.raw_output = self.teacher.get_rule()
        self.output = self.output_formater.format_rule(self.raw_output)
        self.editor.set_output(self.output.get_content())
        set_syntax_folding()
        self._state = NORMAL

    def _reprint_teacher(self):
        self.editor.change_to_teacher_window()
        self._print_teacher()

    def close(self):
        self.editor.close_output_window()

    # Teacher buttons
    def _prepare_buttons(self):
        # TODO refactor
        self.buttons = {
            'edit_content': self.edit_content,
            'copy_line': self.copy_line,
            'delete_line': self.delete_line,
            'edit_regex_name': self.edit_regex_name,
            'edit_regex': self.edit_regex,
            'guess_regex': self.guess_regex,
            ('edit', (BMC.GROUP, BMC.PARSER)): self.edit_group,
            ('edit', (BMC.LOG_TYPE, BMC.PARSER)): self.edit_log_type,
            'new_log_type': self.new_log_type,
            ('edit', (BMC.PRIMARY_KEY, BMC.PARSER)): self.edit_primary_key_groups,
            'add_constraint': self.add_constraint,
            'delete_constraint': self.delete_constraint,
            'add_param': self.add_param,
            ('edit', (BMC.CONSTRAINT_GROUP, BMC.CONSTRAINT)): self.edit_constraint_group,
            ('edit', (BMC.PARAM, BMC.CONSTRAINT)): self.edit_constraint_param,
            'save': self.save,
            'test_rule': self.test_rule,
            'return_to_file': self.return_to_file,
            'give_up_rule': self.give_up_rule,
        }

    def _set_read_input_info(self, function, meta_info):
        self.read_input_info = ReadInputInfo(function, meta_info)
        self._state = INPUT

    def edit_content(self, parser_id):
        default_content = self.raw_output.parsers[parser_id].line_content
        self.editor.create_input_window(default_content)
        # TODO uncomment this funciton
        # self.teacher.remove_line(parser)
        meta_info = {PARSER: parser_id}
        self._set_read_input_info(self.back_edit_content, meta_info)
        print 'edit_content executed with parser: %s' % parser_id

    def back_edit_content(self, read_input_info):
        parser_id = read_input_info.meta_info[PARSER]
        # TODO parser input
        content = read_input_info.content
        front_input = FrontInput(0, content, None)
        self.teacher.add_line(parser_id, front_input)
        print 'back_edit_content, %s' % content

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

        meta_info = {PARSER: parser_id}
        self._set_read_input_info(self.back_edit_regex_name, meta_info)
        print 'edit_regex_name executed with parser_id: %s' % parser_id

    def back_edit_regex_name(self, read_input_info):
        parser_id = read_input_info.meta_info[PARSER]
        regex_name = read_input_info.content
        self.teacher.update_pattern_name(parser_id, regex_name)
        print 'back_edit_regex_name %s ' % regex_name

    def edit_regex(self, parser_id):
        parser = self.raw_output.parsers[parser_id]

        default_content = parser.pattern
        message = parser.line_content
        self.editor.create_input_window(default_content, message)

        meta_info = {PARSER: parser_id, CHECK_FUNCTION: self.check_regex}
        self._set_read_input_info(self.back_edit_regex, meta_info)
        print 'edit_regex executed with parser_id: %s' % parser_id

    def back_edit_regex(self, read_input_info):
        parser_id = read_input_info.meta_info[PARSER]
        # TODO parse input
        regex = read_input_info.content
        self.teacher.update_pattern(parser_id, regex)
        print 'back_edit_regex %s ' % regex

    def check_regex(self, read_input_info):
        parser_id = read_input_info.meta_info[PARSER]
        regex = read_input_info.content[0]
        line_content = self.raw_output.parsers[parser_id].line_content
        if re.match(re.compile(regex), line_content):
            return True
        else:
            self._warning('Regex doen\' match to line content.')
            return False

    def guess_regex(self, parser_id):
        self.teacher.guess_pattern(parser_id)
        self._reprint_teacher()
        print 'guess_regex executed with parser_id: %s' % parser_id

    def edit_group(self, parser_id, group_id):
        # TODO chose type from enum type
        group = self.raw_output.parsers[parser_id].groups[group_id]

        default_content = group.converter
        message = self.output_formater.format_match(group)
        self.editor.create_input_window(default_content, message)

        meta_info = {PARSER: parser_id, GROUP: group_id}
        self._set_read_input_info(self.back_edit_group, meta_info)
        print 'edit executed with parser: %s and group %s' % (parser_id, group_id)

    def back_edit_group(self, read_input_info):
        parser_id = read_input_info.meta_info[PARSER]
        group_id = read_input_info.meta_info[GROUP]
        # TODO parse input
        converter = read_input_info.content
        self.teacher.set_converter(parser_id, group_id, converter)
        print 'back_edit_group %s ' % group_type

    def edit_log_type(self, parser_id, log_type):
        # TODO chose logtype from list
        parser = self.raw_output.parsers[parser_id]

        defaut_content = parser.log_type_name
        output = OutputAgregator()
        self.output_formater.parser.format_line_headers(output, parser)
        self.output_formater.parser.format_regexes_message(output, parser)
        self.editor.create_input_window(defaut_content, output.get_content())

        meta_info = {PARSER: parser_id}
        self._set_read_input_info(self.back_edit_log_type, meta_info)
        print 'edit_log_type executed with parser_id: %s' % parser_id

    def back_edit_log_type(self, read_input_info):
        parser_id = read_input_info.meta_info[PARSER]
        # TODO parse input
        log_type = read_input_info.content
        self.teacher.set_log_type(parser_id, log_type)
        print 'back_edit_log_type %s ' % log_type

    # TODO implement this function
    def new_log_type(self, parser_id):
        print 'new_log_type executed'

    def edit_primary_key_groups(self, parser_id, primary_key):
        parser = self.raw_output.parsers[parser_id]

        defaut_content = self.output_formater.format_key_groups(parser.primary_key_groups)
        output = OutputAgregator()
        self.output_formater.parser.format_line_headers(output, parser)
        self.output_formater.parser.format_regexes_message(output, parser)

        self.editor.create_input_window(defaut_content, output.get_content())

        meta_info = {PARSER: parser_id}
        self._set_read_input_info(self.back_edit_primary_key, meta_info)
        print 'edit_primary_key_groups executed with parser_id: %s' % parser_id

    def back_edit_primary_key(self, read_input_info):
        parser_id = read_input_info.meta_info[PARSER]
        # TODO parsr input
        groups = read_input_info.content
        # self.teacher.set_primary_key(parser_id, groups)
        print 'back_edit_primary_key %s ' % groups

    def add_constraint(self):
        # TODO add select window between teacher and input window
        output = OutputAgregator()
        parsers = self.raw_output.parsers.values()
        self.output_formater.parser.format_constraint_message(output, parsers)
        content = get_constraint_template()
        self.editor.create_input_window(content, output.get_content())

        self._set_read_input_info(self.back_add_constraint, {})
        print 'add_constraint executed'

    def back_add_constraint(self, read_input_info):
        raw_constraint = read_input_info.content
        # TODO add parse constraint
        # constraint = self.input_reader.parse_constraint(raw_constraint)
        # self.teacher.register_constraint(constraint)
        print 'back_add_constraint %s ' % raw_constraint

    def delete_constraint(self, constraint):
        self.teacher.remove_constraint(constraint)
        self._reprint_teacher()
        print 'delete_constraint executed with constraint %s' % constraint

    def add_param(self, constraint):
        output = OutputAgregator()

        content = self.output_formater.format_param(PARAM_KEY, PARAM_VALUE)
        self.output_formater.constraint.format_constraint(output, constraint)

        self.editor.create_input_window(content, output.get_content())
        meta_info = {CONSTRAINT: constraint}
        self._set_read_input_info(self.back_add_param, meta_info)
        print 'add_param executed with constraint %s' % constraint

    def back_add_param(self, read_input_info):
        param = read_input_info.content
        # TODO parse param
        constraint = read_input_info.meta_info[CONSTRAINT]
        # self.teacher.register_constraint(constraint)
        print 'back_add_param %s ' % param

    def edit_constraint_group(self, constraint, constraint_group):
        output = OutputAgregator()
        parsers = self.raw_output.parsers.values()
        self.output_formater.constraint.format_constraint(output, constraint)
        self.output_formater.parser.format_constraint_message(output, parsers)
        self.editor.create_input_window(str(constraint_group), output.get_content())

        meta_info = {CONSTRAINT: constraint, GROUP: constraint_group}
        self._set_read_input_info(self.back_edit_constraint_group, meta_info)
        print 'edit_constraint executed with %s and %s ' % (constraint, constraint_group)

    def back_edit_constraint_group(self, read_input_info):
        group_content = read_input_info.content
        # TODO parse group
        constraint = read_input_info.meta_info[CONSTRAINT]
        constraint_group = read_input_info.meta_info[GROUP]
        # TODO nowy constraint
        # self.teacher.update_constraint_group(constraint, group_id, group_content)
        print 'back_edit_constraint_group %s' % constraint_group

    def edit_constraint_param(self, constraint, param):
        # TODO add message window with constraint
        output = OutputAgregator()
        content = self.output_formater.format_param(param, constraint.params[param])
        self.output_formater.constraint.format_constraint(output, constraint)
        self.editor.create_input_window(content, output.get_content())

        meta_info = {CONSTRAINT: constraint, PARAM: param}
        self._set_read_input_info(self.back_edit_constraint_param, meta_info)
        print 'edit_constraint_param executed with %s and %s' % (constraint, param)

    def back_edit_constraint_param(self, read_input_info):
        param_content = read_input_info.content
        # TODO parse param content
        constraint = read_input_info.meta_info[CONSTRAINT]
        # self.teacher.update_constraint_param(constraint, param, param_content)
        print 'back_edit_constraint_param %s' % param_content

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
        self.main_proxy.new_teacher()
        print 'give_up_rule executed'
