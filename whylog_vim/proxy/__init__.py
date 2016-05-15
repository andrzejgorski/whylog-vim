from whylog import whylog_factory
from whylog_vim.proxy.teacher import TeacherProxy
from whylog_vim.proxy.log_reader import LogReaderProxy
from whylog_vim.consts import EditorStates as States, ActionTypes
from whylog_vim.exceptions import UnknownAction


class WhylogProxy(object):
    def __init__(self, editor):
        self.editor = editor
        log_reader, teacher_generator = whylog_factory()
        self.teacher_generator = teacher_generator
        self.log_reader = LogReaderProxy(editor, log_reader)
        self.new_teacher()

        self.action_handler = {
            States.EDITOR_NORMAL:
            (self.log_reader.new_query, States.LOG_READER),
            States.LOG_READER:
            (self.log_reader.handle_action, States.LOG_READER),
            States.TEACHER: (self.teacher.handle_menu_signal, States.TEACHER),
            States.TEACHER_INPUT: (self._read_input, States.TEACHER_INPUT),
        }

        self.teach_handler = {
            States.EDITOR_NORMAL: (self.teacher.new_lesson, States.ADD_CAUSE),
            States.ADD_CAUSE: (self.teacher.add_cause, States.TEACHER),
        }

    def _read_input(self):
        if self.editor.cursor_at_input() or self.editor.cursor_at_case():
            self.teacher.read_input()

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state

    def action(self):
        self._handle_action(self.action_handler, ActionTypes.STANDARD)

    def teach(self):
        self._handle_action(self.teach_handler, ActionTypes.TEACHER)

    def _update_normal_state(self):
        if not self.editor.is_whylog_window_open() and not self._state == States.ADD_CAUSE:
            self._state = States.EDITOR_NORMAL

    def _handle_action(self, handler, action_type):
        self._update_normal_state()
        try:
            action_function, state = handler[self._state]
        except KeyError:
            raise UnknownAction(action_type, self._state)
        else:
            self._state = state
            action_function()

    def new_teacher(self):
        self.teacher = TeacherProxy(self.teacher_generator(), self.editor,
                                    self)
        self._state = States.EDITOR_NORMAL
