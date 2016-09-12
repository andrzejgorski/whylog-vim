from mock import MagicMock

from whylog import FrontInput, LineSource, LogType
from whylog.config.filename_matchers import WildCardFilenameMatcher
from whylog.config.super_parser import RegexSuperParser

from whylog_vim.proxy import WhylogProxy


class TestConsts(object):
    LINE = '000 line content'
    REGEX = '(\d+) line content'
    NEW_LOG_TYPE = 'new_log_type'
    DEFAULT_LOG_TYPE = 'default'


class MocksForProxy(object):
    @classmethod
    def mock_log_types(cls):
        log_type_names = [TestConsts.NEW_LOG_TYPE, TestConsts.DEFAULT_LOG_TYPE]
        return [cls.create_mocked_log_type(name) for name in log_type_names]

    @classmethod
    def create_mocked_log_type(cls, log_type_name):
        super_parser = RegexSuperParser('^(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d).*', [1], {1: 'date'})
        matcher = WildCardFilenameMatcher('localhost', 'node_1.log', 'default', super_parser)
        return LogType(log_type_name, [matcher])

    @classmethod
    def create_line_source(cls):
        return LineSource('host', 'path')

    @classmethod
    def create_whylog_proxy(cls, editor):
        whylog_proxy = WhylogProxy(editor)
        whylog_proxy.log_types = {
            cls.create_line_source(): cls.create_mocked_log_type(TestConsts.NEW_LOG_TYPE)
        }
        return whylog_proxy

    @classmethod
    def create_mock_editor(cls):
        mock_editor = MagicMock()
        mock_editor.get_front_input.return_value = FrontInput(
            1, TestConsts.LINE, cls.create_line_source()
        )
        mock_editor.get_line_source.return_value = cls.create_line_source()
        return mock_editor
