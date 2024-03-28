from DataStream.ChecksumEncoder import ChecksumEncoder
from Logic.Long.LogicLong import LogicLong

class ByteStream(ChecksumEncoder):
    def __init__(self, capacity: int) -> None:
        super().__init__()
        self.bitIndex: int = 0
        self.buffer: bytearray = bytearray(capacity)
        self.length: int = 0
        self.offset: int = 0

    def getLength(self) -> int:
        if (self.offset < self.length):
            return self.length
        
        return self.offset
    
    def getOffset(self) -> int:
        return self.offset
    
    def isAtEnd(self) -> bool:
        return self.offset >= self.length
    
    def clear(self, capacity: int):
        self.buffer = bytearray(capacity)
        self.offset = 0

    def getByteArray(self) -> bytearray:
        return self.buffer
    
    def readBoolean(self) -> bool:
        if (self.bitIndex == 0):
            self.offset += 1

        value: bool = (self.buffer[self.offset - 1] & (1 << self.bitIndex)) != 0
        self.bitIndex = (self.bitIndex + 1) & 7

        return value
    
    def readByte(self):
        self.bitIndex = 0
        value = self.buffer[self.offset]
        self.offset += 1
        return value
    
    def readShort(self):
        self.bitIndex = 0

        value = (self.buffer[self.offset] << 8) | self.buffer[self.offset + 1]
        self.offset += 2

        return value
    
    def readInt(self): 
        self.bitIndex = 0

        value = (self.buffer[self.offset] << 24) | (self.buffer[self.offset + 1] << 16) | (self.buffer[self.offset + 2] << 8) | self.buffer[self.offset + 3]
        self.offset += 4

        return value
    
    def readLong(self) -> LogicLong:
        long: LogicLong = LogicLong()
        long.decode(self)
        return long

    def readBytesLength(self) -> int:
        return self.readInt()
    
    def readBytes(self, length: int, maxCapacity: int) -> bytearray:
        self.bitIndex = 0

        if (length <= -1):
            if (length != -1):
                print("Negative readBytes length encountered.")

            return None

        if (length <= maxCapacity):
            array: bytearray = self.buffer[self.offset: self.offset + length]
            self.offset += length
            return array
        
        print("readBytes too long array, max " + str(maxCapacity))
        return None

    def readString(self, maxCapacity: int = 900001) -> str:
        length: int = self.readBytesLength()

        if (length == -1):
            if (length != -1):
                print("Too long String encountered.")

            return None
        else:
            if (length <= maxCapacity):
                byteArray: bytearray = self.buffer[self.offset: self.offset + length]
                stringValue: str = byteArray.decode("utf-8")
                self.offset += length
                return stringValue
            
            print("Too long String encountered, max " + str(maxCapacity))

        return None
    
    def readStringReference(self, maxCapacity: int = 900000) -> str:
        length: int = self.readBytesLength()

        if (length <= -1):
            print("Negative String length encountered.")

        else:
            if (length <= maxCapacity):
                byteArray: bytearray = self.buffer[self.offset: self.offset + length]
                stringValue: str = byteArray.decode("utf-8")
                self.offset += length
                return stringValue
            
            print("Too long String encountered, max " + maxCapacity)
        
        return ""
                

    def writeBoolean(self, value: bool):
        super().writeBoolean(value)

        if self.bitIndex == 0:
            self.ensureCapacity(1)
            self.buffer[self.offset] = 0
            self.offset += 1

        if value:
            self.buffer[self.offset - 1] |= (1 << self.bitIndex) & 0xFF

        self.bitIndex = (self.bitIndex + 1) & 7

    def writeByte(self, value: int):
        super().writeByte(value)

        self.ensureCapacity(1)

        self.bitIndex = 0

        self.buffer[self.offset] = value
        self.offset += 1

    def writeShort(self, value: int):
        super().writeShort(value)

        self.ensureCapacity(2)

        self.bitIndex = 0

        self.buffer[self.offset] = (value >> 8) & 0xFF
        self.buffer[self.offset + 1] = value & 0xFF

        self.offset += 2

    def writeInt(self, value: int):
        super().writeInt(value)

        self.ensureCapacity(4)

        self.bitIndex = 0

        self.buffer[self.offset] = (value >> 24) & 0xFF
        self.buffer[self.offset + 1] = (value >> 16) & 0xFF
        self.buffer[self.offset + 2] = (value >> 8) & 0xFF
        self.buffer[self.offset + 3] = value & 0xFF

        self.offset += 4

    def writeIntToByteArray(self, value: int) -> None:
        self.writeInt(value)

    def writeBytes(self, value: bytearray, length: int):
        super().writeBytes(value, length)

        if value is None:
            self.writeInt(-1)
        else:
            self.ensureCapacity(length + 4)
            self.writeInt(length)

            self.buffer[self.offset:self.offset + length] = value
            self.offset += length

    def writeString(self, value: str):
        super().writeString(value)

        if (value is None):
            self.writeInt(-1)

        else:
            bytesValue: bytes = value.encode("utf-8")
            length: int = len(bytesValue)

            if (length <= 900001):
                self.ensureCapacity(length + 4)
                self.writeInt(length)

                self.buffer[self.offset:self.offset + length] = bytesValue
                self.offset += length
            else:
                print("ByteStream::writeString invalid string length " + str(length))
                self.writeInt(-1)

    def writeStringReference(self, value: str):
        super().writeStringReference(value)

        bytesValue: bytes = value.encode("utf-8")
        length: int = len(bytesValue)

        if (length <= 900001):
            self.ensureCapacity(length + 4)
            self.writeInt(length)

            self.buffer[self.offset:self.offset + length] = bytesValue
            self.offset += length
        else:
            print("ByteStream::writeString invalid string length " + str(length))
            self.writeInt(-1)


    def resetOffset(self):
        self.offset = 0
        self.bitIndex = 0

    def setByteArray(self, buffer: bytearray, length: int):
        self.offset = 0
        self.bitIndex = 0
        self.buffer = buffer
        self.length = length

    def setOffset(self, offset: int):
        self.offset = offset
        self.bitIndex = 0

    def ensureCapacity(self, capacity: int):
        bufferLength = len(self.buffer)

        if self.offset + capacity > bufferLength:
            tmpBuffer = bytearray(bufferLength + capacity + 100)
            tmpBuffer[:bufferLength] = self.buffer # copy from buffer to tmpBuffer by bufferLength
            self.buffer = tmpBuffer

    def destruct(self):
        self.buffer = None
        self.bitIndex = 0
        self.length = 0
        self.offset = 0