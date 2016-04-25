

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
    MESSAGE_CONTENT = '=== %s: %s'
    META = 'file: %s, offset: %s'
    OTHERS_HEAD = '--- Other:'
    PRIMARY_KEY = 'primary key groups: %s'
    REGEX_BUTTONS = '[guess_regex]'
    REGEX_HEAD = '--- Regex: %s'
    LINE_CONTENT = '--- Line %s: %s'

    EFFECT_LINE_NAME = 'effect'
    CAUSE_LINE_NAME = 'cause_%s'


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
    CANCEL_LOGTYPE = '[cancel]'


class Messages():
    PREFIX = '# %s'
    HEADER = 'This is whylog input window.'
    ENDING = 'Do not change the commented text above.'
    INPUT_INFO = 'Enter the content below commented block and press <F3>.'
    CASE_INFO = 'Select an option and press <F3>'
    CONVERER = 'This is the match of the group: %s'
    REGEX = 'This is the content of the line:'
    LOGTYPE = 'This is the content and path of the line:'
    PRIMARY_KEY = 'This is the content and path of the line:'


class WarningMessages():
    REGEX_NOT_MATCH = '!! Warning Message: Regex doen\'t match to the line.!!'


class Input():
    EMPTY_GROUP = '(?P<content>.+)'
    GROUP1 = '(?P<content1>.+)'
    GROUP2 = '(?P<content2>.+)'
    INT_GROUP1 = '(?P<int1>\d+)'
    INT_GROUP2 = '(?P<int2>\d+)'


class MainStates():
    # Editor states
    EDITOR_NORMAL = 'editor normal'
    LOG_READER = 'query'
    TEACHER = 'teacher menu'
    ADD_CAUSE = 'add cause'
    TEACHER_INPUT = 'input window'
    EFFECT_ADDED = 'added effect'


class WindowSizes():
    MAX_MESSAGE_SIZE = 20


class ActionTypes():
    STANDARD = 'standard action'
    TEACHER = 'teacher action'
