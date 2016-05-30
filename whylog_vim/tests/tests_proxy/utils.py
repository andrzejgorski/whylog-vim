from mock import MagicMock

from whylog import FrontInput, LineSource


class TestConsts(object):
    LINE = '000 line content'
    REGEX = '\d0\d line content'


def create_mock_editor():
    mock_editor = MagicMock()
    mock_editor.get_front_input.return_value = FrontInput(
        1, TestConsts.LINE, LineSource('host', 'path')
    )
    return mock_editor
