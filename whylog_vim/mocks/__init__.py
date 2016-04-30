from whylog import LogType, WildCardFilenameMatcher


def converter_returner():
    return ['string', 'to_date', 'int', 'float']


def log_type_returner():
    matchers1 = [WildCardFilenameMatcher('localhost', '^.*.path$', 'lala')]
    matchers2 = [WildCardFilenameMatcher('localhost', '^.*.path$', 'lala'), WildCardFilenameMatcher('localhost', '^.*.log$', 'lala')]
    matchers3 = []
    return [
        LogType('hydra', matchers1),
        LogType('filesystem', matchers2),
        LogType('dummy_log_type', matchers3),
    ]


def constraint_returner():
    return [
        'indentical',  # no params
        'different',  # no params
        'value_delta',  # max, min
        'hetero_constraint',  # different
        'time_delta',  # delta
    ]
