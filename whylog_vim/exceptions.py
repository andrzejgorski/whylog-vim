class WhylogVimException(Exception):
    pass


class UnknownAction(WhylogVimException):
    def __init__(self, action_type, state):
        self.action_type = action_type
        self.state = state

    def __repr__(self):
        return 'Unknown action for action type %s in states %s' % (
            self.action_type, self.state)
