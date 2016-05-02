

class WindowTypes():
    QUERY = 'whylog_query_output'
    TEACHER = 'whylog_teacher'
    INPUT = 'whylog_input'
    MESSAGE = 'whylog_message'
    CASE = 'whylog_case'


class TeacherConsts():
    BUTTONS_HEADER = '--- Buttons:'
    EMPTY_LINE = ''
    END_BRACKET = '<<<'
    ABANDON_BUTTON = '[abandon_rule]'
    VERIFY_BUTTON = '[verify_rule]'
    RETURN_BUTTON = '[return_to_file]'
    SAVE_BUTTON = '[save]'


class ButtonsMetaConsts():
    CONSTRAINT = 'constraint'
    CONSTRAINT_GROUP = 'constraint_group'
    GROUP = 'group_id'
    LOG_TYPE = 'log_type'
    PARAM = 'param'
    PARSER = 'line_id'
    PRIMARY_KEY = 'primary_key'
    BUTTON = 'button'
    FUNCTION = 'function'


class ParserOutputConsts():
    GROUP_CONVERTER = 'group %s: %s, match: %s'
    COPY_BUTTON = '[copy_line]'
    DELETE_BUTTON = '[delete_line]'
    LOG_TYPE = 'log type: %s'
    MESSAGE_CONTENT = '=== %s: %s'
    META = 'file: %s, offset: %s'
    OTHERS_HEADER = '--- Other:'
    PRIMARY_KEY = 'primary key groups: %s'
    GUESS_BUTTON = '[guess_regex]'
    REGEX_HEADER = '--- Regex: %s'
    LINE_CONTENT = '--- Line %s: %s'

    EFFECT_LINE_NAME = 'effect'
    CAUSE_LINE_NAME = 'cause_%s'


class ConstraintsOutputConsts():
    ADD_BUTTON = '[add_constraint]'
    DELETE_BUTTON = '[delete_constraint]'
    GROUP = 'line: %s, group: %s'
    HEADER = '=== Rule Constraints:'
    PARAM = '%s: %s'
    PARAMS_HEADER = 'params:'
    TYPE = '--- Constraint: %s'


class LogTypeConsts():
    NAME = '--- name: %s'
    HOST_PATTERN = 'host pattern: %s'
    PATH_PATTERN = ' path pattern: %s'
    FILE_NAME_MATCHER = 'file name matcher: %s'
    ADD_LOGTYPE = '[add_log_type]'
    CANCEL_LOGTYPE = '[cancel]'


class Messages():
    PREFIX = '# %s'
    TEACHER_HEADER = 'You are using whylog teacher.'
    INPUT_HEADER = 'This is whylog input window.'
    ENDING = 'Do not change the commented text above.'
    INPUT_INFO = 'Enter the content the below commented block and press <F3>.'
    CASE_INFO = 'Select an option and press <F3>'
    CONVERTER = 'This is the match of the group: %s'
    REGEX = 'This is the content of the line:'
    LOGTYPE = 'This is the content and path of the line:'
    PRIMARY_KEY = 'This is the content and path of the line:'


class WarningMessages():
    REGEX_NOT_MATCH = '!! Warning Message: Regex doesn\'t match to the line.!!'


class Input():
    EMPTY_GROUP = '(?P<content>.+)'
    GROUP1 = '(?P<content1>.+)'
    GROUP2 = '(?P<content2>.+)'
    INT_GROUP1 = '(?P<int1>\d+)'
    INT_GROUP2 = '(?P<int2>\d+)'


class EditorStates():
    EDITOR_NORMAL = 'editor normal'
    LOG_READER = 'query'
    TEACHER = 'teacher menu'
    ADD_CAUSE = 'add cause'
    TEACHER_INPUT = 'input window'
    EFFECT_ADDED = 'added effect'


class WindowSizes():
    QUERY_WINDOW = 10


class ActionTypes():
    STANDARD = 'standard action'
    TEACHER = 'teacher action'
