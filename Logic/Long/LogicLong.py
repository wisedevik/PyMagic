class LogicLong:
    def __init__(self, highInteger: int = 0, lowInteger: int = 0) -> None:
        self.highInteger = highInteger
        self.lowInteger = lowInteger

    def decode(self, stream) -> None:
        self.highInteger = stream.readInt()
        self.lowInteger = stream.readInt()

    def encode(self, encoder) -> None:
        encoder.writeInt(self.highInteger)
        encoder.writeInt(self.lowInteger)

    def toString(self) -> str:
        return "{0}-{1}".format(self.highInteger, self.lowInteger)