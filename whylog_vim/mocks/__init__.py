from whylog.config.log_type import LogType
from whylog.config.filename_matchers import RegexFilenameMatcher


def converter_returner():
    return ['string', 'data', 'int', 'float']


def log_type_returner():
    matchers1 = [RegexFilenameMatcher('localhost', '^.*.path$', 'lala')]
    matchers2 = [RegexFilenameMatcher('localhost', '^.*.path$', 'lala'), RegexFilenameMatcher('localhost', '^.*.log$', 'lala')]
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
