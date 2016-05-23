import six
from functools import partial

from whylog_vim.consts import ConstraintsOutputs, ParserOutputs, WindowTypes
from whylog_vim.output_formater.consts import TeacherMenu
from whylog_vim.output_formater.output_aggregator import OutputAggregator
from whylog_vim.utils import get_parser_name


class TeacherProxyUsingFromater(object):
    def __init__(self, teacher_proxy):
        self.teacher_proxy = teacher_proxy


class ParserFormater(TeacherProxyUsingFromater):
    def format_parser(self, output, parser, parser_id, effect=True):
        # TODO tell Ewa to do that
        parser._id = parser_id
        self._format_line_info(output, parser, effect)
        self._format_regexes(output, parser)
        self._format_line_others(output, parser)
        output.add('')
        output.add(TeacherMenu.END_BRACKET)

    def _format_line_info(self, output, parser, effect):
        output.add(
            ParserOutputs.MESSAGE_CONTENT % (get_parser_name(parser._id), parser.line_content)
        )
        output.create_button(partial(self.teacher_proxy.edit_line_content, parser._id))
        output.add(ParserOutputs.META % (parser.line_resource_location, parser.line_offset))
        if not effect:
            output.add(ParserOutputs.COPY_BUTTON)
            output.add(ParserOutputs.DELETE_BUTTON)
            output.create_button(partial(self.teacher_proxy.delete_parser, parser._id))
        output.add('')

    def _format_regexes(self, output, parser):
        output.add(ParserOutputs.REGEX_HEADER % parser.pattern_name)
        output.add(parser.pattern)
        output.create_button(partial(self.teacher_proxy.edit_regex, parser._id))
        output.add(ParserOutputs.GUESS_BUTTON)
        output.create_button(partial(self.teacher_proxy.guess_regex, parser._id))
        output.add('')
        self._format_converters(output, parser.groups, parser._id)
        output.add('')

    def _format_line_others(self, output, parser):
        output.add(ParserOutputs.OTHERS_HEADER)
        output.add(ParserOutputs.LOG_TYPE % parser.log_type_name)
        output.create_button(
            partial(self.teacher_proxy.edit_log_type, parser._id, parser.log_type_name)
        )
        output.add(ParserOutputs.PRIMARY_KEY % parser.primary_key_groups)
        output.create_button(
            partial(
                self.teacher_proxy.edit_primary_key_groups, parser._id, parser.primary_key_groups
            )
        )

    def _format_converters(self, output, groups, parser_id):
        for group in groups.keys():
            output.add(
                ParserOutputs.GROUP_CONVERTER %
                (group, groups[group].converter, groups[group].content)
            )
            output.create_button(partial(self.teacher_proxy.edit_converter, parser_id, group))


class ConstraintsFormater(TeacherProxyUsingFromater):
    def format_constraints(self, output, constraints):
        output.add(ConstraintsOutputs.HEADER)
        output.add(ConstraintsOutputs.ADD_BUTTON)
        output.create_button(self.teacher_proxy.add_constraint)
        output.add('')
        for constraint in constraints:
            self._format_single(output, constraint)
        output.add(TeacherMenu.END_BRACKET)

    def _format_single(self, output, constraint):
        output.add(ConstraintsOutputs.TYPE % constraint.type)
        output.create_button(partial(self.teacher_proxy.edit_constraint, constraint))
        output.add(ConstraintsOutputs.DELETE_BUTTON)
        # TODO in this line should be constraint id
        output.create_button(partial(self.teacher_proxy.delete_constraint, constraint))
        for group in constraint.groups:
            output.add(ConstraintsOutputs.GROUP % (get_parser_name(group[0]), group[1]))
        if constraint.params:
            self._format_params(output, constraint)
        output.add(TeacherMenu.EMPTY_LINE)

    def _format_params(self, output, constraint):
        output.add(ConstraintsOutputs.PARAMS_HEADER)
        params = constraint.params
        for param in six.iterkeys(params.keys):
            output.add(ConstraintsOutputs.PARAM % (param, params[param]))


class TeacherFormater(TeacherProxyUsingFromater):
    def __init__(self, teacher_proxy):
        self.parser = ParserFormater(teacher_proxy)
        self.constraint = ConstraintsFormater(teacher_proxy)
        self.teacher_proxy = teacher_proxy

    def _format_causes(self, output, rule, effect_id):
        for line_id in six.iterkeys(rule.parsers):
            if line_id != effect_id:
                self.parser.format_parser(output, rule.parsers[line_id], line_id, effect=False,)

    def format_rule(self, rule_intent, validation_result):
        output = OutputAggregator()
        output.add_commented(WindowTypes.TEACHER)
        effect_id = rule_intent.effect_id

        self.parser.format_parser(output, rule_intent.parsers[effect_id], effect_id, effect=True)
        self._format_causes(output, rule_intent, effect_id)
        self.constraint.format_constraints(output, rule_intent.constraints)
        output.add(TeacherMenu.BUTTONS_HEADER)
        output.add(TeacherMenu.ABANDON_BUTTON)
        output.add(TeacherMenu.VERIFY_BUTTON)
        output.add(TeacherMenu.RETURN_BUTTON)
        output.add(TeacherMenu.SAVE_BUTTON)
        return output
