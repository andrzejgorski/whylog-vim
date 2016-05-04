import re
from whylog.input_reader import prepare_regex
from whylog.consts import LogTypeConsts


class Input(object):
    EMPTY_GROUP = '(?P<content>.+)'
    GROUP1 = '(?P<content1>.+)'
    GROUP2 = '(?P<content2>.+)'
    INT_GROUP1 = '(?P<int1>\d+)'
    INT_GROUP2 = '(?P<int2>\d+)'


class RegexPatterns(object):
    COMMENTS = re.compile('^# .*$')
    BUTTON = re.compile('\[[^[^[]*\]')
    LOGTYPE_NAME = re.compile(prepare_regex(LogTypeConsts.NAME))
    HOST_PATTERN = re.compile(prepare_regex(LogTypeConsts.HOST_PATTERN))
    PATH_PATTERN = re.compile(prepare_regex(LogTypeConsts.PATH_PATTERN))
