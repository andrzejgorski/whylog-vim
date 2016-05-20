import six
import platform
from unittest import TestCase, skipIf
from mock import patch, call
from . import create_mock_editor
from whylog_vim.proxy import WhylogProxy
from whylog_vim.consts import ReadMessages


class TeacherMenuTests(TestCase):
    def setUp(self):
        self.editor = create_mock_editor()
        self.whylog_proxy = WhylogProxy(self.editor)
        self.whylog_proxy.teach()
        self.whylog_proxy.teach()

    @skipIf(platform.system() == 'java', 'not supported on jython')
    def tests_edit_content(self):
        numb = next(six.iterkeys(self.whylog_proxy.teacher.output.buttons))
        self.editor.get_line_number.return_value = numb
        self.whylog_proxy.action()
        self.editor.get_input_content.return_value = ['some line']
        self.assertNotEqual(self.whylog_proxy.teacher.rule.parsers[0].line_content, 'some line')
        self.whylog_proxy.action()
        self.assertEqual(self.whylog_proxy.teacher.rule.parsers[0].line_content, 'some line')

    @patch('six.print_')
    @skipIf(platform.system() == 'java', 'not supported in jython')
    def tests_edit_content_to_many_lines_fail(self, mock_print):
        numb = next(six.iterkeys(self.whylog_proxy.teacher.output.buttons))
        self.editor.get_line_number.return_value = numb
        self.whylog_proxy.action()
        self.editor.get_input_content.return_value = ['some line', 'and another']
        self.whylog_proxy.action()
        self.assertEqual(mock_print.call_args, call(ReadMessages.TOO_MANY_LINES))
