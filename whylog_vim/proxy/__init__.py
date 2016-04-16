from whylog.front.whylog_factory import whylog_factory
from whylog_vim.proxy.teacher import TeacherProxy
from whylog_vim.proxy.log_reader import LogReaderProxy
from whylog_vim.consts import mainStates as States


#TODO Add path_loader
WHYLOG_PATH = '/home/andrzej/.whylog/config'


class WhylogProxy():
    """
    This class is the only one that will be used by plugins for text editors
    implementing Whylog.
    It provides all funtionalities of whylog.
    """

    def _update_state(self):
        if not self.editor.is_whylog_window_open():
            self._state = States.EDITOR_NORMAL

    def signal_1(self):
        self._update_state()
        if self._state == States.EDITOR_NORMAL:
            self._state = States.LOG_READER
            self.log_reader.new_query()
        elif self._state == States.LOG_READER:
            self.log_reader.signal_1()
        elif self._state == States.TEACHER:
            self.teacher.signal_1()

    def signal_2(self):
        self._update_state()
        if self._state == States.EDITOR_NORMAL:
            self._state = States.TEACHER
            self.teacher.signal_2()
        elif self._state == States.LOG_READER:
            self.log_reader.signal_2()
        elif self._state == States.TEACHER:
            self.teacher.signal_2()

    def __init__(self, editor, path=WHYLOG_PATH, **opening_params):
        log_reader, teacher_generator = whylog_factory(path)
        self._state = States.EDITOR_NORMAL
        self.editor = editor
        self.teacher_generator = teacher_generator
        self.log_reader = LogReaderProxy(editor, log_reader)
        self._create_teacher()

    def _create_teacher(self):
        self.teacher = TeacherProxy(self.teacher_generator.next(), self.editor, self)

    def new_teacher(self):
        self.teacher.close()
        self.create_teacher()
        self._state = States.EDITOR_NORMAL
