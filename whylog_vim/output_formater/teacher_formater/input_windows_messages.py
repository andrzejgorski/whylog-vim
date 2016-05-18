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
        output.add_commented(ParserOutputs.META % (parser.line_resource_location, parser.line_offset))
        output.add_commented(ENDING)
        return output

    @classmethod
    def get_primary_key_message(cls, parser):
        output = OutputAggregator()
        cls._add_message_prefix(ouptut, WindowTypes.INPUT)
        output.add_commented(Messages.PRIMARY_KEY)
        output.add_commented(ParserOutputs.LINE_CONTENT % (parser._id, parser.line_content))
        output.add_commented(ParserOutputs.META % (parser.line_resource_location, parser.line_offset))
        output.add_commented(parser.pattern)
        for group in parser.groups.keys():
            result.append(POC.GROUP_CONVERTER %
                (group, parser.groups[group].converter, parser.groups[group].content))
        output.add_commented(ENDING)
        return output

    @classmethod
    def get_constraint_message(cls, parsers):
        result = []
        for parser in parsers:
            result.append(POC.LINE_CONTENT % (parser._id, parser.line_content))
            result.append(POC.META % (parser.line_resource_location, parser.line_offset))
            result.append(parser.pattern)
            for group in parser.groups.keys():
                result.append(POC.GROUP_CONVERTER %
                    (group, parser.groups[group].converter, parser.groups[group].content))
            result.append(TeacherConsts.EMPTY_LINE)
        return result
