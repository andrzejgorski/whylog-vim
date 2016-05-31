from mock import MagicMock

from whylog import FrontInput, LineSource, LogType
from whylog_vim.proxy import WhylogProxy


class TestConsts(object):
    LINE = '000 line content'
    REGEX = '\d0\d line content'


def create_line_source():
    return LineSource('host', 'path')


def create_whylog_proxy(editor):
    whylog_proxy = WhylogProxy(editor)
    whylog_proxy.log_types = {create_line_source(): LogType('some log type', [])}
    return whylog_proxy


def create_mock_editor():
    mock_editor = MagicMock()
    mock_editor.get_front_input.return_value = FrontInput(1, TestConsts.LINE, create_line_source())
    mock_editor.get_line_source.return_value = create_line_source()
    return mock_editor
