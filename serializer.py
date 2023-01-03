from jsonpickle import dumps, loads


class BaseSerializer:
    """Базовый сериализатор"""

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)
