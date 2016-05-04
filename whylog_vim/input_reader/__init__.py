import re
from whylog_vim.input_reader.consts import Input


def filter_comments(content):
    result = []
    pattern = re.compile('^# .*$')
    for line in content:
        if not pattern.match(line):
            result.append(line)
    return result


def get_button_name(line, offset):
    offset -= 1
    for match in re.finditer(re.compile("\[[^[^[]*\]"), line):
        if offset >= match.start(0) and offset < match.end(0):
            return match.group(0)[1:-1]
    else:
        return None


def prepare_regex(pattern):
    return ('^' + pattern + '$') % Input.EMPTY_GROUP
