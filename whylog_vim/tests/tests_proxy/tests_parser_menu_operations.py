import six
from unittest import TestCase
from . import create_mock_editor
from whylog_vim.proxy import WhylogProxy
from mock import patch


class TeacherMenuTests(TestCase):
    def setUp(self):
        self.editor = create_mock_editor()
        self.whylog_proxy = WhylogProxy(self.editor)
        self.whylog_proxy.teach()
        self.whylog_proxy.teach()

    def tests_edit_content(self):
        numb = next(six.iterkeys(self.whylog_proxy.teacher.output.buttons))
        self.editor.get_line_number.return_value = numb
        self.whylog_proxy.action()
        self.editor.get_input_content.return_value = ['some line']
        self.assertNotEqual(self.whylog_proxy.teacher.rule.parsers[0].line_content, 'some line')
        self.whylog_proxy.action()
        self.assertEqual(self.whylog_proxy.teacher.rule.parsers[0].line_content, 'some line')

    @patch('six.print_')
    def tests_edit_content_to_many_lines_fail(self, my_print):
        numb = next(six.iterkeys(self.whylog_proxy.teacher.output.buttons))
        self.editor.get_line_number.return_value = numb
        self.whylog_proxy.action()
        self.editor.get_input_content.return_value = ['some line', 'and another']
        self.whylog_proxy.action()
        # Error message is printed to user
        assert my_print.called
