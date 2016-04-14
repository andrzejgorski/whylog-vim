from whylog.config.log_type import LogType


def converter_returner():
    return ['string', 'data', 'int', 'float']


def log_type_returner():
    return [
        LogType('hydra', None, 'localhost', '.*\.log'),
        LogType('filesystem', None, 'localhost', '.*\.log'),
        LogType('dummy_log_type', None, 'localhost', '.*\.log'),
    ]


def constraint_returner():
    return [
        'indentical',  # no params
        'different',  # no params
        'value_delta',  # max, min
        'hetero_constraint',  # different
        'time_delta',  # delta
    ]
