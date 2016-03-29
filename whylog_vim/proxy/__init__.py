from whylog.teacher import Teacher
from whylog_vim.proxy.teacher import TeacherProxy
from whylog_vim.proxy.log_reader import LogReaderProxy


class states:
    # Editor states
    EDITOR_NORMAL = 0
    LOG_READER = 1
    TEACHER = 2


class WhylogProxy():
    """
    This class is the only one that will be used by plugins for text editors
    implementing Whylog.
    It provides all funtionalities of whylog.
    """

    def _update_state(self):
        if not self.editor.is_output_open():
            self._state = states.EDITOR_NORMAL

    def signal_1(self):
        self._update_state()
        if self._state == states.EDITOR_NORMAL:
            self._state = states.LOG_READER
            self.log_reader.new_query()
        elif self._state == states.LOG_READER:
            self.log_reader.signal_1()
        elif self._state == states.TEACHER:
            self.teacher.signal_1()

    def signal_2(self):
        self._update_state()
        if self._state == states.EDITOR_NORMAL:
            self._state = states.TEACHER
            self.teacher.new_lesson()
        elif self._state == states.LOG_READER:
            self.log_reader.signal_2()
        elif self._state == states.TEACHER:
            self.teacher.signal_2()

    def __init__(self, editor, **opening_params):
        self._state = states.EDITOR_NORMAL
        self.editor = editor
        self.log_reader = LogReaderProxy(editor)
        self.teacher = TeacherProxy(editor)
