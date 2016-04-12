from whylog.teacher import Teacher
from whylog.front.utils import FrontInput, LocallyAccessibleLogOpener

from whylog_vim.output_formater.teacher_formater import TeacherOutput
from whylog_vim.input_reader.teacher_reader import get_button_name
from whylog_vim.gui import set_syntax_folding, get_line_number, get_current_line, go_to_offset, get_current_filename, resize
from whylog_vim.consts import ButtonsMetaConsts as BMC, get_constraint_template


# TODO move this function to utils file
def naturals_generator():
    i = 1
    while True:
        yield i
        i += 1

naturals = naturals_generator()


# TODO move it to the consts file
INPUT = 'input'
EFFECT_ADDED = 'efect added'
BEGIN = 'begin'
NORMAL = 'normal'
FUNCTION = 'function'
PARSER = 'parser'
GROUP = 'group'
CONSTRAINT = 'constraint'
PARAM = 'param'


# TODO Move this function to teacher utils file
class ReadInputInfo():

    def __init__(self, function, meta_info=None):
        self.function=function
        self.meta_info=meta_info

    def set_content(self, content):
        self.content = content


# TODO add message window to input
# TODO add lines_button parsed
# TODO add docsstrings


class TeacherProxy():

    def __init__(self, editor, teacher, proxy):
        self.editor = editor
        self.teacher = teacher
        self.output_formater = TeacherOutput()
        self._effect_is_added = False
        self._prepare_buttons()
        self.main_proxy = proxy
        self._state = BEGIN

    def _press_button(self):
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
        self._return_info = {}
        func(**meta)

    def _read_input(self):
        function = self.read_input_info.function
        self.read_input_info.set_content(self.editor.get_input_content())
        function(self.read_input_info)
        # self.editor.change_to_teacher_window()
        self._print_teacher()
        self._state = NORMAL
        del self.read_input_info

    # TODO implement this function
    def _return_cursor(self):
        pass

    def signal_1(self):
        if self.editor.cursor_at_output():
            if self._state == NORMAL:
                self._press_button()
            elif self._state == INPUT:
                self._read_input()
            # self.editor.go_to_input_window()
        else:
            pass

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
        self.teacher.add_line(0, front_input)
        self._effect_is_added = True
        self.origin_file_name = get_current_filename()
        self._state = EFFECT_ADDED
        print '### WHYLOG ### You added line {} as effect. Select cause and press <F4>.'

    def _add_cause(self):
        self.editor.create_teacher_window()
        front_input = self.editor.get_front_input()
        self.teacher.add_line(naturals.next() , front_input)
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
        self.buttons = {
            'edit_content': self.edit_content,
            'copy_line': self.copy_line,
            'delete_line': self.delete_line,
            'edit_regex_name': self.edit_regex_name,
            'edit_regex': self.edit_regex,
            'guess_regex': self.guess_regex,
            ('edit', (BMC.PARSER, BMC.GROUP)): self.edit_group,
            ('edit', (BMC.PARSER, BMC.LOG_TYPE)): self.edit_log_type,
            'new_log_type': self.new_log_type,
            ('edit', (BMC.PARSER, BMC.PRIMARY_KEY)): self.edit_primary_key_groups,
            'add_constraint': self.add_constraint,
            'delete_constraint': self.delete_constraint,
            'add_param': self.add_param,
            ('edit', (BMC.GROUP, BMC.CONSTRAINT)): self.edit_constraint_group,
            ('edit', (BMC.PARAM, BMC.CONSTRAINT)): self.edit_constraint_param,
            'save': self.save,
            'test_rule': self.test_rule,
            'return_to_file': self.return_to_file,
            'give_up_rule': self.give_up_rule,
        }

    def edit_content(self, parser):
        self.editor.create_input_window(self.raw_output.parsers[parser].line_content)
        self.teacher.remove_line(parser)
        meta_info = {PARSER: parser}
        self.read_input_info = ReadInputInfo(self.back_edit_content, meta_info)
        self._state = INPUT
        print 'edit_content executed with parser: %s' % parser

    def back_edit_content(self, read_input_info):
        parser = read_input_info.meta_info[PARSER]
        # TODO parser input
        content = read_input_info.content
        front_input = FrontInput(0, content, None)
        self.teacher.add_line(parser, front_input)
        print 'back_edit_content, %s' % content

    def copy_line(self, parser):
        # TODO id_generator
        new_id = naturals.next()
        self.teacher.add_line(new_id, self.teacher._lines[parser])
        self._reprint_teacher()
        print 'copy_line executed with parser: %s, new_id = %s ' % (parser, new_id)

    def delete_line(self, parser):
        self.teacher.remove_line(parser)
        self._reprint_teacher()
        print 'delete_line executed with parser: %s' % parser

    def edit_regex_name(self, parser):
        # TODO add message with content and pattern
        self.editor.create_input_window(self.raw_output.parsers[parser].pattern_name)
        meta_info = {PARSER: parser}
        self.read_input_info = ReadInputInfo(self.back_edit_regex_name, meta_info)
        self._state = INPUT
        print 'edit_regex_name executed with parser: %s' % parser

    def back_edit_regex_name(self, read_input_info):
        parser = read_input_info.meta_info[PARSER]
        # TODO parser input
        regex_name = read_input_info.content
        # TODO tell Ewa to implement this function
        # self.teacher.update_pattern_name(parser, regex_name)
        print 'back_edit_regex_name %s ' % regex_name

    def edit_regex(self, parser):
        # TODO add message with pattern name and content
        self.editor.create_input_window(self.raw_output.parsers[parser].pattern)
        meta_info = {PARSER: parser}
        self.read_input_info = ReadInputInfo(self.back_edit_regex, meta_info)
        self._state = INPUT
        print 'edit_regex executed with parser: %s' % parser

    def back_edit_regex(self, read_input_info):
        parser = read_input_info.meta_info[PARSER]
        # TODO parser input
        regex = read_input_info.content
        self.teacher.update_pattern(parser, regex)
        print 'back_edit_regex %s ' % regex

    def guess_regex(self, parser):
        self.teacher.guess_pattern(parser)
        self._reprint_teacher()
        print 'guess_regex executed with parser: %s' % parser

    def edit_group(self, parser, group):
        # TODO add message with parser pattern and match
        self.editor.create_input_window(self.raw_output.parsers[parser].groups[group].converter)
        meta_info = {PARSER: parser, GROUP: group}
        self.read_input_info = ReadInputInfo(self.back_edit_group, meta_info)
        self._state = INPUT
        print 'edit executed with parser: %s and group %s' % (parser, group)

    def back_edit_group(self, read_input_info):
        parser = read_input_info.meta_info[PARSER]
        group = read_input_info.meta_info[GROUP]
        # TODO parse input
        group_type = read_input_info.content
        # TODO tells Ewa to implement this function
        # self.teacher.update_group(parser, group, group_type)
        print 'back_edit_group %s ' % group_type

    def edit_log_type(self, parser, log_type):
        # TODO chose logtype from list
        # TODO add message window with pattern and content
        self.editor.create_input_window(self.raw_output.parsers[parser].log_type_name)
        meta_info = {PARSER: parser}
        self.read_input_info = ReadInputInfo(self.back_edit_log_type, meta_info)
        self._state = INPUT
        print 'edit_log_type executed with parser: %s' % parser

    def back_edit_log_type(self, read_input_info):
        parser = read_input_info.meta_info[PARSER]
        # TODO parse input
        log_type = read_input_info.content
        self.teacher.set_log_type(parser, log_type)
        print 'back_edit_log_type %s ' % log_type

    # TODO implement this function
    def new_log_type(self, parser):
        print 'new_log_type executed'

    def edit_primary_key_groups(self, parser, primary_key):
        # TODO add message with content and pattern
        self.editor.create_input_window(str(self.raw_output.parsers[parser].primary_key_groups[0]))
        meta_info = {PARSER: parser}
        self.read_input_info = ReadInputInfo(self.back_edit_primary_key, meta_info)
        self._state = INPUT
        print 'edit_primary_key_groups executed with parser: %s' % parser

    def back_edit_primary_key(self, read_input_info):
        parser = read_input_info.meta_info[PARSER]
        # TODO parsr input
        groups = read_input_info.content
        # TODO tells Ewa that this funciton takse only 1 arg
        # self.teacher.set_primary_key(parser, groups)
        print 'back_edit_primary_key %s ' % groups

    def add_constraint(self):
        # TODO add message with info of lines
        # TODO add select window between teacher and input window
        self.editor.create_input_window(get_constraint_template())
        self.read_input_info = ReadInputInfo(self.back_add_constraint, {})
        self._state = INPUT
        print 'add_constraint executed'

    def back_add_constraint(self, read_input_info):
        raw_constraint = read_input_info.content
        # constraint = self.input_reader.parse_constraint(raw_constraint)
        # self.teacher.register_constraint(constraint)
        print 'back_add_constraint %s ' % raw_constraint

    def delete_constraint(self, constraint):
        self.teacher.remove_constraint(constraint)
        self._reprint_teacher()
        print 'delete_constraint executed with constraint %s' % constraint

    def add_param(self, constraint):
        # TODO add message window with groups and matches
        self.editor.create_input_window('')
        meta_info = {CONSTRAINT: constraint}
        self.read_input_info = ReadInputInfo(self.back_add_param, meta_info)
        self._state = INPUT
        print 'add_param executed with constraint %s' % constraint

    def back_add_param(self, read_input_info):
        param = read_input_info.content
        # TODO parser param
        constraint = read_input_info.meta_info[CONSTRAINT]
        # self.teacher.register_constraint(constraint)
        print 'back_add_param %s ' % param

    def edit_constraint_group(self, constraint, group):
        # TODO add message window with groups of all lines
        self.editor.create_input_window(str(group))
        meta_info = {CONSTRAINT: constraint, GROUP: group}
        self.read_input_info = ReadInputInfo(self.back_edit_constraint_group, meta_info)
        self._state = INPUT
        print 'edit_constraint executed with %s and %s ' % (constraint, group)

    def back_edit_constraint_group(self, read_input_info):
        group_content = read_input_info.content
        # TODO parse group
        constraint = read_input_info.meta_info[CONSTRAINT]
        group = read_input_info.meta_info[GROUP]
        self.teacher.update_constraint_group(constraint, group_id, group_content)
        print 'back_edit_constraint_group %s' % group

    def edit_constraint_param(self, constraint, param):
        # TODO add message window with constraint
        self.editor.create_input_window('%s: %s' % (param, constraint.params[param]))
        meta_info = {CONSTRAINT: constraint, PARAM: param}
        self.read_input_info = ReadInputInfo(self.back_edit_constraint_param, meta_info)
        self._state = INPUT
        print 'edit_constraint_param executed with %s and %s' % (constraint, param)

    def back_edit_constraint_param(self, read_input_info):
        param_content = read_input_info.content
        # TODO parse param content
        constraint = read_input_info.meta_info[CONSTRAINT]
        # TODO tells Ewa to implement this function
        # self.teacher.update_constraint_param(constraint, param, param_content)
        print 'back_edit_constraint_param %s' % param_content

    # TODO add buttons and implement funcitons:
    # 1. Delete param
    # 2. Delete group

    def save(self):
        self.teacher.save()
        print 'save executed'

    def test_rule(self):
        print 'test rule executed'

    def return_to_file(self):
        self.editor.go_to_file(self.origin_file_name, 1)
        self.editor.close_teacher_window()
        print 'return_to_file executed'

    def give_up_rule(self):
        self.main_proxy.new_teacher()
        print 'give_up_rule executed'
