import re
from whylog_vim.consts import LogType, Constraint


class Input(object):
    EMPTY_GROUP = '(?P<content>.+)'
    GROUP1 = '(?P<content1>.+)'
    GROUP2 = '(?P<content2>.+)'
    INT_GROUP1 = '(?P<int1>\d+)'
    INT_GROUP2 = '(?P<int2>\d+)'


def _regex_begin_end(func):
    def wrapper(pattern):
        return '^' + func(pattern) + '$'

    return wrapper


@_regex_begin_end
def _prepare_default(pattern):
    return pattern % Input.EMPTY_GROUP


@_regex_begin_end
def _prepare_group(pattern):
    return pattern % (Input.GROUP1, Input.INT_GROUP2)


@_regex_begin_end
def _prepare_params(pattern):
    return pattern % (Input.GROUP1, Input.GROUP2)


class RegexPatterns(object):
    COMMENTS = re.compile('^# .*$')
    BUTTON = re.compile('\[[^[^[]*\]')


class LogTypeInput(object):
    NAME = re.compile(_prepare_default(LogType.NAME))
    HOST = re.compile(_prepare_default(LogType.HOST_PATTERN))
    PATH = re.compile(_prepare_default(LogType.PATH_PATTERN))


class ConstraintInput(object):
    TYPE = re.compile(_prepare_default(Constraint.TYPE))
    GROUP = re.compile(_prepare_group(Constraint.GROUP))
    PARAM = re.compile(_prepare_params(Constraint.PARAM))
    PARAMS_HEADER = Constraint.PARAMS_HEADER
