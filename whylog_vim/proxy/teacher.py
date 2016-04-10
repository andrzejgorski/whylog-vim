from whylog.teacher import Teacher
from whylog_vim.output_formater.teacher_formater import TeacherOutput
from whylog_vim.input_reader.teacher_reader import get_button_name
from whylog_vim.gui import set_syntax_folding, get_line_number, get_current_line, go_to_offset, get_current_filename, resize
from whylog_vim.consts import ButtonsMetaConsts as BMC, get_constraint_template


def naturals_generator():
    i = 1
    while True:
        yield i
        i += 1

naturals = naturals_generator()


INPUT = 'input'
EFFECT_ADDED = 'efect added'
BEGIN = 'begin'
NORMAL = 'normal'


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
            else:
                func(**meta)
        else:
            func(**meta)

    def _read_input(self):
        content = self.editor.get_input_content()
        self.editor.change_to_teacher_window()
        self._print_teacher()
        self._state = NORMAL

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
        self._state = INPUT
        # print 'edit_content executed with parser: %s' % parser

    def copy_line(self, parser):
        self.teacher.add_line(self.teacher._lines[parser])
        self._reprint_teacher()
        print 'copy_line executed with parser: %s' % parser

    def delete_line(self, parser):
        self.teacher.remove_line(parser)
        self._reprint_teacher()
        print 'delete_line executed with parser: %s' % parser

    def edit_regex_name(self, parser):
        self.editor.create_input_window(self.raw_output.parsers[parser].pattern_name)
        self._state = INPUT
        print 'edit_regex_name executed with parser: %s' % parser

    def edit_regex(self, parser):
        self.editor.create_input_window(self.raw_output.parsers[parser].pattern)
        self._state = INPUT
        print 'edit_regex executed with parser: %s' % parser

    def guess_regex(self, parser):
        self.teacher.guess_pattern(parser)
        self._reprint_teacher()
        print 'guess_regex executed with parser: %s' % parser

    def edit_group(self, parser, group):
        self.editor.create_input_window(self.raw_output.parsers[parser].groups[group].converter)
        self._state = INPUT
        print 'edit executed with parser: %s and group %s' % (parser, group)

    def edit_log_type(self, parser, log_type):
        self.editor.create_input_window(self.raw_output.parsers[parser].log_type_name)
        self._state = INPUT
        print 'edit_log_type executed with parser: %s' % parser

    # TODO
    def new_log_type(self, parser):
        print 'new_log_type executed'

    def edit_primary_key_groups(self, parser, primary_key):
        self.editor.create_input_window(str(self.raw_output.parsers[parser].primary_key_groups[0]))
        self._state = INPUT
        print 'edit_primary_key_groups executed with parser: %s' % parser

    def add_constraint(self):
        self.editor.create_input_window(get_constraint_template())
        self._state = INPUT
        print 'add_constraint executed'

    def delete_constraint(self, constraint):
        self.teacher.remove_constraint(constraint)
        self._reprint_teacher()
        print 'delete_constraint executed with constraint %s' % constraint

    def add_param(self, constraint):
        self.editor.create_input_window('')
        self._state = INPUT
        print 'add_param executed with constraint %s' % constraint

    def edit_constraint_group(self, constraint, group):
        self.editor.create_input_window(str(group))
        self._state = INPUT
        print 'edit_constraint executed with %s and %s ' % (constraint, group)

    def edit_constraint_param(self, constraint, param):
        self.editor.create_input_window('%s: %s' % (param, constraint.params[param]))
        self._state = INPUT
        print 'edit_constraint_param executed with %s and %s' % (constraint, param)

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
