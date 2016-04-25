import re
from whylog.config.log_type import LogType
from whylog.config.filename_matchers import RegexFilenameMatcher
from whylog_vim.consts import ButtonsMetaConsts as BMC, LogTypeConsts as LTC, Input, ConstraintsOutputConsts as COC


def get_button_name(line, offset):
    offset -= 1
    for match in re.finditer(re.compile("\[[^[^[]*\]"), line):
        if offset >= match.start(0) and offset < match.end(0):
            return match.group(0)[1:-1]
    else:
        return None


def prepare_regex(pattern):
    return ('^' + pattern + '$') % Input.EMPTY_GROUP


def parse_log_type(lines):
    # TODO catche errors
    pattern = re.compile(prepare_regex(LTC.NAME))
    name = pattern.match(lines[0]).group(1)
    pattern = re.compile(prepare_regex(LTC.HOST_PATTERN))
    host_pattern = pattern.match(lines[1]).group(1)
    pattern = re.compile(prepare_regex(LTC.PATH_PATTERN))
    path_pattern = pattern.match(lines[2]).group(1)
    matcher = RegexFilenameMatcher(host_pattern, path_pattern, name)
    return LogType(name, matcher)


def parse_primary_key_groups(content):
    return map(int, content[0].split(', '))


def parse_constraint_group(content):
    result = content[0].split(', ')
    if len(result) == 2:
        return map(int, result)
    else:
        # TODO add parse exceptions WhylogVIMParseExceptions
        raise Exception()


def parse_param(content):
    return content[0].split(': ')


def parse_constraint(lines):
    # TODO Add errors handler
    pattern = re.compile(prepare_regex(COC.TYPE))
    constr_type = pattern.match(lines[0]).group(1)
    regex = '^' + COC.GROUP % (Input.INT_GROUP1, Input.INT_GROUP2) + '$'
    pattern = re.compile(regex)
    groups = []
    for line in range(1, len(lines)):
        match = pattern.match(lines[line])
        # print line
        if match:
            groups.append((match.group('int1'), match.group('int2')))
        else:
            go_line = line + 1
            break
        # print line, lines[line]
    else:
        return constr_type, groups, {}

    pattern = re.compile('^' + COC.PARAMS_HEADER + '$')
    while pattern.match(lines[go_line]):
        go_line += 1

    pattern = re.compile('^' + COC.PARAM_SIMPLE % (Input.GROUP1, Input.GROUP2) + '$')

    params = {}
    match = pattern.match(lines[go_line])
    # print lines[go_line], match
    while match:
        params[match.group('content1')] = match.group('content2')
        go_line += 1
        if go_line >= len(lines):
            break
        match = pattern.match(lines[go_line])

    return constr_type, groups, params


class LogTypeLoader():

    def __init__(self, log_type_menu, get_line_number, set_return_function):
        self.log_type_menu = log_type_menu
        self.get_line_number = get_line_number
        self.set_return_function = set_return_function

    def __call__(self):
        button_meta = self.log_type_menu.get_button_meta(self.get_line_number())
        if BMC.LOG_TYPE in button_meta:
            return button_meta[BMC.LOG_TYPE]

        if BMC.FUNCTION in button_meta:
            self.set_return_function(button_meta[BMC.FUNCTION])


def filter_comments(content):
    result = []
    pattern = re.compile('^# .*$')
    for line in content:
        if not pattern.match(line):
            result.append(line)
    return result


class GetInputContentLoader():

    def __init__(self, get_input_content):
        self.get_input_content = get_input_content

    def __call__(self):
        raise NotImplemented()


class NewLogTypeLoader(GetInputContentLoader):

    def __call__(self):
        return parse_log_type(self.get_input_content())


class PrimaryKeyLoader(GetInputContentLoader):

    def __call__(self):
        return parse_primary_key_groups(self.get_input_content())


class ConstraintLoader(GetInputContentLoader):

    def __call__(self):
        return parse_constraint(self.get_input_content())


class ParseParamLoader(GetInputContentLoader):

    def __call__(self):
        return parse_param(self.get_input_content())


class ConstraintGroupLoader(GetInputContentLoader):

    def __call__(self):
        return parse_constraint_group(self.get_input_content())
