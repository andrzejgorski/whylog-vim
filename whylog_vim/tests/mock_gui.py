

class MockVimEditor(object):

    def get_input_content(self):
        pass

    def create_case_window(self, default_input=None):
        pass

    def create_input_window(self, default_input=None):
        pass

    def create_teacher_window(self, default_input=None):
        pass

    def create_query_window(self, default_input=None):
        pass

    def go_to_file(self, filename, offset=1):
        pass

    def set_query_output(self, content):
        pass

    def set_teacher_output(self, content):
        pass

    def is_any_whylog_window_open(self):
        pass

    def close_window(self, filename):
        pass

    def get_button_name(self):
        pass

    def get_front_input(self):
        pass

    def close_query_window(self):
        pass

    def close_teacher_window(self):
        pass

    def cursor_at_whylog_windows(self):
        pass

    def cursor_at_teacher_window(self):
        pass

    def cursor_at_input_window(self):
        pass

    def cursor_at_case_window(self):
        pass

    def go_to_query_window(self):
        pass

    def go_to_offset(self, byte_offset):
        pass

    def set_syntax_folding(self):
        pass

    def open_fold(self):
        pass

    def get_current_line(self):
        pass

    def get_current_filename(self):
        pass

    def get_line_number(self):
        pass

    def get_offset(self):
        pass
