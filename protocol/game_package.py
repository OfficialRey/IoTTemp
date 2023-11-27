class GamePackage:

    def construct(self):
        raise NotImplementedError()

    def deconstruct(self, json: dict):
        raise NotImplementedError()
