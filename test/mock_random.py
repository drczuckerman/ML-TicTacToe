class MockRandom(object):
    def __init__(self, choice_index):
        self.choice_index = choice_index

    def choice(self, choices):
        return choices[self.choice_index]
