

class GlobalConsts():
    BUTTONS_HEADER = '=== Buttons:'
    EMPTY_LINE = ''
    END_BRACKET = '<<<'
    MAIN_BUTTONS = '[save] [test_rule] [return_to_file] [give_up_rule]'
    MAIN_HEADER = '# You are using whylog teacher.'


class ButtonsMetaConsts():
    CONSTRAINT = 'constraint'
    GROUP = 'group'
    LOG_TYPE = 'log_type'
    PARAM = 'param'
    PARSER = 'parser'
    PRIMARY_KEY = 'primary_key'


class ParserOutputConsts():
    GROUP_CONVERTER = '[edit] group_converter %s: %s, match: %s'
    LINE_BUTTONS = '[edit_content] [copy_line] [delete_line]'
    LOG_TYPE = '[edit] log type name: %s'
    MESSAGE_CONTENT = '=== %s %s: %s'
    META = 'file: %s, offset: %s'
    OTHERS_HEAD = '--- Other:'
    PRIMARY_KEY = '[edit] primary key groups: %s'
    REGEX_BUTTONS = '[edit_regex_name] [edit_regex] [guess_regex]'
    REGEX_HEAD = '--- Regex: %s'


class ConstraintsOutputConsts():
    BUTTONS = '[add_constraint]'
    CONSTR_BUTTONS = '[delete_constraint] [add_param]'
    GROUP = '[edit] parser <%s> group <%s>'
    HEADER = '=== Rule Constraints:'
    PARAM = '[edit] param %s: %s'
    PARAMS_HEADER = '--- Params:'
    TYPE = '--- Constraint: %s'


class Messages():
    CAUSE = 'cause line'
    EFFECT = 'effect line'


def get_constraint_template():
    result = []
    result.append(ConstraintsOutputConsts.TYPE)
    result.append(ConstraintsOutputConsts.GROUP)
    result.append(ConstraintsOutputConsts.GROUP)
    result.append(GlobalConsts.EMPTY_LINE)
    result.append(ConstraintsOutputConsts.PARAMS_HEADER)
    result.append(ConstraintsOutputConsts.PARAM)
    return '\n'.join(result)
