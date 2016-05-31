from functools import partial
from whylog import whylog_factory
from whylog_vim.proxy.teacher import TeacherProxy
from whylog_vim.proxy.log_reader import LogReaderProxy
from whylog_vim.consts import EditorStates as States, ActionTypes
from whylog_vim.exceptions import UnknownAction
from whylog_vim.output_formater.input_windows_messages import InputMessages


class WhylogProxy(object):
    def __init__(self, editor):
        self.editor = editor
        log_reader, teacher_generator, config = whylog_factory()
        self.teacher_generator = teacher_generator
        self.config = config
        self.log_reader = LogReaderProxy(log_reader, config, editor, self)
        self.teacher = TeacherProxy(self.teacher_generator(), config, self.editor, self)
        self._state = States.EDITOR_NORMAL
        self.log_types = dict()

        self.action_handler = {
            States.ASK_LOG_TYPE: (self.handle_log_type_menu, States.ASK_LOG_TYPE),
            States.EDITOR_NORMAL: (self.log_reader.new_query, States.LOG_READER),
            States.LOG_READER: (self.log_reader.handle_action, States.LOG_READER),
            States.TEACHER: (self.teacher.handle_menu_signal, States.TEACHER),
            States.TEACHER_INPUT: (self._read_input, States.TEACHER_INPUT),
        }

        self.teach_handler = {
            States.EDITOR_NORMAL: (self.teacher.new_lesson, States.ADD_CAUSE),
            States.ADD_CAUSE: (self.teacher.add_cause, States.TEACHER),
        }
        self.handlers = {
            ActionTypes.STANDARD: self.action_handler,
            ActionTypes.TEACHER: self.teach_handler,
        }

    def _read_input(self):
        self.teacher.read_input()

    def try_to_set_log_type_automatic(self, action_after_set_log_type):
        """
        This function is trying to set the log type automatic by the function
        config get_log_type. If it isn't possible it creates new windows,
        which asks user for the logtype.
        """
        if self.editor.is_any_whylog_window_open():
            return True
        line_source = self.editor.get_line_source()
        if self.log_types.get(line_source):
            return True
        if self._state == States.ASK_LOG_TYPE:
            return True

        log_type = self.config.get_log_type(line_source)
        if log_type:
            self.log_types[line_source] = log_type
            return True
        self.create_set_log_type_menu(action_after_set_log_type, line_source)
        return False

    def create_set_log_type_menu(self, action_after_set_log_type, line_source):
        self._state = States.ASK_LOG_TYPE
        log_types = self.config.get_all_log_types()
        output = InputMessages.get_case_log_type_main(
            log_types, partial(self.set_log_type, action_after_set_log_type, line_source)
        )
        self.ask_log_type_output = output
        self.editor.create_case_window(output.get_content())

    def handle_log_type_menu(self):
        self.ask_log_type_output.call_button(self.editor.get_line_number())

    def set_log_type(self, action, line_source, log_type):
        self.log_types[line_source] = log_type
        self.editor.log_type = log_type
        self._state = States.EDITOR_NORMAL
        self.editor.close_case_window()
        self._handle_action(action)

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state

    def action(self):
        self._handle_action(ActionTypes.STANDARD)

    def teach(self):
        self._handle_action(ActionTypes.TEACHER)

    def _update_normal_state(self):
        if not self.editor.is_any_whylog_window_open() and self._state != States.ADD_CAUSE:
            self._state = States.EDITOR_NORMAL

    def _handle_action(self, action_type):
        if self.try_to_set_log_type_automatic(action_type):
            self._update_normal_state()
            try:
                action_function, state = self.handlers[action_type][self._state]
            except KeyError:
                raise UnknownAction(action_type, self._state)
            else:
                self._state = state
                action_function()

    def new_teacher(self):
        self.teacher = TeacherProxy(self.teacher_generator(), self.config, self.editor, self)
        self._state = States.EDITOR_NORMAL

    def create_input_window(self, content):
        self.editor.create_input_window(content)
        self._state = States.TEACHER_INPUT

    def create_case_window(self, content):
        self.editor.create_case_window(content)
        self._state = States.TEACHER_INPUT

    def create_new_log_type(self):
        self.output = InputMessages.get_case_log_types_parser(parser, log_types, partial(self.set_parser_log_type, parser))
        self.read_function = partial(self.back_after_create_new_log_type, parser)
