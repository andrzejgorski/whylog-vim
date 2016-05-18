import six

from whylog_vim.output_formater.consts import Global
from whylog_vim.consts import Messages, ParserOutputs, WindowTypes
from whylog_vim.output_fromater.output_aggregator import OutputAggregator


class InputMessages(object):
    TYPE_TO_MESSAGE = {
        WindowTypes.INPUT: Messages.INPUT_INFO,
        WindowTypes.CASE: Messages.CASE_INFO,
        WindowTypes.TEACHER: Messages.CASE_INFO,
    }

    @classmethod
    def _add_message_prefix(cls, output, window_type):
        if window_type == WindowTypes.TEACHER:
            output.add_commented(Messages.TEACHER_HEADER)
        else:
            output.add_commented(Messages.INPUT_HEADER)
        output.add_commented(TYPE_TO_MESSGAE[window_type])

    @classmethod
    def get_log_types_message(cls, parser):
        output = OutputAggregator()
        cls._add_message_prefix(ouptut, WindowTypes.INPUT)
        output.add_commented(Messages.LOGTYPE)
        output.add_commented(ParserOutputs.LINE_CONTENT % (parser._id, parser.line_content))
        output.add_commented(
            ParserOutputs.META % (parser.line_resource_location, parser.line_offset)
        )
        output.add_commented(ENDING)
        return output

    @classmethod
    def _add_parser(cls, output, parser):
        output.add_commented(ParserOutputs.LINE_CONTENT % (parser._id, parser.line_content))
        output.add_commented(
            ParserOutputs.META % (parser.line_resource_location, parser.line_offset)
        )
        output.add_commented(parser.pattern)
        for group in six.iterkeys(parser.groups):
            output.add_commented(
                ParserOutputs.GROUP_CONVERTER %
                (group, parser.groups[group].converter, parser.groups[group].content)
            )
        output.add_commented(Global.EMPTY_LINE)

    @classmethod
    def get_primary_key_message(cls, parser):
        output = OutputAggregator()
        cls._add_message_prefix(ouptut, WindowTypes.INPUT)
        output.add_commented(Messages.PRIMARY_KEY)
        cls._add_parser(output, parser)
        return output

    @classmethod
    def get_constraint_message(cls, parsers):
        output = OutputAggregator()
        cls._add_message_prefix(ouptut, WindowTypes.INPUT)
        for parser in parsers:
            cls._add_parser(output, parser)
        return output
