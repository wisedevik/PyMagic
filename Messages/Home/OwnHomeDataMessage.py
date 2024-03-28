from Messages.PiranhaMessage import PiranhaMessage
from Logic.Home.LogicClientHome import LogicClientHome
from Logic.Avatar.LogicClientAvatar import LogicClientAvatar

class OwnHomeDataMessage(PiranhaMessage):
    def __init__(self) -> None:
        super().__init__(0)

        self.clientHome = LogicClientHome()
        self.clientAvatar = LogicClientAvatar()

    def encode(self):
        super().encode()
        self.stream.writeInt(0)
        self.clientHome.encode(self.stream)
        
        self.clientAvatar.encode(self.stream)

    def getMessageType(self) -> int:
        return 24101