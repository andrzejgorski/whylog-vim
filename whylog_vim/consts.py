class WindowTypes(object):
    QUERY = 'whylog_query_output'
    TEACHER = 'whylog_teacher'
    INPUT = 'whylog_input'
    MESSAGE = 'whylog_message'
    CASE = 'whylog_case'


class WindowSizes(object):
    QUERY_WINDOW = 10


class Messages(object):
    COMMENT_PREFIX = '# %s'
    TEACHER_HEADER = 'You are using whylog teacher.'
    INPUT_HEADER = 'This is whylog input window.'
    ENDING = 'Do not change the commented text above.'
    INPUT_INFO = 'Enter the content below the commented block and press <F3>.'
    CASE_INFO = 'Select an option and press <F3>'
    CONVERTER = 'This is the match of the group: %s'
    REGEX = 'This is the content of the line:'
    LOGTYPE = 'This is the content and path of the line:'
    PRIMARY_KEY = 'This is the content and path of the line:'
    ADDED_EFFECT = '### WHYLOG ### You added line as effect. Select cause and press <F4>.'
    EMPTY_DATABASE = 'There is nothing in database. Add rules to get queries.'


class EditorStates(object):
    EDITOR_NORMAL = 'editor normal'
    LOG_READER = 'query'
    TEACHER = 'teacher menu'
    ADD_CAUSE = 'add cause'
    TEACHER_INPUT = 'input window'
    EFFECT_ADDED = 'added effect'


class ActionTypes(object):
    STANDARD = 'standard action'
    TEACHER = 'teacher action'


class ParserOutputs(object):
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


class ConstraintsOutputs(object):
    ADD_BUTTON = '[add_constraint]'
    DELETE_BUTTON = '[delete_constraint]'
    GROUP = 'line: %s, group: %s'
    HEADER = '=== Rule Constraints:'
    PARAM = '%s: %s'
    PARAMS_HEADER = 'params:'
    TYPE = '--- Constraint: %s'


class Constraint(object):
    ADD_BUTTON = 'add_constraint'
    DELETE_BUTTON = 'delete_constraint'
    GROUP = 'line: %s, group: %s'
    HEADER = '=== Rule Constraints:'
    PARAM = '%s: %s'
    PARAMS_HEADER = 'params:'
    TYPE = '--- Constraint: %s'


class LogType(object):
    NAME = '--- name: %s'
    HOST_PATTERN = 'host pattern: %s'
    PATH_PATTERN = ' path pattern: %s'
    FILE_NAME_MATCHER = 'file name matcher: %s'
    ADD_BUTTON = 'add_log_type'
    CANCEL_BUTTON = 'cancel'


class LineNames(object):
    EFFECT = 'effect'
    CAUSE = 'cause_%s'
    CAUSE_PREFIX = 6


class Templates(object):
    READ_ERROR = '! Error ! %s'


class ReadMessages(object):
    TOO_MANY_LINES = Templates.READ_ERROR % 'You can put only single line as content of parser.'
