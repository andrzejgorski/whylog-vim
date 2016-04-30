class WhylogVIMExceptions(Exception):
    pass


class UnknownAction(WhylogVIMExceptions):

    def __init__(self, action_type, state):
        self.action_type = action_type
        self.state = state

    def __repr__(self):
        return 'Unknown action for argument name %s in states %s' % (self.action_type, self.state)
