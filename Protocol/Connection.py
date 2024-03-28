import socket
import time
import threading
import traceback

from Protocol.Messaging import Messaging
from RC4Crypto.RC4Encrypter import RC4Encrypter
from Messages.PiranhaMessage import PiranhaMessage
from Messages.LogicMagicMessageFactory import LogicMagicMessageFactory
from Messages.MessageManager import MessageManager

def printByteArray(array: bytearray):
    hexStr = ''.join('\\x{:02x}'.format(b) for b in array)
    print(f'bytearray(b\"{hexStr}\")')

class Connection(threading.Thread):
    def __init__(self, socket: socket.socket, address):
        super().__init__()
        self.client = socket
        self.address = address

        self.crypto = RC4Encrypter("fhsd6f86f67rt8fw78fw789we78r9789wer6re", "nonce")
        
        self.messaging = Messaging(self.client)
        self.manager = MessageManager(self.messaging)

    def recv(self, n: int) -> bytearray: # receive packet (payload)
        data: bytearray = bytearray()
        while len(data) < n:
            packet = self.client.recv(n - len(data))
            if not packet:
                print("Data is NULL")
                return b''
            data.extend(packet)
        return data
    
    def run(self) -> None:
        try:
            while True:
                header = self.client.recv(7)
                
                if (len(header) >= 7):
                    messageType, encodingLength, messageVersion = Messaging.readHeader(header)
                    payload: bytearray = self.recv(encodingLength)

                    decPayload: bytearray = self.crypto.decrypt(payload)
                    # print(f"[Connection] Received: Type: {messageType} Length: {encodingLength} Version: {messageVersion}")
                    # printByteArray(decPayload)

                    message: PiranhaMessage = LogicMagicMessageFactory.createMessageByType(messageType)

                    if (message is not None):
                        message.setMessageVersion(messageVersion)
                        message.getByteStream().setByteArray(decPayload, encodingLength)
                        message.decode()

                        self.manager.receiveMessage(message)
                    else:
                        print(f"[Connection] Ignoring message of unknown type {messageType}")

        except ConnectionError:
            print(f"Client {self.address[0]}:{self.address[1]} has disconnected")
            self.client.close()
        except Exception as e:
            print("Error: " + str(e))
            traceback.print_exc()