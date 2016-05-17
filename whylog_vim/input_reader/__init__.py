import re
from whylog_vim.input_reader.consts import Input, RegexPatterns

class InputReader():
    @classmethod
    def filter_comments(cls, content):
        return [line for line in content if not RegexPatterns.COMMENTS.match(line)]

    @classmethod
    def get_button_name(cls, line, offset):
        offset -= 1
        for match in re.finditer(RegexPatterns.BUTTON, line):
            if offset >= match.start(0) and offset < match.end(0):
                return match.group(0)[1:-1]

    @classmethod
    def _prepare_regex(cls, pattern):
        return ('^' + pattern + '$') % Input.EMPTY_GROUP

    @classmethod
    def parse_log_type(cls, lines):
        # TODO catche errors
        pattern = re.compile(cls._prepare_regex(LTC.NAME))
        name = pattern.match(lines[0]).group(1)
        pattern = re.compile(cls._prepare_regex(LTC.HOST_PATTERN))
        host_pattern = pattern.match(lines[1]).group(1)
        pattern = re.compile(cls._prepare_regex(LTC.PATH_PATTERN))
        path_pattern = pattern.match(lines[2]).group(1)
        matcher = RegexFilenameMatcher(host_pattern, path_pattern, name)
        return LogType(name, matcher)

    @classmethod
    def parse_primary_key_groups(cls, content):
        return map(int, content[0].split(', '))

    @classmethod
    def parse_constraint(cls, lines):
        # TODO Add errors handler
        pattern = re.compile(cls._prepare_regex(COC.TYPE))
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
