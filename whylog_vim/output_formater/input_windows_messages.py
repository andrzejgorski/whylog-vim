from functools import partial

import six
from whylog_vim.consts import (  # isort:skip
    Messages, ParserOutputs, WindowTypes, LogType, DefaultContent, FunctionNames  # isort:skip
)  # isort:skip
from whylog_vim.output_formater.output_aggregator import OutputAggregator


class InputMessages(object):
    TYPE_TO_MESSAGE = {
        WindowTypes.INPUT: Messages.INPUT_INFO,
        WindowTypes.CASE: Messages.CASE_INFO,
        WindowTypes.TEACHER: Messages.CASE_INFO,
    }

    @classmethod
    def _create_prefix(cls, window_type):
        output = OutputAggregator()
        if window_type == WindowTypes.TEACHER:
            output.add_commented(Messages.TEACHER_HEADER)
        else:
            output.add_commented(Messages.INPUT_HEADER)
        output.add_commented(cls.TYPE_TO_MESSAGE[window_type])
        return output

    @classmethod
    def get_log_types_message(cls, parser, log_types, read_function):
        output = cls._create_prefix(WindowTypes.INPUT)
        output.add_commented(Messages.LOGTYPE)
        output.add_commented(ParserOutputs.LINE_CONTENT % (parser._id, parser.line_content))
        output.add_commented(
            ParserOutputs.META % (parser.line_resource_location, parser.line_offset)
        )
        output.add_commented('')
        output.add_commented(Messages.SELECT_LOG_TYPE)
        output.add_commented(Messages.ENDING)
        cls._format_menu_for_log_type(output, log_types, read_function)
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
        output.add_commented('')

    @classmethod
    def get_primary_key_message(cls, parser):
        output = cls._create_prefix(WindowTypes.INPUT)
        output.add_commented(Messages.PRIMARY_KEY)
        cls._add_parser(output, parser)
        output.add_commented(Messages.ENDING)
        return output

    @classmethod
    def get_constraint_message(cls, parsers):
        output = cls._create_prefix(WindowTypes.INPUT)
        for parser in parsers:
            cls._add_parser(output, parser)
        output.add_commented(Messages.ENDING)
        return output

    @classmethod
    def get_edit_line_message(cls, old_content):
        output = cls._create_prefix(WindowTypes.INPUT)
        output.add_commented(Messages.ENDING)
        output.add(old_content)
        return output

    @classmethod
    def get_edit_regex_message(cls, line_content, old_regex):
        output = cls._create_prefix(WindowTypes.INPUT)
        output.add_commented(Messages.CONTENT_OF_LINE)
        output.add_commented(line_content)
        output.add_commented(Messages.ENDING)
        output.add(old_regex)
        return output

    @classmethod
    def _format_log_type(cls, output, log_type, read_function):
        create_button_param = (
            partial(read_function, log_type), (FunctionNames.READ_LOG_TYPE, log_type.name)
        )
        output.add(LogType.NAME % log_type.name)
        output.create_button(*create_button_param)
        for matcher in log_type.filename_matchers:
            host_pattern = matcher.host_pattern or DefaultContent.UNDEFINED
            path_pattern = matcher.path_pattern or DefaultContent.UNDEFINED
            super_parser = matcher.super_parser.regex.pattern or DefaultContent.UNDEFINED

            output.add(LogType.HOST_PATTERN % host_pattern)
            output.create_button(*create_button_param)
            output.add(LogType.PATH_PATTERN % path_pattern)
            output.create_button(*create_button_param)
            output.add(LogType.SUPER_PARSER % super_parser)
            output.create_button(*create_button_param)

    @classmethod
    def _format_menu_for_log_type(cls, output, log_types, read_function):
        for log_type in log_types:
            cls._format_log_type(output, log_type, read_function)

    @classmethod
    def get_main_set_log_type_message(cls, log_types, read_function):
        output = cls._create_prefix(WindowTypes.CASE)
        output.add_commented(Messages.SELECT_LOG_TYPE)
        cls._format_menu_for_log_type(output, log_types, read_function)
        return output
