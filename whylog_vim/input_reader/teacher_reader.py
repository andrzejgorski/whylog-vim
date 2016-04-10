import re
from whylog_vim.consts import ButtonsMetaConsts as BMC


def get_button_name(line, offset):
    offset -= 1
    for match in re.finditer(re.compile("\[[^[^[]*\]"), line):
        if offset >= match.start(0) and offset < match.end(0):
            return match.group(0)[1:-1]
    else:
        return None
