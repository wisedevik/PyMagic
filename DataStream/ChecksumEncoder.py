from Logic.Long.LogicLong import LogicLong

class ChecksumEncoder:
    def __init__(self) -> None:
        self.checksum: int = 0
        self.snapshotChecksum: int = 0
        
        self.enabled: bool = True

    def enableCheckSum(self, enable: bool):
        if (not self.enabled or enable):
            if (not self.enabled and enable):
                self.checksum = self.snapshotChecksum
            
            self.enabled = enable
        else:
            self.snapshotChecksum = self.checksum
            self.enabled = False

    def resetChecksum(self):
        self.checksum = 0

    def writeBoolean(self, value: bool):
        self.checksum = (13 if value else 7) + self.rotateRight(self.checksum, 31)

    def writeByte(self, value: int):
        self.checksum = value + self.rotateRight(self.checksum, 31) + 11

    def writeShort(self, value: int):
        self.checksum = value + self.rotateRight(self.checksum, 31) + 19

    def writeInt(self, value: int):
        self.checksum = value + self.rotateRight(self.checksum, 31) + 9

    def writeLong(self, value: LogicLong):
        value.encode(self)

    def writeBytes(self, value: bytes, length: int):
        self.checksum = ((length + 28 if value is not None else 27) + (self.checksum >> 31)) | (self.checksum << (32 - 31))

    def writeString(self, value: str):
        self.checksum = (len(value) + 28 if value is not None else 27) + self.rotateRight(self.checksum, 31)

    def writeStringReference(self, value: str):
        self.checksum = len(value) + self.rotateRight(self.checksum, 31) + 38

    def isCheckSumEnabled(self) -> bool:
        return self.enabled
    
    def isCheckSumOnlyMode(self) -> bool:
        return True
    
    @staticmethod
    def rotateRight(value: int, count: int):
        return (value >> count) | (value << (32 - count))