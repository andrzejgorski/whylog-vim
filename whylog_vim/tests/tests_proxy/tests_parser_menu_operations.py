from mock import call, patch
from unittest2 import TestCase

from whylog_vim.consts import EditorStates, FunctionNames, ReadMessages
from whylog_vim.tests.tests_proxy.utils import TestConsts, create_mock_editor, create_whylog_proxy, create_line_source


class TeacherMenuTests(TestCase):
    def setUp(self):
        self.editor = create_mock_editor()
        self.whylog_proxy = create_whylog_proxy(self.editor)
        self.whylog_proxy.teach()
        self.whylog_proxy.teach()

    def tests_edit_content(self):
        self.editor.get_line_number.return_value = self.whylog_proxy.teacher.output.function_lines[(
            FunctionNames.EDIT_LINE_CONTENT, 0
        )]
        self.whylog_proxy.action()
        self.editor.get_input_content.return_value = ['some line']
        self.assertNotEqual(self.whylog_proxy.teacher.rule.parsers[0].line_content, 'some line')
        self.whylog_proxy.action()
        self.assertEqual(self.whylog_proxy.teacher.rule.parsers[0].line_content, 'some line')
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.TEACHER)

    @patch('six.print_')
    def tests_edit_content_to_many_lines_fail(self, mock_print):
        self.editor.get_line_number.return_value = self.whylog_proxy.teacher.output.function_lines[(
            FunctionNames.EDIT_LINE_CONTENT, 0
        )]
        self.whylog_proxy.action()
        self.editor.get_input_content.return_value = ['some line', 'and another']
        self.whylog_proxy.action()
        self.assertEqual(mock_print.call_args, call(ReadMessages.TOO_MANY_LINES))
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.TEACHER_INPUT)

    def tests_edit_regex(self):
        self.editor.get_line_number.return_value = self.whylog_proxy.teacher.output.function_lines[(
            FunctionNames.EDIT_REGEX, 0
        )]
        self.whylog_proxy.action()
        self.editor.get_input_content.return_value = [TestConsts.REGEX]
        self.whylog_proxy.action()
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.TEACHER)
        self.assertEqual(self.whylog_proxy.teacher.rule.parsers[0].pattern, TestConsts.REGEX + '$')

    @patch('six.print_')
    def tests_edit_regex_to_many_lines_fail(self, mock_print):
        self.editor.get_line_number.return_value = self.whylog_proxy.teacher.output.function_lines[(
            FunctionNames.EDIT_REGEX, 0
        )]
        self.whylog_proxy.action()
        self.editor.get_input_content.return_value = [TestConsts.REGEX, 'and another']
        self.whylog_proxy.action()
        self.assertEqual(mock_print.call_args, call(ReadMessages.TOO_MANY_LINES))
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.TEACHER_INPUT)
