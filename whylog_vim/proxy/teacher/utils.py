from functools import partial
from itertools import count

import six

from whylog import FrontInput
from whylog_vim.consts import ReadMessages
from whylog_vim.output_formater.teacher_formater.input_windows_messages import InputMessages

get_next_parser_id = partial(next, count(0))
get_next_constraints_id = partial(next, count(0))


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
        else:
            six.print_(ReadMessages.TOO_MANY_LINES)
            return False
