import re
from whylog_vim.input_reader.consts import Input, RegexPatterns


def filter_comments(content):
    pattern = re.compile(RegexPatterns.COMMENTS)
    return [line for line in content if not pattern.match(line)]


def get_button_name(line, offset):
    offset -= 1
    for match in re.finditer(re.compile(RegexPatterns.BUTTON), line):
        if offset >= match.start(0) and offset < match.end(0):
            return match.group(0)[1:-1]
    return None


def prepare_regex(pattern):
    return ('^' + pattern + '$') % Input.EMPTY_GROUP
