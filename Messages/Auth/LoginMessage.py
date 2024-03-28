from Messages.PiranhaMessage import PiranhaMessage
from Logic.Long.LogicLong import LogicLong

class LoginMessage(PiranhaMessage):
    def __init__(self) -> None:
        super().__init__(0)
        self.accountId: LogicLong = LogicLong()

        self.passToken: str = ""
        self.clientMajorVersion: int = -1
        self.clientBuild: int = -1
        self.resourceSha: str = ""

    def decode(self):
        super().decode()

        # Account id
        self.accountId = self.stream.readLong()

        self.passToken = self.stream.readString()
        self.clientMajorVersion = self.stream.readInt()
        self.stream.readInt()
        self.clientBuild = self.stream.readInt()
        self.resourceSha = self.stream.readString()

    def getMessageType(self) -> int:
        return 10101