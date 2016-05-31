from mock import patch
from unittest2 import TestCase

from whylog_vim.consts import EditorStates as States
from whylog_vim.consts import FunctionNames
from whylog_vim.proxy import WhylogProxy
from whylog_vim.tests.tests_proxy.utils import create_mock_editor, create_whylog_proxy


class UnitTestWhylogProxy(TestCase):
    def setUp(self):
        self.whylog_proxy = create_whylog_proxy(create_mock_editor())

    def tests_unit_check_log_reader_states_of_whylog_proxy(self):
        with patch('whylog.log_reader.LogReader.get_causes') as mock:
            mock.return_value = []
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

    def test_no_log_type(self):
        self.editor = create_mock_editor()
        self.whylog_proxy = WhylogProxy(self.editor)
        with patch('whylog.log_reader.LogReader.get_causes') as mock:
            mock.return_value = []
            self.assertEqual(self.whylog_proxy.get_state(), States.EDITOR_NORMAL)
            self.editor.is_any_whylog_window_open.return_value = False
            self.whylog_proxy.action()
            self.editor.is_any_whylog_window_open.return_value = True
            self.assertEqual(self.whylog_proxy.get_state(), States.ASK_LOG_TYPE)
            self.editor.get_line_number.return_value = self.whylog_proxy.ask_log_type_output.function_lines[
                (FunctionNames.READ_LOG_TYPE, 'default')
            ]
            self.whylog_proxy.action()
            self.assertEqual(self.whylog_proxy.get_state(), States.LOG_READER)
            self.whylog_proxy.action()
            self.assertEqual(self.whylog_proxy.get_state(), States.LOG_READER)
