import re


class Input(object):
    EMPTY_GROUP = '(?P<content>.+)'
    GROUP1 = '(?P<content1>.+)'
    GROUP2 = '(?P<content2>.+)'
    INT_GROUP1 = '(?P<int1>\d+)'
    INT_GROUP2 = '(?P<int2>\d+)'


class RegexPatterns(object):
    COMMENTS = re.compile('^# .*$')
    BUTTON = re.compile('\[[^[^[]*\]')
