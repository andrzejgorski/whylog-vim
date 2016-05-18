class TeacherProxy(object):
    def __init__(self, teacher, editor, main_proxy):
        self.teacher = teacher
        self.editor = editor
        self.main_proxy = main_proxy

    def handle_menu_signal(self):
        pass

    def read_input(self):
        pass

    def new_lesson(self):
        pass

    def add_cause(self):
        pass
