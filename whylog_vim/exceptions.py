class WhylogVIMExceptions():
    pass


class UnknownAction(WhylogVIMExceptions):

    def __init__(self, move_type, state):
        self.move_type = move_type
        self.state = state

    def __repr__(self):
        'Unknown action for %s in states %s' % (self.move_type, self.state)
