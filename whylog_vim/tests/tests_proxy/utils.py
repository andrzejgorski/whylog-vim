from mock import MagicMock

import six

from whylog import FrontInput, LineSource


def create_mock_editor():
    mock_editor = MagicMock()
    mock_editor.get_front_input.return_value = FrontInput(
        1, 'line content', LineSource('host', 'path')
    )
    return mock_editor


def skipIf(condition, message):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            if condition:
                function(args, **kwargs)
            else:
                six.print_(message)

        return wrapper

    return real_decorator
