import socket

from Protocol.Connection import Connection

class TcpNetwork:
    def __init__(self, address) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.setupConnection(address)

    def setupConnection(self, address):
        self.server.bind(address)
        print("[TcpNetwork] Server is listening at " + str(address))
        while True:
            self.server.listen(100)
            socket, address = self.server.accept()
            print(f"[TcpNetwork] New connection from {address[0]}:{address[1]}")
            Connection(socket, address).start()