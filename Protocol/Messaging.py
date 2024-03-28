from Messages.PiranhaMessage import PiranhaMessage
from RC4Crypto.RC4Encrypter import RC4Encrypter

import socket

class Messaging:
    def __init__(self, client: socket.socket) -> None:
        self.client = client

        self.encrypter = RC4Encrypter("fhsd6f86f67rt8fw78fw789we78r9789wer6re", "nonce")

    def sendMessage(self, message: PiranhaMessage):
        message.encode()

        encodingBytes = message.getByteStream().getByteArray()[:message.getEncodingLength()]
        encEncodingBytes = self.encrypter.encrypt(encodingBytes)

        fullPayload = bytearray(len(encEncodingBytes) + 7)
        Messaging.writeHeader(fullPayload, message, len(encEncodingBytes))
        fullPayload[7:] = encEncodingBytes

        self.client.send(fullPayload)
        print("[Messaging] Sent " + str(message.getMessageType()))

    def recv(self, n) -> bytearray:
        data = bytearray()
        while len(data) < n:
            packet = self.client.recv(n - len(data))
            if not packet:
                print("Data is NULL")
                return b''
            data.extend(packet)
        return data

    @staticmethod
    def readHeader(buffer: bytearray):
        messageType = buffer[0] << 8 | buffer[1]
        encodingLength = buffer[2] << 16 | buffer[3] << 8 | buffer[4]
        messageVersion = buffer[5] << 8 | buffer[6]
        return messageType, encodingLength, messageVersion

    @staticmethod
    def writeHeader(buffer: bytearray, message: PiranhaMessage, length: int):
        messageType = message.getMessageType()
        messageVersion = message.getMessageVersion()

        buffer[0] = (messageType >> 8) & 0xFF
        buffer[1] = messageType & 0xFF
        buffer[2] = (length >> 16) & 0xFF
        buffer[3] = (length >> 8) & 0xFF
        buffer[4] = length & 0xFF
        buffer[5] = (messageVersion >> 8) & 0xFF
        buffer[6] = messageVersion & 0xFF
