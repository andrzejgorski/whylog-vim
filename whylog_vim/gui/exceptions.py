from whylog_vim.exceptions import WhylogVimException


class WindowException(WhylogVimException):
    def __init__(self, window_type):
        self.window_type = window_type


class CannotCloseWindow(WindowException):
    def __repr__(self):
        return 'Cannot close the window %s' % self.window_type


class CannotFindWindowId(WindowException):
    def __repr__(self):
        return 'Cannot find id of the window %s' % self.window_type


class CannotGetWindowContent(WindowException):
    def __repr__(self):
        return 'Cannot get content of the window %s' % self.window_type


class CannotSetWindowContent(WindowException):
    def __repr__(self):
        return 'Cannot set content of the window %s' % self.window_type


class CannotSwitchToWindow(WindowException):
    def __repr__(self):
        return 'Cannot switch to the window %s' % self.window_type
