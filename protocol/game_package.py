class GamePackage:
    package: bytes

    def construct(self) -> bytes:
        raise NotImplementedError()

    def deconstruct(self, json: dict) -> bytes:
        raise NotImplementedError()
