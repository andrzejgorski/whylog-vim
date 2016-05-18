from whylog_vim.consts import LineNames


def get_parser_name(parser_id):
    if parser_id == 0:
        return LineNames.EFFECT
    else:
        return LineNames.CAUSE % parser_id


def get_id_from_name(name):
    if name == LineNames.EFFECT:
        return 0
    return int(name[LineNames.CAUSE_PREFIX:])
