from functools import partial

from whylog import FrontInput
from whylog_vim.input_reader.teacher_reader import TeacherReader
from whylog_vim.output_formater.teacher_formater.input_windows_messages import InputMessages


class MenuHandler(object):
    def edit_line_content(self, parser_id):
        output = InputMessages.get_edit_line_message(self.rule.parsers[parser_id].line_content)
        effect = self.rule.effect_id == parser_id
        self.main_proxy.create_input_window(output.get_content())
        self.read_function = partial(self.back_after_edit_line_content, parser_id, effect)

    def back_after_edit_line_content(self, parser_id, effect):
        content = self.editor.get_input_content()
        if len(content) == 1:
            front_input = FrontInput(None, content[0], None)
            self.teacher.add_line(parser_id, front_input, effect)
            return True
        return False

    def edit_regex(self, parser):
        output = InputMessages.get_edit_regex(parser.line_content, parser.pattern)
        self.main_proxy.create_input_window(output.get_content())
        self.read_function = partial(self.back_after_edit_regex, parser)

    def back_after_edit_regex(self, parser):
        content = TeacherReader.read_single_line(self.editor.get_input_content())
        if content:
            self.teacher.update_pattern(parser.line_id, content)
            return True
        return False
