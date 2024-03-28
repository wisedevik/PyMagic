from DataStream.ByteStream import ByteStream

class PiranhaMessage:
    def __init__(self, version) -> None:
        self.stream = ByteStream(10)
        self.version = version

    def decode(self):
        ...

    def encode(self):
        ...

    def getMessageType(self) -> int:
        return 0
    
    def destruct(self):
        self.stream.destruct()

    def getServiceNodeType(self) -> int:
        return -1
    
    def getMessageVersion(self) -> int:
        return self.version
    
    def setMessageVersion(self, version: int):
        self.version = version

    def isServerToClientMessage(self) -> bool:
        return self.getMessageType() >= 20000
    
    def getMessageBytes(self) -> bytearray:
        return self.stream.getByteArray()
    
    def getEncodingLength(self) -> int:
        return self.stream.getLength()
    
    def getByteStream(self) -> ByteStream:
        return self.stream