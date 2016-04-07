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

    def signal_1(self):
        if self.editor.cursor_at_output():
            # print self.editor.get_button_name()
            self.editor.go_to_input_window()
        else:
            pass

    def signal_2(self):
        if self.editor.cursor_at_output():
            pass
        else:
            self._add_cause()

    def new_lesson(self):
        self.editor.create_teacher_window()
        front_input = self.editor.get_front_input()
        self.teacher.add_line(0, front_input)
        contents = self.output_formater.print_teacher(self.teacher)
        self.editor.set_output(contents, line=4)
        self.editor.go_to_output_window()

    def _add_cause(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(naturals.next() , front_input)
        contents = self.output_formater.print_teacher(self.teacher)
        self.editor.set_output(contents, line=4)
        self.editor.go_to_output_window()
