
# Originator Class - Vote Storage
class Originator():
    _state = None

    def __init__(self, state):
        self._state = state

    def save(self, state):
        return Memento(state)

    def restore(self, memento):
        self._state = memento.get_state()

class Memento():
    _state = None

    def __init__(self, state):
        self._state = state

    def get_state(self):
        return self._state
