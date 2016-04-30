import re
from whylog_vim.consts import (
    GlobalConsts,
    ButtonsMetaConsts as BMC,
    ParserOutputConsts as POC,
    ConstraintsOutputConsts as COC,
    Messages,
    WarningMessages,
    LogTypeConsts as LTC,
    WindowTypes,
)


#TODO Refactor this module.


def get_parser_name(id_):
    if id_ == 0:
        return POC.EFFECT_LINE_NAME
    else:
        return POC.CAUSE_LINE_NAME % id_


def get_log_types_message(parser):
    result = [Messages.LOGTYPE]
    result.append(POC.LINE_CONTENT % (parser._id, parser.line_content))
    result.append(POC.META % (parser.line_resource_location, parser.line_offset))
    return result


def get_primary_key_message(parser):
    result = [Messages.PRIMARY_KEY]
    result.append(POC.LINE_CONTENT % (parser._id, parser.line_content))
    result.append(POC.META % (parser.line_resource_location, parser.line_offset))
    result.append(parser.pattern)
    for group in parser.groups.keys():
        result.append(POC.GROUP_CONVERTER %
            (group, parser.groups[group].converter, parser.groups[group].content))
    return result


def get_constraint_message(parsers):
    result = []
    for parser in parsers:
        result.append(POC.LINE_CONTENT % (parser._id, parser.line_content))
        result.append(POC.META % (parser.line_resource_location, parser.line_offset))
        result.append(parser.pattern)
        for group in parser.groups.keys():
            result.append(POC.GROUP_CONVERTER %
                (group, parser.groups[group].converter, parser.groups[group].content))
        result.append(GlobalConsts.EMPTY_LINE)
    return result


def to_buttons(elem_list):
    result = '[%s]' % elem_list[0]
    for elem in elem_list[1:]:
        result += '\n[%s]' % elem
    return result


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

    def add_commented(self, content):
        self.add(Messages.PREFIX % content)

    def add_message(self, content, window_type=WindowTypes.INPUT):
        self.add_commented(Messages.HEADER)
        if window_type == WindowTypes.INPUT:
            self.add_commented(Messages.INPUT_INFO)
        elif window_type == WindowTypes.CASE:
            self.add_commented(Messages.CASE_INFO)
        for item in content:
            self.add_commented(item)
        self.add_commented(Messages.ENDING)


class ParserFormater():

    def __init__(self, teacher_performer):
        self.teacher_performer = teacher_performer

    def format(self, output, parser, parser_id, effect=False):
        parser._id = parser_id
        self._format_line_info(output, parser, effect)
        self._format_regexes(output, parser)
        self._format_line_others(output, parser)
        output.add(GlobalConsts.EMPTY_LINE)
        output.add(GlobalConsts.END_BRACKET)

    def _format_regexes(self, output, parser):
        output.add(POC.REGEX_HEAD % parser.pattern_name)
        output.add(parser.pattern)
        output.set_buttons_meta({
            BMC.PARSER: parser._id,
            BMC.FUNCTION: self.teacher_performer.edit_regex,
        })
        output.add(POC.REGEX_BUTTONS)
        output.set_buttons_meta({BMC.PARSER: parser._id})
        if self._regex_is_not_correct(parser.pattern, parser.line_content):
            output.add(WarningMessages.REGEX_NOT_MATCH)
        output.add(GlobalConsts.EMPTY_LINE)
        self._format_converters_(output, parser.groups, parser._id)
        output.add(GlobalConsts.EMPTY_LINE)

    def _format_converters_(self, output, groups, parser_id):
        for group in groups.keys():
            output.add(POC.GROUP_CONVERTER %
                (group, groups[group].converter, groups[group].content))
            output.set_buttons_meta({
                BMC.PARSER: parser_id,
                BMC.GROUP: group,
                BMC.FUNCTION: self.teacher_performer.edit_group,
            })

    def _format_line_info(self, output, parser, effect):
        output.add(POC.MESSAGE_CONTENT % (get_parser_name(parser._id), parser.line_content))
        output.set_buttons_meta({
            BMC.PARSER: parser._id,
            BMC.FUNCTION: self.teacher_performer.edit_content,
        })
        output.add(POC.META % (parser.line_resource_location, parser.line_offset))
        if not effect:
            output.add(POC.COPY_BUTTON)
            output.add(POC.DELETE_BUTTON)
            output.set_buttons_meta({BMC.PARSER: parser._id})
        output.add(GlobalConsts.EMPTY_LINE)

    def _format_line_others(self, output, parser):
        output.add(POC.OTHERS_HEAD)
        output.add(POC.LOG_TYPE % parser.log_type_name)
        output.set_buttons_meta({
            BMC.PARSER: parser._id,
            BMC.LOG_TYPE: parser.log_type_name,
            BMC.FUNCTION: self.teacher_performer.edit_log_type,
        })
        output.add(POC.PRIMARY_KEY % parser.primary_key_groups[0])
        output.set_buttons_meta({
            BMC.PARSER: parser._id,
            BMC.PRIMARY_KEY: parser.primary_key_groups[0],
            BMC.FUNCTION: self.teacher_performer.edit_primary_key_groups,
        })

    def _regex_is_not_correct(self, regex, line_content):
        return not re.match(re.compile(regex), line_content)

    def format_converters(self, output, groups, parser_id):
        for group in groups.keys():
            output.add(POC.GROUP_CONVERTER %
                (group, groups[group].converter, groups[group].content))
            output.set_buttons_meta({BMC.PARSER: parser_id, BMC.GROUP: group})

    def format_regexes_message(self, output, parser):
        output.add(POC.REGEX_HEAD % parser.pattern_name)
        output.add(parser.pattern)
        output.add(GlobalConsts.EMPTY_LINE)
        self.format_converters(output, parser.groups, parser._id)
        output.add(GlobalConsts.EMPTY_LINE)


class ConstraintsFormater():

    def __init__(self, teacher_proxy):
        self.teacher_proxy = teacher_proxy

    def _format_params(self, output, constraint):
        output.add(COC.PARAMS_HEADER)
        params = constraint.params
        for param in params.keys():
            output.add(COC.PARAM % (param, params[param]))
            output.set_buttons_meta({
                BMC.CONSTRAINT: constraint,
                BMC.PARAM: param,
            })

    def _format_single(self, output, constraint):
        output.add(COC.TYPE % constraint.type)
        output.set_buttons_meta({
            BMC.CONSTRAINT: constraint,
            BMC.FUNCTION: self.teacher_proxy.edit_constraint,
        })
        output.add(COC.CONSTR_BUTTONS)
        # TODO in this line should be constraint id
        output.set_buttons_meta({
            BMC.CONSTRAINT: constraint,
        })
        for group in constraint.groups:
            output.add(COC.GROUP % (get_parser_name(group[0]), group[1]))
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

    def format_constraint(self, output, constraint):
        output.add(COC.TYPE % constraint.type)
        output.set_buttons_meta({BMC.CONSTRAINT: constraint})
        for group in constraint.groups:
            output.add(COC.GROUP % (get_parser_name(group[0]), group[1]))
        if constraint.params:
            self._format_params(output, constraint)
        output.add(GlobalConsts.EMPTY_LINE)


class TeacherOutput():

    def __init__(self, teacher_proxy):
        self.parser = ParserFormater(teacher_proxy)
        self.constraint = ConstraintsFormater(teacher_proxy)
        self.teacher = teacher_proxy

    def _format_effect_line(self, output, raw_output, effect_id):
        self.parser.format(
                output,
                raw_output.parsers[effect_id],
                effect_id,
                effect=True,
            )

    def _format_causes(self, output, rule, effect_id):
        causes_lines = rule.parsers.keys()
        causes_lines.remove(effect_id)
        for line_id in causes_lines:
            self.parser.format(
                    output,
                    rule.parsers[line_id],
                    line_id,
                    effect=False,
                )

    def format_rule(self, rule_intent, message=None):
        output = OutputAgregator()
        output.add(GlobalConsts.MAIN_HEADER)
        effect_id = rule_intent.effect_id
        self._format_effect_line(output, rule_intent, effect_id)
        self._format_causes(output, rule_intent, effect_id)
        self.constraint.format(output, rule_intent.constraints)
        output.add(GlobalConsts.BUTTONS_HEADER)
        output.add(GlobalConsts.MAIN_BUTTONS)
        return output

    def format_param(self, param_key, param_value):
        return COC.PARAM_SIMPLE % (param_key, param_value)

    def format_comma(self, primary_key_groups):
        return ', '.join(map(str, primary_key_groups))

    def get_constraint_template(self, constraint_type):
        result = []
        result.append(COC.TYPE % constraint_type)
        result.append(COC.GROUP)
        result.append(COC.GROUP)
        result.append(GlobalConsts.EMPTY_LINE)
        result.append(COC.PARAMS_HEADER)
        result.append(COC.PARAM_SIMPLE % ('param_key', 'value'))
        return '\n'.join(result)

    def get_constraint_content(self, output, constraint):
        output.add(COC.TYPE % constraint.type)
        for group in constraint.groups:
            output.add(COC.GROUP % (get_parser_name(group[0]), group[1]))
        if constraint.params:
            output.add(COC.PARAMS_HEADER)
            for param in constraint.params.keys():
                output.add(COC.PARAM % (param, constraint.params[param]))

    def format_log_type(self, output, log_types):
        for log_type in log_types:
            output.add(LTC.NAME % log_type.name)
            output.set_buttons_meta({BMC.LOG_TYPE: log_type})
            for matcher in log_type._filename_matchers:
                output.add(LTC.HOST_PATTERN % matcher._host_pattern)
                output.set_buttons_meta({BMC.LOG_TYPE: log_type})
                output.add(LTC.PATH_PATTERN % matcher._path_pattern)
                output.set_buttons_meta({BMC.LOG_TYPE: log_type})
            output.add(GlobalConsts.EMPTY_LINE)
        output.add(LTC.ADD_LOGTYPE)
        output.set_buttons_meta({BMC.FUNCTION: self.teacher.new_log_type})
        output.add(LTC.CANCEL_LOGTYPE)
        output.set_buttons_meta({BMC.FUNCTION: self.teacher.reprint_teacher})
        return output

    def get_log_type_template(self):
        result = []
        result.append(LTC.NAME)
        result.append(LTC.HOST_PATTERN)
        result.append(LTC.PATH_PATTERN)
        return '\n'.join(result)
