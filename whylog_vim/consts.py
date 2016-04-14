

class WindowTypes():
    QUERY = 'whylog_query_output'
    TEACHER = 'whylog_teacher'
    INPUT = 'whylog_input'
    MESSAGE = 'whylog_message'
    CASE = 'whylog_case'


class GlobalConsts():
    BUTTONS_HEADER = '--- Buttons:'
    EMPTY_LINE = ''
    END_BRACKET = '<<<'
    MAIN_BUTTONS = '[save] [test_rule] [return_to_file] [give_up_rule]'
    MAIN_HEADER = '# You are using whylog teacher.'


class ButtonsMetaConsts():
    CONSTRAINT = 'constraint'
    CONSTRAINT_GROUP = 'constraint_group'
    GROUP = 'group_id'
    LOG_TYPE = 'log_type'
    PARAM = 'param'
    PARSER = 'parser_id'
    PRIMARY_KEY = 'primary_key'
    BUTTON = 'button'
    FUNCTION = 'function'


class ParserOutputConsts():
    GROUP_CONVERTER = 'group %s: %s, match: %s'
    LINE_BUTTONS = '[copy_line] [delete_line]'
    LOG_TYPE = 'log type: %s'
    MESSAGE_CONTENT = '=== %s %s: %s'
    META = 'file: %s, offset: %s'
    OTHERS_HEAD = '--- Other:'
    PRIMARY_KEY = 'primary key groups: %s'
    REGEX_BUTTONS = '[guess_regex]'
    REGEX_HEAD = '--- Regex: %s'
    LINE_CONTENT = '--- Line %s: %s'


class ConstraintsOutputConsts():
    BUTTONS = '[add_constraint]'
    CONSTR_BUTTONS = '[delete_constraint] [add_param]'
    GROUP = 'parser: %s, group: %s'
    HEADER = '=== Rule Constraints:'
    PARAM = '%s: %s'
    PARAMS_HEADER = '--- Params:'
    TYPE = '--- Constraint: %s'
    PARAM_SIMPLE = '%s: %s'


class LogTypeConsts():
    NAME = '--- name: %s'
    HOST_PATTERN = 'host pattern: %s'
    PATH_PATTERN = 'path pattern: %s'
    FILE_NAME_MATCHER = 'file name matcher: %s'
    ADD_LOGTYPE = '[add_log_type]'


class Messages():
    CAUSE = 'cause line'
    EFFECT = 'effect line'


class WarningMessages():
    REGEX_NOT_MATCH = '!! Warning Message: Regex doen\'t match to the line.!!'


class Input():
    EMPTY_GROUP = '(?P<content>.+)'
    GROUP1 = '(?P<content1>.+)'
    GROUP2 = '(?P<content2>.+)'
    INT_GROUP1 = '(?P<int1>\d+)'
    INT_GROUP2 = '(?P<int2>\d+)'
