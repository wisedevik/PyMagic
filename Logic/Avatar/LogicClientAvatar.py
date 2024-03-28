from DataStream.ChecksumEncoder import ChecksumEncoder
from Logic.LogicBase import LogicBase
from Logic.Long.LogicLong import LogicLong

class LogicClientAvatar(LogicBase):
    def __init__(self) -> None:
        super().__init__()

        self.resources = [3000001, 3000002, 3000003] # resources list
        self.tutorialSteps = list(range(21000000, 21000013)) # tutorial steps list

    def encode(self, encoder: ChecksumEncoder):
        super().encode(encoder)

        encoder.writeLong(LogicLong(1, 1))
        encoder.writeLong(LogicLong(1, 1))
        encoder.writeBoolean(False)
        encoder.writeBoolean(False)
        encoder.writeBoolean(False)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeString("Name") # Name
        encoder.writeString("")
        encoder.writeInt(1)
        encoder.writeInt(0)
        encoder.writeInt(2147483647) # Diamonds
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeBoolean(False)
        encoder.writeInt(0)

        encoder.writeInt(0)
        encoder.writeInt(len(self.resources))
        for item in self.resources:
            encoder.writeInt(item)
            encoder.writeInt(2147483647)

        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)

        encoder.writeInt(len(self.tutorialSteps)) # skip tutorial
        for item in self.tutorialSteps:
            encoder.writeInt(item)

        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
        encoder.writeInt(0)
