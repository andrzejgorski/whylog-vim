from mock import MagicMock
from whylog_vim.proxy import WhylogProxy
from whylog_vim.consts import EditorStates as States


def tests_unit_check_log_reader_states_of_whylog_proxy():
    whylog_proxy = WhylogProxy(MagicMock())

    assert whylog_proxy.get_state() == States.EDITOR_NORMAL
    whylog_proxy.action()
    assert whylog_proxy.get_state() == States.LOG_READER
    whylog_proxy.action()
    assert whylog_proxy.get_state() == States.LOG_READER


def tests_unit_check_teacher_states_of_whylog_proxy():
    whylog_proxy = WhylogProxy(MagicMock())

    assert whylog_proxy.get_state() == States.EDITOR_NORMAL
    whylog_proxy.teach()
    assert whylog_proxy.get_state() == States.ADD_CAUSE
    whylog_proxy.teach()
    assert whylog_proxy.get_state() == States.TEACHER
