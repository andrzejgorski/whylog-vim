from whylog_vim.proxy import WhylogProxy
from whylog_vim.gui import VimEditor


whylog = WhylogProxy(VimEditor())


def whylog_action():
    whylog.action()


def whylog_teach():
    whylog.teach()
