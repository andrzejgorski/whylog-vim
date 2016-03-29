from whylog_vim.output_formater.teacher_formater import TeacherMenu


class TeacherProxy():

    def __init__(self, editor):
        self.editor = editor
        self.output_formater = TeacherMenu()

    def signal_1(self):
        if self.editor.cursor_at_output():
            self.editor.go_to_input_window()
        else:
            pass

    def signal_2(self):
        if self.editor.cursor_at_output():
            pass
        else:
            self._add_cause()

    def new_lesson(self):
        self.editor.create_output_window()
        front_input = self.editor.get_front_input()
        self.effect = front_input
        self.causes = []
        contents = self.output_formater.format_effect(front_input)
        self.editor.set_output(contents, line=4)
        self.editor.go_to_output_window()

    def _add_cause(self):
        front_input = self.editor.get_front_input()
        self.causes.append(front_input)
        contents = self.output_formater.add_causes(self.effect, self.causes)
        self.editor.set_output(contents, line=4)
        self.editor.go_to_output_window()
