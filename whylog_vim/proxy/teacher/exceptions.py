from whylog_vim.exceptions import WhylogVIMExceptions


class CannotGoToPosition(WhylogVIMExceptions):

    def __init__(self, position):
        self.position = position

    def __repr__(self):
        return 'Cannot go to byte %s in window' % self.position
