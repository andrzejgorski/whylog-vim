class TeacherProxy(object):
    def __init__(self, teacher, editor, main_proxy):
        self.teacher = teacher
        self.editor = editor
        self.main_proxy = main_proxy

    def handle_menu_signal(self):
        pass

    def read_input(self):
        self.read_input_info.load_input()
        return_function = self.read_input_info.return_function
        if return_function(self.read_input_info):
            self.editor.create_teacher_window()
            self.performer.print_teacher()

            del self.read_input_info
            self._return_cursor_to_position()

    def new_lesson(self):
        self.performer.new_lesson()

    def add_cause(self):
        self.performer.add_cause()

    def _set_cursor_position(self):
        self._return_offset = self.editor.get_offset()

    def _return_cursor_to_position(self):
        try:
           self.editor.go_to_offset(self._return_offset)
        except Exception:
            raise CannotGoToPosition(self._return_offset)
        try:
            self.editor.open_fold()
        except Exception:
            # Fold opening error. Nothing to do.
            pass
