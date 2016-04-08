from whylog.teacher import Teacher
from whylog_vim.output_formater.teacher_formater import TeacherOutput
from whylog_vim.input_reader.teacher_reader import TeacherInputReader
from whylog_vim.input_reader import get_button_name


def naturals_generator():
    i = 1
    while True:
        yield i
        i += 1

naturals = naturals_generator()


class TeacherProxy():

    def __init__(self, editor, teacher):
        self.editor = editor
        self.teacher = teacher
        self.output_formater = TeacherOutput()
        self.input_reader = TeacherInputReader()
        self._effect_is_added = False
        self._cause_is_added = False

    def signal_1(self):
        if self.editor.cursor_at_output():
            # print self.editor.get_button_name()
            self.editor.go_to_input_window()
        else:
            pass

    def signal_2(self):
        if not self._effect_is_added:
            self._new_lesson()
        elif not self._cause_is_added:
            self._add_cause()
        # elif self.editor.cursor_at_output():
        #     pass
        # else:
        #     self._add_cause()

    def _new_lesson(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(0, front_input)
        self._effect_is_added = True
        print '### WHYLOG ### You added line {} as effect. Select cause and press <F4>.'

    def _add_cause(self):
        self.editor.create_teacher_window()
        front_input = self.editor.get_front_input()
        self.teacher.add_line(naturals.next() , front_input)
        self._print_teacher()

    def _print_teacher(self):
        raw_output = self.teacher.get_rule()
        contents = self.output_formater.format(raw_output)
        self.editor.set_output(contents, line=4)
        self.editor.go_to_output_window()
