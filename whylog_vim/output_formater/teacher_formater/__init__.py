import six
from functools import partial

from whylog_vim.consts import WindowTypes
from whylog_vim.output_formater.consts import TeacherMenu
from whylog_vim.output_formater.output_aggregator import OutputAggregator
from whylog_vim.consts import ParserOutputs


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
        output.add(TeacherConsts.END_BRACKET)

    def _format_line_info(self, output, parser, effect):
        output.add(ParserOutputs.MESSAGE_CONTENT % (get_parser_name(parser._id), parser.line_content))
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
        output.create_button(partial(self.teacher_proxy, parser._id))
        output.add('')
        self._format_converters(output, parser.groups, parser._id)
        output.add('')

    def _format_line_others(self, output, parser):
        output.add(ParserOutputs.OTHERS_HEADER)
        output.add(ParserOutputs.LOG_TYPE % parser.log_type_name)
        output.create_button(partial(self.teacher_proxy, parser._id, parser.log_type_name))
        output.add(ParserOutputs.PRIMARY_KEY % parser.primary_key_groups)
        output.create_button(partial(self.teacher_performer.edit_primary_key_groups, parser._id, parser.primary_key_groups)

    def _format_converters_(self, output, groups, parser_id):
        for group in groups.keys():
            output.add(POC.GROUP_CONVERTER %
                (group, groups[group].converter, groups[group].content))
            output.create_button(partial(self.teacher_proxy.edit_group, parser_id,  group))


class ConstraintsFormater(TeacherProxyUsingFromater):
    def format_constraints(self, output, constraints):
        pass


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
