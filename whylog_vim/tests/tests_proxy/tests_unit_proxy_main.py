from unittest import TestCase
from mock import MagicMock, patch

from whylog import FrontInput, LineSource

from whylog_vim.consts import EditorStates as States
from whylog_vim.proxy import WhylogProxy


class UnitTestWhylogProxy(TestCase):
    def setUp(self):
        mock_editor = MagicMock()
        mock_editor.get_front_input.return_value = FrontInput(1, 'line content', LineSource('host'    , 'path'))
        self.whylog_proxy = WhylogProxy(mock_editor)

    @patch('whylog.LogReader')
    def tests_unit_check_log_reader_states_of_whylog_proxy(self, LogReader):
        LogReader.get_causes.return_value = []
        self.assertEqual(self.whylog_proxy.get_state(), States.EDITOR_NORMAL)
        self.whylog_proxy.action()
        self.assertEqual(self.whylog_proxy.get_state(), States.LOG_READER)
        self.whylog_proxy.action()
        self.assertEqual(self.whylog_proxy.get_state(), States.LOG_READER)

    def tests_unit_check_teacher_states_of_whylog_proxy(self):
        self.assertEqual(self.whylog_proxy.get_state(), States.EDITOR_NORMAL)
        self.whylog_proxy.teach()
        self.assertEqual(self.whylog_proxy.get_state(), States.ADD_CAUSE)
        self.whylog_proxy.teach()
        self.assertEqual(self.whylog_proxy.get_state(), States.TEACHER)
