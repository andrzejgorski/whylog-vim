from whylog_vim.consts import LineNames


def get_parser_name(id_):
    if id_ == 0:
        return LineNames.EFFECT
    else:
        return LineNames.CAUSE % id_


def get_id_from_name(name):
    if name == LineNames.EFFECT:
        return 0
    return int(name[6:])
