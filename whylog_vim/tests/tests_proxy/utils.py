import six
from mock import MagicMock

from whylog import FrontInput, LineSource


def create_mock_editor():
    mock_editor = MagicMock()
    mock_editor.get_front_input.return_value = FrontInput(
        1, 'line content', LineSource('host', 'path')
    )
    return mock_editor
