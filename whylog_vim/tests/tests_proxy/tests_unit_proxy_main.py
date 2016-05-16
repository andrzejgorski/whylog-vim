from unittest import TestCase
from mock import MagicMock

from whylog_vim.consts import EditorStates as States
from whylog_vim.proxy import WhylogProxy


class UnitTestWhylogProxy(TestCase):

    def tests_unit_check_log_reader_states_of_whylog_proxy(self):
        whylog_proxy = WhylogProxy(MagicMock())

        self.assertEqual(whylog_proxy.get_state(), States.EDITOR_NORMAL)
        whylog_proxy.action()
        self.assertEqual(whylog_proxy.get_state(), States.LOG_READER)
        whylog_proxy.action()
        self.assertEqual(whylog_proxy.get_state(), States.LOG_READER)


    def tests_unit_check_teacher_states_of_whylog_proxy(self):
        whylog_proxy = WhylogProxy(MagicMock())

        self.assertEqual(whylog_proxy.get_state(), States.EDITOR_NORMAL)
        whylog_proxy.teach()
        self.assertEqual(whylog_proxy.get_state(), States.ADD_CAUSE)
        whylog_proxy.teach()
        self.assertEqual(whylog_proxy.get_state(), States.TEACHER)
