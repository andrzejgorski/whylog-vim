import six

from functools import partial
from itertools import count
from whylog import FrontInput
from whylog_vim.consts import ReadMessages

get_next_parser_id = partial(next, count(0))
get_next_constraints_id = partial(next, count(0))


class MenuHandler(object):
    def edit_line_content(self, parser_id):
        old_line_content = [self.rule.parsers[parser_id].line_content]
        self.main_proxy.create_input_window(old_line_content)
        self.read_function = partial(self.back_after_edit_line_content, parser_id)

    def back_after_edit_line_content(self, parser_id):
        content = self.editor.get_input_content()
        if len(content) == 1:
            front_input = FrontInput(None, content[0], None)
            self.teacher.add_line(parser_id, front_input)
            return True
        else:
            six.print_(ReadMessages.TOO_MANY_LINES)
            return False
