import six
from mock import call, patch
from unittest2 import TestCase

from whylog_vim.consts import EditorStates, FunctionNames, ReadMessages
from whylog_vim.tests.tests_proxy.utils import TestConsts, MocksForProxy


class TeacherMenuTests(TestCase):
    def setUp(self):
        self.editor = MocksForProxy.create_mock_editor()
        self.whylog_proxy = MocksForProxy.create_whylog_proxy(self.editor)
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

    def tests_delete_parser(self):
        self.editor.get_line_number.return_value = self.whylog_proxy.teacher.output.function_lines[(
            FunctionNames.DELETE_PARSER, 1
        )]
        self.assertEqual(len(self.whylog_proxy.teacher.rule.parsers), 2)
        self.whylog_proxy.action()
        self.assertEqual(len(self.whylog_proxy.teacher.rule.parsers), 1)
        # Check if effect parser is not deleted.
        self.assertEqual(next(six.iterkeys(self.whylog_proxy.teacher.rule.parsers)), 0)

    @patch('whylog.config.abstract_config.AbstractConfig.get_all_log_types')
    def tests_edit_log_type(self, get_all_log_types):
        get_all_log_types.return_value = MocksForProxy.mock_log_types()
        self.assertNotEqual(
            self.whylog_proxy.teacher.rule.parsers[0].log_type_name, TestConsts.NEW_LOG_TYPE
        )
        self.editor.get_line_number.return_value = self.whylog_proxy.teacher.output.function_lines[(
            FunctionNames.EDIT_LOG_TYPE,
            0,
        )]
        self.whylog_proxy.action()
        self.editor.get_line_number.return_value = self.whylog_proxy.teacher.output.function_lines[(
            FunctionNames.READ_LOG_TYPE, TestConsts.NEW_LOG_TYPE
        )]
        self.whylog_proxy.action()
        self.assertEqual(
            self.whylog_proxy.teacher.rule.parsers[0].log_type_name, TestConsts.NEW_LOG_TYPE
        )

    def tests_abandon_rule(self):
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.TEACHER)
        self.editor.get_line_number.return_value = self.whylog_proxy.teacher.output.function_lines[(
            FunctionNames.ABANDON_RULE
        )]
        self.whylog_proxy.action()
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.EDITOR_NORMAL)

    def tests_return_to_file(self):
        self.assertEqual(len(self.whylog_proxy.teacher.rule.parsers), 2)
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.TEACHER)
        self.editor.get_line_number.return_value = self.whylog_proxy.teacher.output.function_lines[(
            FunctionNames.RETURN_TO_FILE
        )]
        self.whylog_proxy.action()
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.ADD_CAUSE)
        self.whylog_proxy.teach()
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.TEACHER)
        self.assertEqual(len(self.whylog_proxy.teacher.rule.parsers), 3)

    @patch('whylog.teacher.Teacher.save')
    def tests_save(self, save_function):
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.TEACHER)
        self.editor.get_line_number.return_value = self.whylog_proxy.teacher.output.function_lines[(
            FunctionNames.SAVE
        )]
        self.whylog_proxy.action()
        self.assertEqual(self.whylog_proxy.get_state(), EditorStates.EDITOR_NORMAL)
        self.assertTrue(save_function.called)
