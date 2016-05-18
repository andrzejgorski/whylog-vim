import re
from whylog_vim.consts import Constraint, LogType


class Groups(object):
    GROUP_FST = 'content1'
    GROUP_SND = 'content2'


class Input(object):
    GROUP_FST = '(?P<%s>.+)' % Groups.GROUP_FST
    GROUP_SND = '(?P<%s>.+)' % Groups.GROUP_SND
    INT_GROUP_FST = '(?P<%s>\d+)' % Groups.GROUP_FST
    INT_GROUP_SND = '(?P<%s>\d+)' % Groups.GROUP_SND


def _regex_begin_end(prepare_function):
    def wrapper(pattern):
        return '^' + prepare_function(pattern) + '$'

    return wrapper


@_regex_begin_end
def _prepare_default(pattern):
    return pattern % Input.GROUP_FST


@_regex_begin_end
def _prepare_group(pattern):
    return pattern % (Input.GROUP_FST, Input.INT_GROUP_SND)


@_regex_begin_end
def _prepare_params(pattern):
    return pattern % (Input.GROUP_FST, Input.GROUP_SND)


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
