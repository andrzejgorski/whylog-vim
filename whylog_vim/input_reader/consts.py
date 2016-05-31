import re
from whylog_vim.consts import Constraint, LogType


class Groups(object):
    GROUP1 = 'content1'
    GROUP2 = 'content2'


class Input(object):
    GROUP1 = '(?P<%s>.+)' % Groups.GROUP1
    GROUP2 = '(?P<%s>.+)' % Groups.GROUP2
    INT_GROUP1 = '(?P<%s>\d+)' % Groups.GROUP1
    INT_GROUP2 = '(?P<%s>\d+)' % Groups.GROUP2


def _regex_begin_end(prepare_function):
    def wrapper(pattern):
        return '^' + prepare_function(pattern) + '$'

    return wrapper


@_regex_begin_end
def _prepare_default(pattern):
    return pattern % Input.GROUP1


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
    PARAMS_HEADER = re.compile(Constraint.PARAMS_HEADER)
