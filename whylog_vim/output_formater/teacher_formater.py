import re
from whylog_vim.consts import GlobalConsts, ButtonsMetaConsts as BMC, ParserOutputConsts as POC, ConstraintsOutputConsts as COC, Messages


class OutputAgregator():

    def __init__(self):
        self.buttons_info = {}
        self.parsers = {}
        self.output_lines = []

    def add(self, element):
        self.output_lines.append(element)

    def get_content(self):
        return '\n'.join(self.output_lines)

    def _get_line(self):
        return len(self.output_lines)

    def set_buttons_meta(self, content):
        line = self._get_line()
        self.buttons_info[line] = content

    def get_button_meta(self, line):
        try:
            return self.buttons_info[line]
        except KeyError:
            return {}


class ParserFormater():

    def _format_regexes(self, output, parser):
        output.add(POC.REGEX_HEAD % parser.pattern_name)
        output.add(parser.pattern)
        output.add(POC.REGEX_BUTTONS)
        output.set_buttons_meta({BMC.PARSER: parser._id})
        output.add(GlobalConsts.EMPTY_LINE)
        self._format_converters(output, parser.groups, parser._id)
        output.add(GlobalConsts.EMPTY_LINE)

    def _format_converters(self, output, groups, parser_id):
        for group in groups.keys():
            output.add(POC.GROUP_CONVERTER %
                (group, groups[group].converter, groups[group].content))
            output.set_buttons_meta({BMC.PARSER: parser_id, BMC.GROUP: group})

    def _format_line_info(self, output, message, parser):
        output.add(POC.MESSAGE_CONTENT % (message, parser._id, parser.line_content))
        output.add(POC.META % (parser.line_resource_location, parser.line_offset))
        output.add(POC.LINE_BUTTONS)
        output.set_buttons_meta({BMC.PARSER: parser._id})
        output.add(GlobalConsts.EMPTY_LINE)

    def _format_line_others(self, output, parser):
        output.add(POC.OTHERS_HEAD)
        output.add(POC.LOG_TYPE % parser.log_type_name)
        output.set_buttons_meta({BMC.PARSER: parser._id, BMC.LOG_TYPE: parser.log_type_name})
        output.add(POC.PRIMARY_KEY % parser.primary_key_groups[0])
        output.set_buttons_meta({BMC.PARSER: parser._id, BMC.PRIMARY_KEY: parser.primary_key_groups[0]})

    def format(self, output, message, parser, parser_id):
        parser._id = parser_id
        self._format_line_info(output, message, parser)
        self._format_regexes(output, parser)
        self._format_line_others(output, parser)
        output.add(GlobalConsts.EMPTY_LINE)
        output.add(GlobalConsts.END_BRACKET)


class ConstraintsFormater():

    def _format_params(self, output, constraint):
        output.add(GlobalConsts.EMPTY_LINE)
        output.add(COC.PARAMS_HEADER)
        params = constraint.params
        for param in params.keys():
            output.add(COC.PARAM % (param, params[param]))
            output.set_buttons_meta({BMC.CONSTRAINT: constraint, BMC.PARAM: param})
        output.add(GlobalConsts.EMPTY_LINE)

    def _format_single(self, output, constraint):
        output.add(COC.TYPE % constraint.type)
        output.add(COC.CONSTR_BUTTONS)
        # TODO in this line should be constraint id
        output.set_buttons_meta({BMC.CONSTRAINT: constraint})
        # FIXME
        for group in constraint.groups:
            output.add(COC.GROUP % (group[0], group[1]))
            # FIXME
            output.set_buttons_meta({BMC.CONSTRAINT: constraint, BMC.GROUP: group})
        if constraint.params:
            self._format_params(output, constraint)
        output.add(GlobalConsts.EMPTY_LINE)

    def format(self, output, constraints):
        output.add(COC.HEADER)
        output.add(COC.BUTTONS)
        output.add(GlobalConsts.EMPTY_LINE)
        for constraint in constraints:
            self._format_single(output, constraint)
        output.add(GlobalConsts.END_BRACKET)


class TeacherOutput():

    def __init__(self):
        self.parser_formater = ParserFormater()
        self.constraints_formater = ConstraintsFormater()

    def _format_effect_line(self, output, raw_output, effect_id):
        self.parser_formater.format(
                output,
                Messages.EFFECT,
                raw_output.parsers[effect_id],
                effect_id,
            )

    def _format_causes(self, output, rule, effect_id):
        causes_lines = rule.parsers.keys()
        causes_lines.remove(effect_id)
        for line_id in causes_lines:
            self.parser_formater.format(
                    output,
                    Messages.CAUSE,
                    rule.parsers[line_id],
                    line_id,
                )

    def format_rule(self, rule_intent):
        output = OutputAgregator()
        output.add(GlobalConsts.MAIN_HEADER)
        effect_id = rule_intent.effect_id
        self._format_effect_line(output, rule_intent, effect_id)
        self._format_causes(output, rule_intent, effect_id)
        self.constraints_formater.format(output, rule_intent.constraints)
        output.add(GlobalConsts.BUTTONS_HEADER)
        output.add(GlobalConsts.MAIN_BUTTONS)
        output.add(GlobalConsts.END_BRACKET)
        return output
