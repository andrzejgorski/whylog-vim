from whylog_vim.proxy import WhylogProxy
from whylog_vim.gui import VimEditor


whylog = WhylogProxy(VimEditor())


def whylog_1():
    whylog.signal_1()


def whylog_2():
    whylog.signal_2()
