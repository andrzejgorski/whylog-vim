from whylog_vim.exceptions import WhylogVimExceptions


class CannotGoToPosition(WhylogVimExceptions):

    def __init__(self, position):
        self.position = position

    def __repr__(self):
        return 'Cannot go to byte %s in window' % self.position
