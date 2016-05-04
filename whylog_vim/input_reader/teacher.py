from whylog_vim.input_reader import RegexPatterns


def parse_log_type(lines):
    name = RegexPatterns.LOGTYPE_NAME.match(lines[0]).group(1)
    host_pattern = RegexPatterns.HOST_PATTERN.match(lines[1]).group(1)
    path_pattern = RegexPatterns.PATH_PATTERN.match(lines[2]).group(1)
    matcher = RegexFilenameMatcher(host_pattern, path_pattern, name)
    return LogType(name, matcher)


def parse_primary_key_groups(content):
    return map(int, content[0].split(', '))
