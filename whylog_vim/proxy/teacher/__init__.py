from whylog_vim.consts import EditorStates
from whylog_vim.output_formater.teacher_formater import TeacherFormater
from whylog_vim.proxy.teacher.utils import get_next_parser_id


class TeacherProxy(object):
    def __init__(self, teacher, editor, main_proxy):
        self.teacher = teacher
        self.editor = editor
        self.main_proxy = main_proxy

    def handle_menu_signal(self):
        self._set_cursor_position()
        line_number = self.editor.get_line_number()
        meta = self.output.get_button_meta(line_number)
        try:
            func = meta[BMC.FUNCTION]
        except KeyError:
            try:
                func = self.buttons[self.editor.get_button_name()]
            except KeyError:
                print 'This line is not editable'
            else:
                func(**meta)
        else:
            del meta[BMC.FUNCTION]
            func(**meta)

        if self.main_proxy.get_state() == EditorStates.TEACHER:
            self._return_cursor_to_position()
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
        front_input = self.editor.get_front_input()
        self.teacher.add_line(get_next_parser_id(), front_input, effect=True)
        self.origin_file_name = self.editor.get_current_filename()

        # TODO Add consts dialoges
        print '### WHYLOG ### You added line as effect. Select cause and press <F4>.'

    def add_cause(self):
        front_input = self.editor.get_front_input()
        self.teacher.add_line(get_next_parser_id(), front_input)
        self.editor.create_teacher_window()
        self.print_teacher()

    def print_teacher(self):
        self.raw_rule = self.teacher.get_rule()
        output = TeacherFormater.format_rule(self.raw_rule)
        self.output = output
        self.editor.set_teacher_output(output.get_content())
        self.editor.set_syntax_folding()
        self.main_proxy.set_state(EditorStates.TEACHER)

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

    def set_return_function(self, return_function):
        self.return_function = return_function
